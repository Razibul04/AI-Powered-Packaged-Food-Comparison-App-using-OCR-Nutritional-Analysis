# Ingredient normalization
import pandas as pd
import re

ingredient_db = pd.read_csv(r"C:\1_PROFESSIONAL\RIST\8th Sem\MAJOR_PROJECT_DETAILS\8_Model\food-comparator\backend\utils\Final_Indian_Ingredient_HealthDataset_Scored - Copy.csv")

def clean_ingredient_name(name):
    return re.sub(r"[^a-z ]", "", name.lower().strip())

def get_alias_matches(name, df):
    for _, row in df.iterrows():
        aliases = row['aliases']
        if pd.isna(aliases):
            continue
        alias_list = [a.strip().lower() for a in aliases.split(",")]
        if name in alias_list or name == row['ingredient'].lower():
            return pd.DataFrame([row])
    return pd.DataFrame()
