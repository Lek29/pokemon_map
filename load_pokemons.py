import os
import json
from django.db import transaction

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pogomap.settings')
import django

django.setup()
from pokemon_entities.models import Pokemon


def update_pokemons_from_json(json_file_path: str) -> None:
    """Обновляет информацию о покемонах в базе данных на основе данных из JSON файла.

    Args:
        json_file_path: Путь к JSON файлу, содержащему данные о покемонах.

    Raises:
        FileNotFoundError: Если JSON файл не найден.
        json.JSONDecodeError: Если JSON файл не может быть декодирован.
    """
    try:
        with open(json_file_path, encoding='utf-8') as file:
            file_content = json.load(file)
            pokemons_info = file_content.get('pokemons', [])
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: File not found or invalid JSON")
        return

    with transaction.atomic():
        for pokemon_info in pokemons_info:
            pokemon_title_ru = pokemon_info.get('title_ru')
           
            if not pokemon_title_ru:
                print(f"Warning: Skipping pokemon, no `title_ru` {pokemon_info.get('title_en')}")
                continue

            pokemon, created = Pokemon.objects.get_or_create(
                title=pokemon_title_ru,
                defaults={
                    'title_en': pokemon_info.get('title_en'),
                    'title_jp': pokemon_info.get('title_jp'),
                    'description': pokemon_info.get('description')
                }
            )
            if not created:
                 pokemon.title_en = pokemon_info.get('title_en')
                 pokemon.title_jp = pokemon_info.get('title_jp')
                 pokemon.description = pokemon_info.get('description')
                 

            previous_evolution_info = pokemon_info.get('previous_evolution')
            if previous_evolution_info:
                previous_pokemon_title_ru = previous_evolution_info.get('title_ru')
                if previous_pokemon_title_ru:
                    try:
                         previous_pokemon = Pokemon.objects.get(title=previous_pokemon_title_ru)
                         pokemon.privious_evolution = previous_pokemon
                         
                    except Pokemon.DoesNotExist:
                        print(f"Error: Previous Pokemon with title {previous_pokemon_title_ru} does not exist.")
            pokemon.save()
json_file_path = os.path.join('pokemon_entities', 'pokemons.json')
update_pokemons_from_json(json_file_path)