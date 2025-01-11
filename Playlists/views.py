from django.shortcuts import render , HttpResponse
# from utils.helper import DBManager , get_supabase_client    
# Create your views here.


def Playlist(request):
    # supabase = get_supabase_client()
    # response = supabase.table("Home_song").select("*").execute()
    # songs_list = response.data  # This will be a list of dictionaries


    
    
    
    # return render(request , 'Playlists/playlists.html', {'songs': songs_list})
    return render(request , 'Playlists/playlists.html')