from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='pokemon_images/', blank=True, null=True)

    def __str__(self):
        return self.title
    
class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    appeared_at = models.DateTimeField( blank=True, null=True)
    disappeared_at = models.DateTimeField( blank=True, null=True)

    level = models.IntegerField(default=1)
    helth = models.IntegerField(blank=True, null=True)
    strength = models.IntegerField(blank=True, null=True)
    defence = models.IntegerField(blank=True, null=True)
    stamina = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.pokemon.title} at {self.latitude}, {self.longitude}'
    

    


