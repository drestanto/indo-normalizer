import pandas as pd
import time
import openai
from indo_normalizer import Normalizer

# ==== CONFIG ====
INPUT_FILE = "experiment_research_raw_input.csv"
OUTPUT_FILE = "experiment_research_raw_data.csv"
OPENAI_API_KEY = "blah"  # Replace with your key
MODEL_NAME = "gpt-4o-mini"  # You can change model here
RATE_LIMIT_DELAY = 1.2  # seconds between requests to avoid hitting the rate limit
# =================

openai.api_key = OPENAI_API_KEY

# 1. Load CSV
df = pd.read_csv(INPUT_FILE, sep=';')

# 2. Ensure columns exist
required_columns = ["Post ID", "Original Text", "Ground Truth (Manual)", "Indo-Normalizer Output", "GPT Output"]
for col in required_columns:
    if col not in df.columns:
        df[col] = ""

# 3. Initialize Indo-Normalizer
normalizer = Normalizer()

# 4. Fill Indo-Normalizer Output
for idx, row in df.iterrows():
    text = str(row["Original Text"])
    if text.strip():
        normalized_text, _ = normalizer.normalize_text(text)
        df.at[idx, "Indo-Normalizer Output"] = normalized_text

# 5. Fill GPT Output with API calls
for idx, row in df.iterrows():
    text = str(row["Original Text"])
    if text.strip():
        try:
            response = openai.ChatCompletion.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are an Indonesian text normalizer. Convert the given text into standard, formal Indonesian."},
                    {"role": "user", "content": text}
                ],
                temperature=0
            )
            gpt_output = response.choices[0].message["content"].strip()
            df.at[idx, "GPT Output"] = gpt_output
        except Exception as e:
            print(f"Error at row {idx}: {e}")
            df.at[idx, "GPT Output"] = "[ERROR]"
        
        # Respect rate limits
        time.sleep(RATE_LIMIT_DELAY)

# 6. Save to CSV
df.to_csv(OUTPUT_FILE, index=False, sep=';')
print(f"Processing complete. Output saved to {OUTPUT_FILE}")
