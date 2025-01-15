from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Song, Singer

@receiver(post_save, sender=Song)
def add_singers(sender, instance, created, **kwargs):
    if created:
        singer_names = instance.singer.split(",")
        for name in map(str.strip, singer_names):
            if name:
                singer, created = Singer.objects.get_or_create(name=name)
                
                # Increment the song count for the singer
                singer.song_count += 1
                singer.save()  # Save the updated singer object

@receiver(pre_delete, sender=Song)
def deduct_songs(sender, instance, **kwargs):
    singer_names = instance.singer.split(",")
    for name in map(str.strip, singer_names):
        if name:
            try:
                singer = Singer.objects.get(name=name)
                if singer.song_count > 0:
                    singer.song_count -= 1  # Decrease song count
                    singer.save()  # Save the updated singer object
            except Singer.DoesNotExist:
                pass  # Handle the case where the singer doesn't exist
