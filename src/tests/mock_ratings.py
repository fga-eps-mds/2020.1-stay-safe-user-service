user = {
    'full_name': 'Joana da Silva',
    'username': 'joaninha',
    'email': 'joana@doemail.com',
    'password': '292mcXEAuz'
}

neighborhood = {
    "neighborhood": "Lago Sul",
	"city": "Brasília",
	"state": "DF"
}

correct_ratings = [
    {
        "rating_neighborhood": 4,
	    "details": "good lighting",
        "id_rating": -1
    },
    {
        "rating_neighborhood": 3,
	    "details": "good movement of people",
        "id_rating": -1
    },
    {
        "rating_neighborhood": 1,
	    "details": "bad lighting",
        "id_rating": -1
    },
]

wrong_ratings = [
    {
        #Invalid detail to rating 4
        "rating_neighborhood": 4,
	    "details": "bad lighting"
    },
    {
        #Invalid detail to rating 1
        "rating_neighborhood": 1,
	    "details": "good lighting"
    },
    {
        #Without details
        "rating_neighborhood": 4
    },
    {
        #Without rating
        "details": "good lighting"
    },
]

correct_update_rating = {
	"rating_neighborhood": 2,
	"details": "bad lighting"
}
