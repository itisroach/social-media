from django.shortcuts import render

# Create your views here.
def userPage(request):
    return render(request , "userPage.html")