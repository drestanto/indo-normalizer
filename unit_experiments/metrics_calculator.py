import pandas as pd
import re

# ==== CONFIG ====
CSV_FILE = "experiment_research_raw_data.csv"
OUTPUT_FILE = "experiment_research_full_metrics.csv"
SIMULATED_TIME = 0.05  # seconds per post, adjust if you have real times
# =================

# Load CSV
df = pd.read_csv(CSV_FILE, sep=";")

# Helper: tokenize words
def tokenize(text):
    return re.findall(r'\w+', str(text).lower())

# --- Metrics containers ---
indo_success_rates = []
gpt_success_rates = []
processing_times = []

all_original_tokens = []
all_ground_tokens = []
all_indo_tokens = []
all_gpt_tokens = []

# --- Per-post calculations ---
for _, row in df.iterrows():
    original_tokens = tokenize(row["Original Text"])
    ground_tokens = tokenize(row["Ground Truth (Manual)"])
    indo_tokens = tokenize(row["Indo-Normalizer Output"])
    gpt_tokens = tokenize(row["GPT Output"])

    # Collect tokens for overall token reduction
    all_original_tokens.extend(original_tokens)
    all_ground_tokens.extend(ground_tokens)
    all_indo_tokens.extend(indo_tokens)
    all_gpt_tokens.extend(gpt_tokens)

    # --- Success Rate vs Ground Truth ---
    indo_correct = sum(1 for o, n in zip(ground_tokens, indo_tokens) if o == n)
    gpt_correct = sum(1 for o, n in zip(ground_tokens, gpt_tokens) if o == n)
    indo_success_rates.append((indo_correct / max(len(ground_tokens),1)) * 100)
    gpt_success_rates.append((gpt_correct / max(len(ground_tokens),1)) * 100)

    # --- Simulate processing time ---
    processing_times.append(SIMULATED_TIME)

# --- Overall Token Reduction ---
unique_original = set(all_original_tokens)
unique_ground = set(all_ground_tokens)
unique_indo = set(all_indo_tokens)
unique_gpt = set(all_gpt_tokens)

ground_reduction = (len(unique_ground) - len(unique_original)) / len(unique_original) * 100
indo_reduction = (len(unique_indo) - len(unique_original)) / len(unique_original) * 100
gpt_reduction = (len(unique_gpt) - len(unique_original)) / len(unique_original) * 100

# --- Aggregate metrics ---
avg_processing_time = sum(processing_times) / len(processing_times)
posts_per_minute = 60 / avg_processing_time

summary = {
    "Indo-Normalizer Success Rate (%)": sum(indo_success_rates)/len(indo_success_rates),
    "GPT Success Rate (%)": sum(gpt_success_rates)/len(gpt_success_rates),
    "Indo-Normalizer Token Reduction (%)": indo_reduction,
    "GPT Token Reduction (%)": gpt_reduction,
    "Ground Truth Token Reduction (%)": ground_reduction,
    "Average Processing Time per Post (s)": avg_processing_time,
    "Total Posts Processed per Minute": posts_per_minute,
    "Total Posts": len(df)
}

# --- Print summary ---
print("\n=== Full Normalization Metrics Summary ===")
for k, v in summary.items():
    print(f"{k}: {v:.2f}")