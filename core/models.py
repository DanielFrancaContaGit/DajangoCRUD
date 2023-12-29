from django.db import models

# Create your models here.

class Cliente(models.Model):
    objects = models.Manager
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return f'Nome do Cliente: {self.name} Cliente amial: {self.email}'
    
    