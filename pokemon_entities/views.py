import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
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
    current_time = timezone.localtime()

  
    active_pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lte=current_time,
        disappeared_at__gt=current_time
    ).select_related('pokemon')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemons_on_page = []
    for pokemon_entity in active_pokemon_entities:
        pokemon = pokemon_entity.pokemon
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url) if pokemon.image else DEFAULT_IMAGE_URL,
            'title_ru': pokemon.title,
        })

        add_pokemon(
                folium_map,
                pokemon_entity.latitude,
                pokemon_entity.longitude,
                request.build_absolute_uri(pokemon.image.url) if pokemon.image else DEFAULT_IMAGE_URL
            )
    
    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })

def show_pokemon(request, pokemon_id):
    current_time = timezone.localtime()

    pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    active_pokemon_entities = pokemon.pokemonentity_set.filter(
        appeared_at__lte=current_time,
        disappeared_at__gt=current_time
    )

    

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in active_pokemon_entities:
        image_url = request.build_absolute_uri(pokemon.image.url) if pokemon.image else DEFAULT_IMAGE_URL
        print(f"Image URL: {image_url}")

        add_pokemon(
            folium_map,
            pokemon_entity.latitude, 
            pokemon_entity.longitude, 
            image_url
        )

    evolution = {}

    if pokemon.privious_evolution:
        evolution['previous'] ={
            'title_ru': pokemon.previous_evolution.title,
            'pokemon_id': pokemon.privious_evolution.id,
            'img_url' : request.build_absolute_uri(pokemon.privious_evolution.image.url) if
            pokemon.privious_evolution.image else DEFAULT_IMAGE_URL,
        }

    next_evolutions = []

    for next_evo in pokemon.next_evolutions_relation.all():
        next_evolutions.append({
            'title_ru': next_evo.title,
            'pokemon_id': next_evo.id,
            'img_url': request.build_absolute_uri(next_evo.image.url) if next_evo.image else DEFAULT_IMAGE_URL
        })

    if next_evolutions:
        evolution['next'] = next_evolutions

    pokemons_specificarions={
        'pokemon_id': pokemon.id,
        'image_url' : request.build_absolute_uri(pokemon.image.url) if pokemon.image else   DEFAULT_IMAGE_URL,
        'title_ru' : pokemon.title,
        'title_en' : pokemon.title_en,
        'title_jp' : pokemon.title_jp,
        'description': pokemon.description,
        'evolution': evolution
    }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemons_specificarions
    })
