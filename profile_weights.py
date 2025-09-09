# backend/utils/profile_weights.py

def get_profile_weights(condition):
    condition_multipliers = {
        "diabetes": {
            "sugar": 0.2,
            "maltodextrin": 0.3,
            "glucose": 0.2,
            "dextrose": 0.2,
            "fructose": 0.3
        },
        "gluten_free": {
            "wheat": 0.3,
            "barley": 0.3,
            "rye": 0.3,
            "gluten": 0.2,
            "semolina": 0.3
        },
        "lactose_intolerant": {
            "milk": 0.4,
            "milk solids": 0.4,
            "lactose": 0.3,
            "butter": 0.4,
            "cream": 0.3,
            "cheese": 0.3
        },
        "nut_allergy": {
            "peanuts": 0.2,
            "cashews": 0.3,
            "almonds": 0.3,
            "walnuts": 0.3,
            "hazelnuts": 0.3,
            "pistachios": 0.3
        },
        "low_sodium": {
            "salt": 0.3,
            "sodium": 0.2,
            "iodised salt": 0.3,
            "baking soda": 0.3,
            "monosodium glutamate": 0.2
        },
        "obesity": {
            "sugar": 0.5,
            "fat": 0.6,
            "oil": 0.6,
            "palm oil": 0.5,
            "fried": 0.4
        },
        "cholesterol": {
            "oil": 0.5,
            "fat": 0.4,
            "trans fat": 0.3,
            "saturated fat": 0.3
        },
        "kidney_disease": {
            "sodium": 0.2,
            "potassium": 0.3,
            "phosphates": 0.3,
            "protein": 0.4
        },
        "default": {}  # Neutral: no multipliers
    }

    condition = condition.lower().strip() if condition else "default"
    return condition_multipliers.get(condition, condition_multipliers["default"])
