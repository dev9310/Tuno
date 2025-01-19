from django.shortcuts import render , HttpResponse
from utils.helper import DBManager , get_supabase_client    




# Create your views here.

def Artists(request):
    supabase = get_supabase_client()
    response= supabase.table("Home_singer").select("*").order("song_count", desc=True).limit(10).execute()
    artist_list= response.data
    for i in artist_list:
        print(i.get('name') , i.get('image') ,'  ', i.get("song_count"))
    
    params = {"artist_list" : artist_list}
    
    return render(request , 'Artists/artists.html' , params)