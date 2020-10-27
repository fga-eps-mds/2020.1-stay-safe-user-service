import json
import requests


def printProgressBar(iteration, total):
    """
    Call in a loop to create terminal progress bar
    """
    prefix='Progress'
    suffix='Complete'
    decimals=1
    length=50
    fill='█'
    printEnd="\r"
    percent =\
        ("{0:." + str(decimals) + "f}").format(100 * (iteration/float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


with open("./neighborhoods.json", "r") as read_file:
    data = json.load(read_file)

headers = {
    "Accept": "*/*",
    "Content-Type": "application/json"
}

errors = []

len_neighborhoods = len(data['DF']) + len(data['SP'])
printProgressBar(0, len_neighborhoods)

for i, neigh in enumerate(data['DF']):
    r = requests.post("http://0.0.0.0:8083/api/neighborhood/",
                      data=json.dumps(neigh),
                      headers=headers
                      )
    if(r.status_code != 201):
        print(r.status_code)
        print(neigh['neighborhood'])
        print()
        errors.append(neigh)
    printProgressBar(i+1, len_neighborhoods)


for i, neigh in enumerate(data['SP']):
    r = requests.post("http://0.0.0.0:8083/api/neighborhood/",
                      data=json.dumps(neigh),
                      headers=headers
                      )
    if(r.status_code != 201):
        print(r.status_code)
        print(neigh['neighborhood'])
        print()
        errors.append(neigh)
    printProgressBar(i+1+len(data['DF']), len_neighborhoods)

for i in errors:
    r = requests.post("http://0.0.0.0:8083/api/neighborhood/",
                      data=json.dumps(neigh),
                      headers=headers
                      )
    if(r.status_code != 201):
        print(r.status_code)
        print(neigh['neighborhood'])
        print()
