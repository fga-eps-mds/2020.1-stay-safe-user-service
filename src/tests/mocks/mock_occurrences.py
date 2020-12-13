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
        "occurrence_date_time": "2020-10-31 00:00:00",
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
            -48.044176
        ],
        "occurrence_date_time": "2020-11-01 00:00:00",
        "occurrence_type": "Furto de Veículo",
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
            -48.044177
        ],
        "occurrence_date_time": "2020-11-02 00:00:00",
        "occurrence_type": "Roubo de Residência",
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
            -48.044178
        ],
        "occurrence_date_time": "2020-11-03 00:00:00",
        "occurrence_type": "Furto de Veículo",
        "physical_aggression": True,
        "police_report": False,
        "victim": True
    },
    {
        "gun": "Fire",
        "user": "ghjklasdf",
        "id_occurrence": -1,
        "location": [
            -15.989564,
            -48.044179
        ],
        "occurrence_date_time": "2020-11-04 00:00:00",
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
    {
        # without victim field
        "occurrence_date_time": "2000-06-15 00:00:00",
        "physical_aggression": True,
        "police_report": False,
        "gun": "Arma",
        "location": [
            -15.989564,
            -48.044175
        ],
        "occurrence_type": "Roubo de Bicicleta"
    },
    {
        # without a few fields
        "occurrence_date_time": "2020-12-1 00:00:00",
        "location": [
            -15.989564,
            -48.044175
        ],
        "occurrence_type": "Roubo de Chiclete"
    },
    {
        # without a few fields
        "occurrence_date_time": "2000-06-15 00:00:00",
        "location": -9999,
        "occurrence_type": 1.0
    },
    {
        # Invalid field type
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
        "victim": "Stay Safe"
    },
    {
        # Invalid gun
        "gun": "Arma",
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
    {
        # Invalid occurrence_type
        "gun": "White",
        "user": "ghjklasdf",
        "id_occurrence": -1,
        "location": [
            -15.989564,
            -48.044175
        ],
        "occurrence_date_time": "2020-06-04 00:00:00",
        "occurrence_type": "Roubo de Chiclete",
        "physical_aggression": True,
        "police_report": False,
        "victim": True
    },
    {
        # Invalid date
        "gun": "White",
        "user": "ghjklasdf",
        "id_occurrence": -1,
        "location": [
            -15.989564,
            -48.044175
        ],
        "occurrence_date_time": "2022-12-12 00:00:00",
        "occurrence_type": "Roubo de Residência",
        "physical_aggression": True,
        "police_report": False,
        "victim": True
    },
]

correct_occurrence_update = {
    "police_report": True,
    "occurrence_type": "Roubo de Residência"
}
