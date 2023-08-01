from django.db import models

# Create your models here.


class Recipe(models.Model):
    name = models.CharField(max_length=120)
    cooking_time = models.FloatField(help_text='in minutes')
    ingredients = models.CharField(
        max_length=350, help_text="Input must be separated by commas exp(Eggs, Soy, Milk)")
    description = models.TextField()
    pic = None

    def __str__(self):
        return str(self.name)
