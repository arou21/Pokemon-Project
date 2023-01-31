from pip._vendor import requests
import json

def get_pokemon(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    response = requests.get(url)
    result = response.json()
    ability = result['abilities'][0]['ability']['name']
    name = result['forms'][0]['name']
    base_experience = result['base_experience']
    sub_url = result['forms'][0]['url']
    sub_response = requests.get(sub_url)
    sub_result = sub_response.json()
    image = sub_result['sprites']['front_default']
    
    return name,ability, base_experience, image 
