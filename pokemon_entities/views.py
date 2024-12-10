import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon
from .models import PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
        pokemons = json.load(database)['pokemons']

    pokemon_coords = {}
    for pokemon in pokemons:
        pokemon_id = pokemon['pokemon_id']
        if pokemon['entities']:
            first_entities = pokemon['entities'][0]
            pokemon_coords[pokemon_id] = (first_entities['lat'], first_entities['lon'])
    
    pokemons_from_bd = Pokemon.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemons_on_page = []

    for pokemon in pokemons_from_bd:
        if pokemon.image:
            image_url = request.build_absolute_uri(pokemon.image.url)
        else:
            image_url =DEFAULT_IMAGE_URL

        coords = pokemon_coords.get(pokemon.id, 'None')

        add_pokemon(folium_map, coords[0], coords[1], image_url)

        pokemons_on_page.append(
        {'pokemon_id': pokemon.id,
        'img_url' : image_url,
        'title_ru' : pokemon.title}
        )

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
        pokemons = json.load(database)['pokemons']

    
    
    pokemon_entities = PokemonEntity.objects.filter(pokemon=pokemons)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.latitude,
            pokemon_entity.longitude,
            request.build_absolute_uri(pokemon.img_url.url)
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
