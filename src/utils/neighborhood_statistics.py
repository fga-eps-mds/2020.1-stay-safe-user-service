def get_indice(value):
    if value < 40 and value != 0:
        return 1
    if 40 <= value <= 70:
        return 2
    if value > 70:
        return 3
    return 0


def get_neighborhood_statistics(ratings):

    fields = {'average': 0.0}
    for attr in ratings[0]['details'].items():
        fields.update({attr[0]: {'total': 0, 'positive': 0}})

    for rating in ratings:
        fields['average'] += rating['rating_neighborhood']
        for attr, value in rating['details'].items():
            fields[attr]['total'] += 1
            if value:
                fields[attr]['positive'] += 1

    fields['average'] /= len(ratings)

    for attr, value in fields.items():
        if attr != 'average':
            fields[attr] = get_indice(value['positive'] * 100 / value['total'])
    fields['average'] = round(fields['average'], 1)

    return fields
