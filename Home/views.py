from django.shortcuts import render , HttpResponse
from utils.helper import  SongExtracter
import pandas as pd

# Create your views here.


def Home(request):
    return render(request , 'Home/home.html')


def Search(request):
    se = SongExtracter()
        
    query = request.POST.get('search_query', '')  
    data = se.get_search_result(query)
    
    # params ={
    #     'data':data
    # }
    
    
    
    return HttpResponse("DIV")    
    # return render(request , 'Home/search.html' ,params )
