user = {
    'full_name': 'Amanda Magalhaes',
    'username': 'ghjklasdf',
    'email': 'anderson2222@uorak.com',
    'password': '292mcXEAuz'
}

correct_occurrences = [
    {
        "gun": "Fire",
        "user": "ghjklasdf",
        "id_occurrence": -1,
        "location": [
            -15.989564,
            -48.044175
        ],
        "occurrence_date_time": "2020-09-05 00:00:00",
        "occurrence_type": "Latrocínio",
        "physical_aggression": True,
        "police_report": False,
        "victim": True
    },
    {
        "gun": "None",
        "user": "ghjklasdf",
        "id_occurrence": -1,
        "location": [
            -15.989564,
            -48.044175
        ],
        "occurrence_date_time": "2020-04-08 00:00:00",
        "occurrence_type": "Roubo de Veículo",
        "physical_aggression": False,
        "police_report": True,
        "victim": False
    },
    {
        "gun": "White",
        "user": "ghjklasdf",
        "id_occurrence": -1,
        "location": [
            -15.989564,
            -48.044175
        ],
        "occurrence_date_time": "2020-06-04 00:00:00",
        "occurrence_type": "Roubo de Residência",
        "physical_aggression": True,
        "police_report": False,
        "victim": True
    },
]

wrong_occurrences = [
    {
        # invalid date
        "occurrence_date_time": "2018-05-09 00:00:00",
        "physical_aggression": True,
        "victim": True,
        "police_report": False,
        "gun": "Fire",
        "location": [
            -15.989564,
            -48.044175
        ],
        "occurrence_type": "Latrocínio"
    },
    {
        # invalid gun
        "occurrence_date_time": "2000-08-04 00:00:00",
        "physical_aggression": False,
        "victim": False,
        "police_report": True,
        "gun": "Faca",
        "location": [
            -15.989564,
            -48.044175
        ],
        "occurrence_type": "Roubo de Veículo"
    },
    {
        # invalid occurrency_type
        "occurrence_date_time": "2000-06-15 00:00:00",
        "physical_aggression": True,
        "victim": True,
        "police_report": False,
        "gun": "White",
        "location": [
            -15.989564,
            -48.044175
        ],
        "occurrence_type": "Roubo de Bicicleta"
    },
]

correct_occurrence_update = {
    "police_report": True,
    "occurrence_type": "Roubo de Residência"
}