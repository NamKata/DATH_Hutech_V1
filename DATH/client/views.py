from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse, get_object_or_404
from DB.models import Usergroup, LevelUser, Formality, MangaType, User_Comic, Category, Manga, MangaCategory, Chap, Comment, Follow, Rating, Vote, Notifical
from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def home_client(request):
    manga= Manga.objects.all().order_by('-CreateDate')[:10]
    Data={
        'manga':manga,
        'truyentranh':Manga.objects.filter(MangaType=1).order_by('-CreateDate')[:10],
        'truyenchu':Manga.objects.filter(MangaType=2).order_by('-CreateDate')[:10],
        'chap':Chap.objects.all(),
        'category':MangaCategory.objects.all(),
    }
    return render(request,'client/home.html', Data)

def home_login(request):
    return render(request, 'client/online.html')

def more_manga(request):
    return render(request, 'client/xemthem.html')

def truyenmoicapnhap(request):
    manga = Manga.objects.all().order_by('-CreateDate')
    page = request.GET.get('page', 1)
    paginator = Paginator(manga, 18)
    try:
        lstmanga= paginator.page(page)
    except PageNotAnInteger:
        lstmanga = paginator.page(1)
    except EmptyPage:
        lstmanga = paginator.page(paginator.num_pages)
    
    Data ={
        'manga':lstmanga,
        'chap':Chap.objects.all(),
        'category':MangaCategory.objects.all(),
        'theloai':Category.objects.all()
    }
    return render(request, 'client/danhsachtruyenmoicapnhap.html', Data)

def truyentranh(request):
    manga = Manga.objects.filter(MangaType=1).order_by('-CreateDate')
    page = request.GET.get('page', 1)
    paginator = Paginator(manga, 18)
    try:
        lstmanga= paginator.page(page)
    except PageNotAnInteger:
        lstmanga = paginator.page(1)
    except EmptyPage:
        lstmanga = paginator.page(paginator.num_pages)
    
    Data ={
        'manga':lstmanga,
        'chap':Chap.objects.all(),
        'category':MangaCategory.objects.all(),
        'theloai':Category.objects.all()
    }
    return render(request, 'client/danhsachtruyentranh.html',Data)

def truyenchu(request):
    manga = Manga.objects.filter(MangaType=2).order_by('-CreateDate')
    page = request.GET.get('page', 1)
    paginator = Paginator(manga, 18)
    try:
        lstmanga= paginator.page(page)
    except PageNotAnInteger:
        lstmanga = paginator.page(1)
    except EmptyPage:
        lstmanga = paginator.page(paginator.num_pages)
    
    Data ={
        'manga':lstmanga,
        'chap':Chap.objects.all(),
        'category':MangaCategory.objects.all(),
        'theloai':Category.objects.all()
    }
    return render(request, 'client/danhsachtruyenchu.html', Data)

def manga(request, Manga_id):
    #select_related()
    manga = Chap.objects.filter(Manga=Manga_id).order_by('-CreateDate')
    Data = {
        'manga':manga,
        'manga_chap':Manga.objects.get(id=Manga_id),
        'category':MangaCategory.objects.all(),
        'cungloai':MangaCategory.objects.all()[:10],
    }
    return TemplateResponse(request, 'client/manga.html', Data )

def chap(request, id):
    chap = Chap.objects.get(id=id)
    Data={
        'chap':chap,
        'listchap':Chap.objects.all(),
    }
    return render(request,'client/chap.html', Data)

def chap_chu(request, id):
    chap = Chap.objects.get(id=id)
    Data={
        'chap':chap,
        'listchap':Chap.objects.all(),
    }
    return render(request,'client/chapchu.html',Data)

def info(request):
    return render(request,'client/info.html')

def message(request):
    return render(request,'client/message.html')

def send_messgae(request):
    return render(request,'client/send.html')



    
