correct_occurrences = [
    {
        "occurrence_date_time": "05-09-20 00:00:00",
        "physical_aggression": True,
        "victim": True,
        "police_report": False,
        "gun": "fire",
        "location": [
            -15.989564,
            -48.044175
        ],
        "occurrence_type": "Latrocínio"
    },
    {
        "occurrence_date_time": "04-08-20 00:00:00",
        "physical_aggression": False,
        "victim": False,
        "police_report": True,
        "gun": "null",
        "location": [
            -15.989564,
            -48.044175
        ],
        "occurrence_type": "Roubo de Veículo"
    },
    {
        "occurrence_date_time": "15-06-20 00:00:00",
        "physical_aggression": True,
        "victim": True,
        "police_report": False,
        "gun": "white",
        "location": [
            -15.989564,
            -48.044175
        ],
        "occurrence_type": "Roubo de Residência"
    },
]

wrong_occurrences = [
    {
        # invalid date
        "occurrence_date_time": "09-05-18 00:00:00",
        "physical_aggression": True,
        "victim": True,
        "police_report": False,
        "gun": "fire",
        "location": [
            -15.989564,
            -48.044175
        ],
        "occurrence_type": "Latrocínio"
    },
    {
        # invalid gun
        "occurrence_date_time": "04-08-20 00:00:00",
        "physical_aggression": False,
        "victim": False,
        "police_report": True,
        "gun": "faca",
        "location": [
            -15.989564,
            -48.044175
        ],
        "occurrence_type": "Roubo de Veículo"
    },
    {
        # invalid occurrecncy_type
        "occurrence_date_time": "15-06-20 00:00:00",
        "physical_aggression": True,
        "victim": True,
        "police_report": False,
        "gun": "white",
        "location": [
            -15.989564,
            -48.044175
        ],
        "occurrence_type": "Roubo de Bicicleta"
    },
]

correct_occurrence_update = {
    "id_occurrency": 1
    "police_report": True,
    "occurrence_type": "Roubo de Residência"
}