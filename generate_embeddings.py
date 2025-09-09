# backend/utils/generate_embeddings.py

import pandas as pd
from sentence_transformers import SentenceTransformer
import ast

df = pd.read_csv(r"C:\Users\Documents\8th_Semester\Major_Project\food-comparator\backend\utils\Final_Indian_Ingredient_HealthDataset_Scored.csv")

model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embeddings only if not present
if "embedding" not in df.columns or df["embedding"].isnull().any():
    df["embedding"] = df["Ingredient"].apply(lambda x: model.encode(x).tolist())
    df.to_csv(r"C:\Users\Documents\8th_Semester\Major_Project\food-comparator\backend\utils\Final_Indian_Ingredient_HealthDataset_Scored.csv", index=False)
    print("✅ Embeddings generated and saved.")
else:
    print("✅ Embeddings already present.")
