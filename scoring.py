import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from backend.utils.profile_weights import get_profile_weights
from backend.utils.ingredient_cleaner import clean_ingredient_name, get_alias_matches
from backend.ocr.ocr_reader import get_cleaned_ingredient_list as extract_ingredient_list_from_image

# Load dataset once
ingredient_db = pd.read_csv(
    r"C:\1_PROFESSIONAL\RIST\8th Sem\MAJOR_PROJECT_DETAILS\8_Model\food-comparator\backend\utils\Final_Indian_Ingredient_HealthDataset_Scored - Copy.csv"
)

def get_health_score(ingredient, profile_weights, embedding_model=None):
    cleaned = clean_ingredient_name(ingredient)
    matched_rows = get_alias_matches(cleaned, ingredient_db)

    if not matched_rows.empty:
        base_score = matched_rows.iloc[0]['health_score']
    elif embedding_model:
        emb = embedding_model.encode([ingredient])
        all_embeddings = np.stack(ingredient_db['embedding'].apply(eval))
        sims = cosine_similarity(emb, all_embeddings)[0]
        idx = np.argmax(sims)
        base_score = ingredient_db.iloc[idx]['health_score']
    else:
        base_score = None  # Not found

    profile_multiplier = profile_weights.get(cleaned, 1.0)
    return None if base_score is None else base_score * profile_multiplier

def compare_ingredient_lists(list1, list2, profile_data=None, embedding_model=None):
    # Extract selected condition if valid, else use default
    if isinstance(profile_data, dict) and profile_data:
        selected_condition = next(iter(profile_data.keys()))
    else:
        selected_condition = "default"

    profile_weights = get_profile_weights(selected_condition)

    def calc_weighted_score(ingredient_list):
        scores = []
        for ing in ingredient_list:
            score = get_health_score(ing, profile_weights, embedding_model)
            scores.append((ing, score))
        valid_scores = [s for _, s in scores if s is not None]
        avg_score = np.mean(valid_scores) if valid_scores else 0.0
        return avg_score, scores

    score1, details1 = calc_weighted_score(list1)
    score2, details2 = calc_weighted_score(list2)

    intersection = set(list1) & set(list2)
    union = set(list1) | set(list2)
    similarity = len(intersection) / len(union) if union else 0.0

    recommendation = "Food 1" if score1 > score2 else "Food 2" if score2 > score1 else "Both are similar"

    # Sort by absolute impact on score and take top 3 contributors
    top1 = sorted([d for d in details1 if d[1] is not None], key=lambda x: abs(x[1]), reverse=True)[:3]
    top2 = sorted([d for d in details2 if d[1] is not None], key=lambda x: abs(x[1]), reverse=True)[:3]

    return {
        "food1_score": round(score1, 3),
        "food2_score": round(score2, 3),
        "similarity": round(similarity, 3),
        "recommendation": recommendation,
        "details": {
            "food1_top_ingredients": [(ing, round(score, 2)) for ing, score in top1],
            "food2_top_ingredients": [(ing, round(score, 2)) for ing, score in top2]
        }
    }

# For direct testing
if __name__ == "__main__":
    img1 = r"C:\1_PROFESSIONAL\RIST\8th Sem\MAJOR_PROJECT_DETAILS\8_Model\food-comparator\test_images\4.jpg"
    img2 = r"C:\1_PROFESSIONAL\RIST\8th Sem\MAJOR_PROJECT_DETAILS\8_Model\food-comparator\test_images\3.jpg"

    ingredients1 = extract_ingredient_list_from_image(img1)
    ingredients2 = extract_ingredient_list_from_image(img2)

    print("\nIngredients from Image 1:", ingredients1)
    print("Ingredients from Image 2:", ingredients2)

    user_profile = {
        "Diabetes": True
    }

    result = compare_ingredient_lists(ingredients1, ingredients2, user_profile)
    print("\nComparison Result:")
    print(result)
