from django.db import models

# Create your models here.
class Menu(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    description = models.TextField(max_length=200)
    image = models.ImageField(upload_to='images/%y/%m/%d')

    def __str__(self):
        return self.name