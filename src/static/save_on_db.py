import json
import requests

with open("./sp2.json", "r") as read_file:
    data = json.load(read_file)

data = list(filter(lambda x: x['Uf'] == "SP", data['data']))

headers = {
    "Accept": "*/*",
    "Content-Type": "application/json"
}

for i in data:
    c = i['Nome'].split(" - ")
    if (len(c) == 2):
        city = c[1]
        neighborhood = c[0]
    if (len(c) == 3):
        city = c[2]
        neighborhood = c[0] + '-' + c[1]
    if (len(c) == 4):
        city = c[3]
        neighborhood = c[0] + '-' + c[1] + '-' + c[2]
    m = {
        "neighborhood": neighborhood,
        "city": city,
        "state": i['Uf']
    }
    r = requests.post("http://0.0.0.0:8083/api/neighborhood/", data=json.dumps(m), headers=headers)
    if(r.status_code != 201):
        print(r.status_code)
        print(neighborhood)
        print()
