import json
import requests

with open('df.txt', 'r', encoding='utf-8') as f:
    data = f.readlines()
f.close()

headers = {
    "Accept": "*/*",
    "Content-Type": "application/json"
}

a = 1
for i in range(0, len(data)):
    data[i] = data[i].strip()
    if (a == 1):
        city = data[i]
        a = 0
        continue

    if (data[i] == ''):
        a = 1
        continue
    
    m = {
        "neighborhood": data[i],
        "city": city,
        "state": "DF"
    }

    r = requests.post("http://0.0.0.0:8083/api/neighborhood/", data=json.dumps(m), headers=headers)
    if(r.status_code != 201):
        print(r.status_code)
        print(neighborhood)
        print()



print(data[3] == '')