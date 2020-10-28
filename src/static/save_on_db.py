import os
import json
from controllers import neighborhood as controller


def printProgressBar(iteration, total):
    """
    Call in a loop to create terminal progress bar
    """
    prefix = 'Progress'
    suffix = 'Complete'
    decimals = 1
    length = 50
    fill = '█'
    printEnd = "\r"
    percent =\
        ("{0:." + str(decimals) + "f}").format(100 * (iteration/float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


dir = os.path.dirname(__file__)
with open(dir + "/neighborhoods.json", "r") as read_file:
    data = json.load(read_file)

headers = {
    "Accept": "*/*",
    "Content-Type": "application/json"
}

errors = []

len_neighborhoods = len(data['DF']) + len(data['SP'])
printProgressBar(0, len_neighborhoods)

for i, neigh in enumerate(data['DF']):
    r, code = controller.create_neighborhood(neigh)

    if(code != 201):
        print(code)
        print(neigh['neighborhood'])
        print()
        errors.append(neigh)
    printProgressBar(i+1, len_neighborhoods)


for i, neigh in enumerate(data['SP']):
    r, code = controller.create_neighborhood(neigh)

    if(code != 201):
        print(code)
        print(neigh['neighborhood'])
        print()
        errors.append(neigh)
    printProgressBar(i+1+len(data['DF']), len_neighborhoods)

for i in errors:
    r, code = controller.create_neighborhood(neigh)

    if(code != 201):
        print(code)
        print(neigh['neighborhood'])
        print()
