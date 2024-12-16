# Generated by Django 3.1.14 on 2024-12-13 08:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0006_pokemon_privious_evolution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='privious_evolution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next_evolution_relation', to='pokemon_entities.pokemon'),
        ),
    ]