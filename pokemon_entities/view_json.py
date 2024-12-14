import json
from pprint import pprint

with open('pokemon_entities/pokemons.json', encoding='utf-8') as file:
    pokemons_db = json.load(file)['pokemons']

pprint(pokemons_db)

