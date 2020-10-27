import json
import requests

with open("./neighborhoods.json", "r") as read_file:
    data = json.load(read_file)

headers = {
    "Accept": "*/*",
    "Content-Type": "application/json"
}

errors = []

for state in ['DF', 'SP']:
    for neigh in data[state]:
        r = requests.post("http://0.0.0.0:8083/api/neighborhood/",
                        data=json.dumps(neigh),
                        headers=headers
                        )
        if(r.status_code != 201):
            print(r.status_code)
            print(neigh['neighborhood'])
            print()
            errors.append(neigh)

for i in errors:
    r = requests.post("http://0.0.0.0:8083/api/neighborhood/",
                      data=json.dumps(neigh),
                      headers=headers
                      )
    if(r.status_code != 201):
        print(r.status_code)
        print(neigh['neighborhood'])
        print()
