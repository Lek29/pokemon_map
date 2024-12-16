# Generated by Django 3.1.14 on 2024-12-13 08:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0007_auto_20241213_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='privious_evolution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next_evolutions_relation', to='pokemon_entities.pokemon'),
        ),
    ]