from django.shortcuts import render, HttpResponseRedirect, redirect
from DB.models import Usergroup, LevelUser, Formality, MangaType, User_Comic, Category, Manga, MangaCategory, Chap, Comment, Follow, Rating, Vote, Notifical
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def home_master(request):
    return render(request,'master/home.html')

#############################
def table_user_group(request):
    data = Usergroup.objects.all().order_by('-CreateDate')
    return render(request, 'master/table_user_group.html', {'data':data})

#############################
def table_level_user(request):
    data = LevelUser.objects.all().order_by('id')
    return render(request,'master/table_level_user.html',{'data':data})

#############################
def table_formality(request):
    data = Formality.objects.all().order_by('id')
    return render(request, 'master/table_formality.html', {'data':data})

#############################
def table_user(request):
    data = User_Comic.objects.filter(Group = 2).order_by('-CreateDate')
    return render(request, 'master/table_user.html', {'data':data})

#############################
def table_manga_type(request):
    data = MangaType.objects.all().order_by('id')
    return render(request, 'master/table_manga_type.html', {'data':data})

#############################
def table_category(request):
    data = Category.objects.all().order_by('id')
    return render(request, 'master/table_category.html', {'data':data})

#############################
def table_manga(request):
    data = Manga.objects.all().order_by('MangaName')
    return render(request, 'master/table_manga.html', {'data':data})

#############################
def table_manga_category(request):
    manga = Manga.objects.all().order_by('MangaName')
    data = MangaCategory.objects.all().order_by('Manga')
    Data={
        'data':data,
        'manga':manga,
    }
    return render(request, 'master/table_manga_category.html', Data)

#############################
def table_chap(request):
    manga = Manga.objects.all().order_by('MangaName')
    data = Chap.objects.all()
    Data={
        'manga':manga,
        'data':data
    }
    return render(request, 'master/table_chap.html', Data)

#############################
def table_comment(request):
    return render(request, 'master/table.html')

#############################
def table_rate(request):
    return render(request, 'master/table.html')

#############################
def table_vote(request):
    return render(request, 'master/table.html')

#############################
def table_notifical(request):
    return render(request, 'master/table.html')
