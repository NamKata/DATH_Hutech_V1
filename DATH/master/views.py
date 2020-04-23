from django.shortcuts import render, HttpResponseRedirect, redirect

# Create your views here.
def home_master(request):
    return render(request,'master/home.html')