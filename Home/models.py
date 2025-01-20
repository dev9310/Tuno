from django.db import models

# Create your models here.

class SearchQuerry(models.Model):
    search = models.CharField(max_length=3x00)
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
    
    

class Singer(models.Model):
    name = models.CharField(max_length=100)
    # image = models.URLField()
    # description = models.TextField()
    # number_of_songs = models.IntegerField()
    image = models.ImageField(upload_to='singer_images/', default='singer_images/default.png')  # ImageField with default

    created = models.DateTimeField(auto_now=True)
    song_count = models.PositiveIntegerField(default=0)  # Field to store the number of songs

    def __str__(self):
        return '{}'.format(self.name)
    

# Function to extract unique singer names
def extract_all_singers(singers):
    """
    Splits a comma-separated string of singers and returns unique names.
    """
    return (
        singers.split(",")  # Split by comma
        if singers else []  # Handle empty cases
    )
    
