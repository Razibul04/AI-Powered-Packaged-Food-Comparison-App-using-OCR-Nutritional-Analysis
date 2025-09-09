import pandas as pd

# Load both datasets
cspi_df = pd.read_csv("cspi_food_additives.csv")
codex_df = pd.read_csv("codex_additives.csv")

# Standardize key columns for merging
cspi_df['ingredient'] = cspi_df['ingredient'].str.lower().str.strip()
codex_df['ingredient'] = codex_df['ingredient'].str.lower().str.strip()

# Merge on 'ingredient' (prioritizing CSPI data)
merged_df = pd.concat([cspi_df, codex_df], ignore_index=True)

# Drop duplicates based on 'ingredient' or 'aliases'
merged_df.drop_duplicates(subset=['ingredient', 'aliases'], keep='first', inplace=True)

# Optional: Sort by health score (ascending = more harmful first)
merged_df.sort_values(by='health score', inplace=True)

# Save the final dataset
merged_df.to_csv("final_food_additives.csv", index=False)

print("✅ Merged dataset saved as 'final_food_additives.csv'")
