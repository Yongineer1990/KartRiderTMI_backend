from django.db import models

class Character(models.model):

    name = models.CharField(max_length = 50)
    url  = models.URLField()
    key  = models.CharField(max_length = 100)
    
    class meta:
        db_table = "characters"

    def __str__(self):
        return self.name

class Kart(models.model):

    name = models.CharField(max_length = 50)
    url  = models.URLField()
    key  = models.CharField(max_length = 100)
    
    class meta:
        db_table = "karts"

    def __str__(self):
        return self.name

class Track(models.model):

    name = models.CharField(max_length = 50)
    url  = models.URLField()
    key  = models.CharField(max_length = 100)
    
    class meta:
        db_table = "tracks"

    def __str__(self):
        return self.name
