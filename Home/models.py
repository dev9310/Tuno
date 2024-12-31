from django.db import models

# Create your models here.

class SearchQuerry(models.Model):
    search = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.search)

class Song(models.Model):
    title = models.CharField(max_length=100)
    image = models.URLField()
    description = models.TextField()
    audio_source = models.URLField()
    singer = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    released_on = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now=True)        
    
    def __str__(self):
        return '{} by {}'.format(self.title, self.singer)