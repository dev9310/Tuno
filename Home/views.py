from django.shortcuts import render , HttpResponse
from utils.helper import  SongExtractor
import pandas as pd

from Home.models import Song , SearchQuerry
# Create your views here.


def Home(request):
    return render(request , 'Home/home.html')


def Search(request):
    
    
        
    se = SongExtractor()
    query = request.POST.get('search_query', '')  
    data = se.get_search_result(query)
    
    # Save the search query 
    saveQuerry = SearchQuerry.objects.create(search=query)
    saveQuerry.save()
    

    if not data:
        return render(request, 'Errors/SongNotFound.html')

    for i in data:
        
        # Check if a song with the same details already exists
        # print(i['title'])
        exists = Song.objects.filter(
            title=i['title'],
            image=i['image'],
            description=i['description'],
            audio_source=i['audio_source'],
            singer=i['singer'],
            duration=i['duration'],
            released_on=i['released_on']
        ).exists()

        if not exists:
            # Create and save the song only if it doesn't exist
            song = Song.objects.create(
                title=i['title'],
                image=i['image'],
                description=i['description'],
                audio_source=i['audio_source'],
                singer=i['singer'],
                duration=i['duration'],
                released_on=i['released_on']
            )
            print(f"Saved song: {song}")
        else:
            print(f"Duplicate song found, not saving: {i['title']}")

    params = {'data': data}
    return render(request, 'Home/search.html', params)
