from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    image = models.ImageField(upload_to='pokemon_images/', blank=True, null=True, verbose_name='Изображение')
    title_en = models.CharField(max_length=255, blank=True, null=True, verbose_name='Английское название') 
    title_jp = models.CharField(max_length=255, blank=True, null=True, verbose_name='Японское Название') 
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='next_evolutions',
        verbose_name='Предыдущая эволюция'
    ) 

    def __str__(self):
        return self.title
    
class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='entities', verbose_name='Покемон')
    latitude = models.FloatField(verbose_name='широта')
    longitude = models.FloatField(verbose_name='долгота')
    appeared_at = models.DateTimeField( blank=True, null=True, verbose_name='Когда появится')
    disappeared_at = models.DateTimeField( blank=True, null=True, verbose_name='Когла исчезнет')

    level = models.IntegerField(default=1, verbose_name='Уровень')
    helth = models.IntegerField(blank=True, null=True, verbose_name='Количество жизни')
    strength = models.IntegerField(blank=True, null=True, verbose_name='Сила')
    defence = models.IntegerField(blank=True, null=True, verbose_name='Защита')
    stamina = models.IntegerField(blank=True, null=True, verbose_name='Выносливость')

    def __str__(self):
        return f'{self.pokemon.title} at {self.latitude}, {self.longitude}'
    

    


