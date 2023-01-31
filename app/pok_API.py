from pip._vendor import requests
import random
from .models import Pokemon_table

def get_pokemon(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()
        ability = result['abilities'][0]['ability']['name']
        name = result['forms'][0]['name']
        base_experience = result['base_experience']
        sub_url = result['forms'][0]['url']
        sub_response = requests.get(sub_url)
        sub_result = sub_response.json()
        image = sub_result['sprites']['front_default']
        
        return name,ability, base_experience, image 
    return False

def get_battle_points(pokemon_team):
    # Calculate points given a pokemon team using base experience
    points = 0
    for p in pokemon_team:
        pokemon = Pokemon_table.query.filter_by(name=p.pokemon_type).first()
        points += pokemon.base_experince + random.randrange(0, pokemon.base_experince)
    return points
