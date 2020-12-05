from math import radians, cos, sin, asin, sqrt


def get_params_by_body(fields, body):
    params = {}
    for field in fields:
        if field in body:
            params[field] = body[field]
    return params


def haversine(favorite_place, occurrence):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1 = occurrence['location']
    lon2, lat2 = favorite_place['latitude'], favorite_place['longitude']
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles

    return favorite_place if c * r <= 1 else None
