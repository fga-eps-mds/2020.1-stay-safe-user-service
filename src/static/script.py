import requests
import json

# -*- coding: utf-8 -*-
def print_json(name, number):
	
	aux = "{\n"
	aux += "	\"name\": \"" + str.rstrip(name) + "\"" + ",\n"
	aux += "	\"population\": " + str.rstrip(number) + "\n"
	aux += "}\n"
	return aux;

with open('Municipios.txt', 'r', encoding='utf-8') as f:
    myMunicipios = f.readlines()
f.close()

with open('Numeros.txt', 'r', encoding='utf-8') as f:
    myNumbers = f.readlines()
f.close()

lines = []
f = open("Saida.txt", "w")

for i in range(len(myMunicipios)):
	f.write(print_json(myMunicipios[i], myNumbers[i]))

