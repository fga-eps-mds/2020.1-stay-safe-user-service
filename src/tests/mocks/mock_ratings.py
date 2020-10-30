user = {
    'full_name': 'Joana da Silva',
    'username': 'joaninha',
    'email': 'joana@doemail.com',
    'password': '292mcXEAuz'
}

neighborhood = {
    "neighborhood": "Lago Sul 2",
    "city": "Brasília",
    "state": "DF"
}

correct_ratings = [
    {
        "rating_neighborhood": 5,
        "lighting": True,
        "movement_of_people": True,
        "police_rounds": True
    },
    {
        "rating_neighborhood": 3,
        "lighting": False,
        "movement_of_people": True,
        "police_rounds": False
    },
    {
        "rating_neighborhood": 2,
        "lighting": False,
        "movement_of_people": False,
        "police_rounds": True
    },
]

wrong_ratings = [
    {
        # Invalid detail to rating 5
        "rating_neighborhood": 5,
        "lighting": True,
        "movement_of_people": True,
        "police_rounds": False,
    },
    {
        # Invalid detail to rating 1
        "rating_neighborhood": 1,
        "lighting": True,
        "movement_of_people": False,
        "police_rounds": False,
    },
    {
        # Without rating
        "lighting": False,
        "movement_of_people": False,
        "police_rounds": False,
    },
]

correct_update_rating = {
    "rating_neighborhood": 2,
    "lighting": False,
    "movement_of_people": False,
    "police_rounds": True,
}
