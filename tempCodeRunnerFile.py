
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
    profile_weights = get_profile_weights(profile_data or {})

    def calc_weighted_score(ingredient_list):
        scores = [get_health_score(ing, profile_weights, embedding_model) for ing in ingredient_list]
        filtered_scores = [s for s in scores if s is not None]
        return (np.mean(filtered_scores) if filtered_scores else 0.0), scores

    score1, details1 = calc_weighted_score(list1)
    score2, details2 = calc_weighted_score(list2)

    intersection = set(list1) & set(list2)
    union = set(list1) | set(list2)
    similarity = len(intersection) / len(union) if union else 0.0

    recommendation = "Food 1" if score1 > score2 else "Food 2" if score2 > score1 else "Both are similar"

    return {
        "food1_score": round(score1, 3),
        "food2_score": round(score2, 3),
        "similarity": round(similarity, 3),
        "recommendation": recommendation,
        "details": {
            "food1_ingredients": list1,
            "food1_individual_scores": details1,
            "food2_ingredients": list2,
            "food2_individual_scores": details2
        }
    }

# For direct testing