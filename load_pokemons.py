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
            pokemons_data = json.load(file)
            pokemons = pokemons_data.get('pokemons', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return

    with transaction.atomic():
        for pokemon_data in pokemons:
            pokemon_title_ru = pokemon_data.get('title_ru')
            if not pokemon_title_ru:
                continue

            Pokemon.objects.filter(title=pokemon_title_ru).update(
                title_en=pokemon_data.get('title_en'),
                title_jp=pokemon_data.get('title_jp'),
                description=pokemon_data.get('description')
            )


json_file_path = os.path.join('pokemon_entities', 'pokemons.json')
update_pokemons_from_json(json_file_path)