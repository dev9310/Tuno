from django.shortcuts import render , HttpResponse
from utils.helper import  SongExtractor
from utils.scrapper import SearchResult
from Home.models import Song , SearchQuerry , Singer
# Create your views here.


def SupaManager( query, data):

    # Save the search query 
    saveQuerry = SearchQuerry.objects.create(search=query)
    saveQuerry.save()
    
    singers = Singer.objects.all()
    print(singers)    

    for i in data:
        
        
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

    return data
    
def scrapManager(request):

    sr = SearchResult()    
    query = request.POST.get('search_query', '')  
    data = [] 

    for i in sr.google_custom_search(query):
        data.append(i)

    if not data:
        return render(request, 'Errors/SongNotFound.html')
    
    return query , data
    

    


def Home(request):
    return render(request , 'Home/home.html')

def Search(request):

    
    query, data = scrapManager(request)    
    data  = SupaManager(query, data)    
    
    params = {'data': data}
    return render(request, 'Home/search.html', params)
