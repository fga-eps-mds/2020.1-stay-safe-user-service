def get_neighborhood_statistics(ratings):
    average = 0.0
    lighting = 0
    movement = 0
    police = 0

    lighting_positive = 0
    movement_positive = 0
    police_positive = 0

    p_lighting = 0
    p_movement = 0
    p_police = 0

    c_lighting = 0
    c_movement = 0
    c_police = 0

    for rating in ratings:
        average += rating['rating_neighborhood']
        if ("lighting" in rating['details']):
            lighting += 1
            if ("good" in rating['details']):
                lighting_positive += 1

        if ("movement of people" in rating['details']):
            movement += 1
            if ("good" in rating['details']):
                movement_positive += 1

        if ("police rounds" in rating['details']):
            police += 1
            if ("frequent" in rating['details']):
                police_positive += 1

    average /= len(ratings)
    if (lighting):
        p_lighting = lighting_positive * 100 / lighting
    if (movement):
        p_movement = movement_positive * 100 / movement
    if (police):
        p_police = police_positive * 100 / police

    if (p_lighting < 40 and p_lighting != 0):
        c_lighting = 1
    elif (p_lighting >= 40 and p_lighting <= 70):
        c_lighting = 2
    elif (p_lighting > 70):
        c_lighting = 3

    if (p_movement < 40 and p_movement != 0):
        c_movement = 1
    elif (p_movement >= 40 and p_movement <= 70):
        c_movement = 2
    elif (p_movement > 70):
        c_movement = 3

    if (p_police < 40 and p_police != 0):
        c_police = 1
    elif (p_police >= 40 and p_police <= 70):
        c_police = 2
    elif (p_police > 70):
        c_police = 3

    return dict({"average": round(average, 1),
                 "lighting": c_lighting,
                 "movement": c_movement,
                 "police": c_police
                 })
