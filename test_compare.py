import requests

data = {
    "ingredients1": ["sugar", "milk solids", "rice bran oil", "iodised salt", "maltodextrin", "INS 551", "wheat","INS 330"],
    "ingredients2": ["Potato", "palm oil", "iodised salt", "maltodextrin", "black salt", "sugar", "tomato powder", "INS 551","INS 627"],
    "profile": {
        "goal": "weight_loss",
        "sensitivity": ["sugar"]
    }
}

response = requests.post("http://127.0.0.1:5000/compare", json=data)
print(response.json())
