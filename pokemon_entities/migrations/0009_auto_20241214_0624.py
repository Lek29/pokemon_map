# Generated by Django 3.1.14 on 2024-12-13 22:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0008_auto_20241213_1639'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pokemon',
            old_name='privious_evolution',
            new_name='previous_evolution',
        ),
    ]
