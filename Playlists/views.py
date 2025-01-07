from django.shortcuts import render , HttpResponse

# Create your views here.


def Playlist(request):
    return render(request , 'Playlists/playlists.html')