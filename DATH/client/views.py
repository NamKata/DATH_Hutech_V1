from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse, get_object_or_404
from DB.models import Usergroup, LevelUser, Formality, MangaType, User_Comic, Category, Manga, MangaCategory, Chap, Comment, Follow,  Notifical
from django.template.response import TemplateResponse
from django.http import HttpResponse, JsonResponse, Http404
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from .forms import RegisterForm, Register_Manga
from django import template
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from PIL import Image
from datetime import datetime
import os
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail, send_mass_mail 
from django.conf import settings
from django.views.generic import View
from DATH.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from datetime import date
from django.utils.dateformat import DateFormat
from django.template.loader import get_template

# import json


# register =template.Library()
# Create your views here.

#-----------------------------
def user_register(request):
    user_register = User_Comic()
    UserName = request.GET.get('UserName', None)
    Password = request.GET.get('Password', None)
    Email=request.GET.get('Email', None)
    RePass=request.GET.get('nPassword', None)
    data ={
        'is_taken':User_Comic.objects.filter(UserName = UserName).exists()
    }
    if data['is_taken']:
        data['exits']= True
    else:
        if Password == RePass:
            user_register.UserName = UserName
            user_register.Email = Email
            user_register.Password = Password
            user_register.LevelUser = LevelUser.objects.get(pk=2)
            user_register.Group = Usergroup.objects.get(pk=2)
            user_register.Birthday = '1999-01-01'
            user_register.save()
            context ={
                    'UserName':user_register.UserName,
                    'Email':user_register.Email,
                    'Id':user_register.pk,
            }
            # html_message = get_template('sendmail.html').render(context)
            to_email = Email
            mail_subject = 'Đăng ký tài khoản'
            # message = "Đăng ký tài khoản thành công : \n"+ str(request.GET.get('Email', None).encode('utf-8'))
            message = get_template('client/sendmail.html').render(context)
            send_message = EmailMessage(mail_subject, message, to=[to_email])
            send_message.content_subtype = "html"
            # send_message.attach(html_message, "text/html")
            send_message.send()
            data['success']= "oke"    
    return JsonResponse(data)




#------------------ Login
def user_login(request):
    UserName = request.GET.get('UserName', None)
    Password = request.GET.get('Password', None)
    data ={
        'Success':User_Comic.objects.filter(UserName = UserName, Password = Password).exists()
    }
    if data['Success']:
        User = User_Comic.objects.get(UserName = UserName, Password = Password, StatusEmail = True)
        if User.Group == Usergroup.objects.get(pk=2):
            request.session['User_client'] = User.id
            # request.session.expire_date(2);
            # request.session.set_expiry(15);
            data['User']=render_to_string("client/include/flogin.html",{'UserName':User})
        else:
            data['Viphamquyen']="oke"
    else:
        data['User']=render_to_string("client/include/flogin.html",{'UserName': ""})
    return JsonResponse(data,safe=False)
                
def check_session_user(request):
    if request.session.has_key('User_client'):
        User = request.session['User_client']
        data ={'Success':True}
        if data['Success']:
            User1 = User_Comic.objects.get(pk=User)
            data['User']=render_to_string("client/include/flogin.html",{'UserName':User1})
        else:
            data['User']=render_to_string("client/include/flogin.html",{'UserName':""})
    else:
        data ={'Success':False}
    return JsonResponse(data,safe=False)

def check_exists(request):
    username = request.GET.get('UserName', None)
    data = {
        'is_taken': User_Comic.objects.filter(UserName__iexact=username).exists()
    }
    return JsonResponse(data)

def check_exists_email(request):
    username = request.GET.get('Email', None)
    data = {
        'is_taken': User_Comic.objects.filter(Email__iexact=username).exists()
    }
    return JsonResponse(data)

def sendmail_quenmatkhau(request):
    Email = request.GET.get('Email', None)
    User = User_Comic.objects.get(Email__iexact = Email)
    context ={
        'UserName':User.UserName,
        'Email':User.Email,
        'Id':User.pk,
    }
    to_email = Email
    mail_subject = 'Quên mật khẩu!'
    # message = "Đăng ký tài khoản thành công : \n"+ str(request.GET.get('Email', None).encode('utf-8'))
    message = get_template('client/resetmkemail.html').render(context)
    send_message = EmailMessage(mail_subject, message, to=[to_email])
    send_message.content_subtype = "html"
    send_message.send()
    data={'success': "oke"}    
    return JsonResponse(data)
def reset_password(request, pk):
    if request.method == "POST":
        User = User_Comic.objects.get(pk =pk)
        Mk1 = request.POST['password_new']
        Mk2 = request.POST['confirm_password_new'] 
        if Mk1 == Mk2:
            User.Password = Mk1
            User.save()
            return redirect("trang-chu")
        else:
            return render(request,'client/resetmk.html',{"Eror":"oke"})
    else:
        return render(request,'client/resetmk.html')
def logout(request, pk):
    try:
        if pk == request.session['User_client']:
            del request.session['User_client']
    except:
        pass 
    return redirect('trang-chu') 

def theloaitruyen(request):
    cate = Category.objects.all().order_by("-pk");
    cate1 =cate.count();
    cate2 =cate.count()/3;
    data={
        'cate': render_to_string('client/include/category.html',{'lstcate':cate,'row':cate[6:cate1],'row1':cate[12:cate1]})
    }
    return JsonResponse(data,safe=False);

#----------------------------        

#----------------------------
def home_client(request):
    # manga= Manga.objects.all().order_by('-CreateDate')[:12]
    manga= Manga.objects.filter(StatusPost=True).all()
    # chap =Chap.objects.all()
    Data={
        'today':datetime.now(),
        'manga':manga.order_by('-CreateDate')[:12],
        'truyentranh':manga.filter(MangaType=1).order_by('-CreateDate')[:12],
        'truyenchu':manga.filter(MangaType=2).order_by('-CreateDate')[:12],
        'category':MangaCategory.objects.all(),
    }
    return render(request,'client/home.html', Data)


def truyenmoicapnhap(request):
    manga = Manga.objects.filter(StatusPost=True).all().order_by('-CreateDate') 
    page = request.GET.get('page', 1)
    paginator = Paginator(manga, 8)
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
    manga = Manga.objects.filter(StatusPost=True).filter(MangaType=1).order_by('-CreateDate')
    page = request.GET.get('page', 1)
    paginator = Paginator(manga, 8)
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
    manga = Manga.objects.filter(StatusPost=True).filter(MangaType=2).order_by('-CreateDate')
    page = request.GET.get('page', 1)
    paginator = Paginator(manga, 8)
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

# def manga(request, Manga_id):
#     #select_related()
#     manga = Chap.objects.filter(Manga=Manga_id).order_by('-CreateDate')
#     Data = {
#         'manga':manga,
#         'manga_chap':Manga.objects.get(id=Manga_id),
#         'category':MangaCategory.objects.all(),
#         'cungloai':MangaCategory.objects.all()[:10],
#     }
#     return TemplateResponse(request, 'client/manga.html', Data )
#---------------------------------------------
def manga_truyentranh(request, Slug):
    #select_related()
    if Manga.objects.filter(Slug=Slug).exists():
        manga = Manga.objects.get(Slug=Slug)
        chap = Chap.objects.filter(Manga=manga).order_by('-CreateDate')
        # if request.session.has_key('User_client'):
        #     User = request.session['User_client']
        #     useUser = User_Comic.objects.get(pk=User)
        #     # follow = Follow.objects.filter(Manga = manga, User_Comic = useUser)
        # else:
        #     useUser =''
        if request.session.get('User_client'):
            users= User_Comic.objects.get(pk=request.session['User_client']) 
            try :
                # if Follow.objects.filter(Manga = manga).get(User_Comic =users).exists():
                follow = Follow.objects.filter(Manga = manga).get(User_Comic =users)
            except Follow.DoesNotExist:
                follow = []
        else:
            follow = []  
        Data = {
            'manga':manga,
            'chap':chap,
            'chapfirst':Chap.objects.filter(Manga=manga).first(),
            # 'manga_chap':Manga.objects.get(id=Manga_id),
            # 'user':useUser,
            'follow':follow,
            'category': MangaCategory.objects.all(),
            'cungloai': MangaCategory.objects.all()[:10],
        }
        return TemplateResponse(request, 'client/truyentranh/truyentranh.html', Data )
    else:
        return HttpResponse('404')
def manga_truyenchu(request, Slug):
    #select_related()
    if Manga.objects.filter(Slug=Slug).exists():
        manga = Manga.objects.get(Slug=Slug)
        chap = Chap.objects.filter(Manga=manga).order_by('-CreateDate')
        if request.session.get('User_client'):
            users= User_Comic.objects.get(pk=request.session['User_client']) 
            try :
                # if Follow.objects.filter(Manga = manga).get(User_Comic =users).exists():
                follow = Follow.objects.filter(Manga = manga).get(User_Comic =users)
            except Follow.DoesNotExist:
                follow = []
        else:
             follow = []  
        Data = { 
            'manga':manga,
            'chap':chap,
            'chapfirst':Chap.objects.filter(Manga=manga).first(),
            'follow':follow,
            # 'manga_chap':Manga.objects.get(id=Manga_id),
            'category':MangaCategory.objects.all(),
            'cungloai':MangaCategory.objects.all()[:10],
        }
        return TemplateResponse(request, 'client/truyentranh/truyenchu.html', Data )
    else:
        raise Http404

# def chap(request, id):
#     chap = Chap.objects.get(id=id)
#     Data={
#         'chap':chap,
#         'listchap':Chap.objects.all().order_by('-SttChap'),
#     }
#     return render(request,'client/chap.html', Data)
def chap_truyentranh(request, Slug, SttChap):
    if Manga.objects.filter(Slug=Slug).exists():
        manga = Manga.objects.get(Slug=Slug)
        if Chap.objects.filter(Manga=manga, SttChap =SttChap).exists():
            chap = Chap.objects.get(Manga=manga, SttChap =SttChap)
            chap1 = Chap.objects.get(Manga=manga, SttChap =SttChap)
            chap1.Views =chap1.Views+1
            chap1.save()
            # if request.session.has_key('User_client'):
            #     User = request.session['User_client']
            #     useUser = User_Comic.objects.get(pk=User)
            # else:
            #     useUser =''
            # user = request.session['User_client'];
            if not request.session.get('User_client'):
                users = None
            else:
                users= User_Comic.objects.get(pk=request.session['User_client'])
            Data={
                'chap':chap,
                'user':users,
                'comment': Comment.objects.filter(Chap = chap).order_by("-CreateDate"),
                'listchap':Chap.objects.all().order_by('-SttChap'),
            }
            return render(request,'client/chap/truyentranh.html', Data)
        else:
            return HttpResponse('404')
    else:
        return HttpResponse('404')
def chap_truyenchu(request, Slug, SttChap):
    if Manga.objects.filter(Slug=Slug).exists():
        manga = Manga.objects.get(Slug=Slug)
        if Chap.objects.filter(Manga=manga, SttChap =SttChap).exists():
            chap = Chap.objects.get(Manga=manga, SttChap =SttChap)
            chap1 = Chap.objects.get(Manga=manga, SttChap =SttChap)
            chap1.Views =chap1.Views+1
            chap1.save()
            if not request.session.get('User_client'):
                users = None
            else:
                users= User_Comic.objects.get(pk=request.session['User_client'])
            Data={
                'chap':chap,
                'user':users,
                'comment': Comment.objects.filter(Chap = chap).order_by("-CreateDate"),
                'listchap':Chap.objects.all().order_by('-SttChap'),
            }
            return render(request,'client/chap/truyenchu.html', Data)
        else:
            raise Http404
    else:
        raise Http404

# def chap_chu(request, id):
#     chap = Chap.objects.get(id=id)
#     Data={
#         'chap':chap,
#         'listchap':Chap.objects.all(),
#     }
#     return render(request,'client/chapchu.html',Data)

def info(request, pk):
    if pk == request.session['User_client']:
        if request.method == "POST":
            User = User_Comic.objects.get(pk=pk)
            # UserName = request.POST['UserName']
            # Email = request.POST['Email']
            Password = request.POST['Password']
            NickName =request.POST['NickName']
            Birthday =request.POST['Birthday']
            Phone =request.POST['Phone']
            Address =request.POST['Address']
            Gender = request.POST['gender']
            Content = request.POST['Content']
            if bool(request.FILES.get('Image', False)) == True:
                Image = request.FILES['Image']
                if Password == User.Password:
                    # User.UserName = UserName
                # User.Email = Email
                    User.Password = Password
                    User.NickName = NickName
                    User.Birthday = Birthday
                    User.Phone = Phone
                    User.Address = Address
                    if Gender == '1':
                        User.StatusGender =True
                    else:
                        User.StatusGender =False
                    User.Content = Content
                    if Image != '':
                        User.Image = Image
                    User.save()
                    return render(request,'client/info.html', {"user":User,"success":"ok"})
                else:
                    return render(request,'client/info.html', {"user":User,"errorpass":"oke"})
            else:
                if Password == User.Password:
                    User.Password = Password
                    User.NickName = NickName
                    User.Birthday = Birthday
                    User.Phone = Phone
                    User.Address = Address
                    if Gender == '1':
                        User.StatusGender =True
                    else:
                        User.StatusGender =False
                    User.Content = Content
                    User.save()
                    return render(request,'client/info.html', {"user":User,"success":"ok"})
                else:
                    return render(request,'client/info.html', {"user":User,"errorpass":"oke"})           
        else:
            User = User_Comic.objects.get(pk=pk)
            return render(request,'client/info.html', {"user":User})
    else:
        raise Http404
def doimatkhau(request, pk):
    if pk == request.session['User_client']:
        if request.method == "POST":
            User = User_Comic.objects.get(pk=pk)
            Password_old = request.POST['password_old']
            Passwrod_new = request.POST['password_new']
            Cofirm_Pass = request.POST['confirm_password_new']
            if User.Password == Password_old:
                if Passwrod_new == Cofirm_Pass:
                    User.Password = Passwrod_new
                    User.save()
                    return render(request, 'client/doimatkhau.html',{"user":User,'success':'oke'})
                else:
                    return render(request, 'client/doimatkhau.html',{"user":User,'errorcomfirmpass':'oke'})
            else:
                return render(request, 'client/doimatkhau.html',{"user":User,'errorpassold':'oke'})
        else:
            User = User_Comic.objects.get(pk=pk)
            return render(request, 'client/doimatkhau.html',{"user":User})
    else:
        raise Http404

def message(request):
    return render(request,'client/message.html')

def send_messgae(request):
    return render(request,'client/send.html')

def follow_comic(request, pk):
    manga_follow = Follow.objects.filter(User_Comic_id = pk)
    Data={
        'manga':manga_follow ,
        'category':MangaCategory.objects.all(),
    }
    return render(request,'client/truyentheodoi.html', Data)

def dangkytruyen(request):
    manga = Manga();
    if request.method == "POST":
        upload_file = request.FILES['Image']
        if upload_file == None:
            return HttpResponse("chưa chọn ảnh")
        else:    
            fs =FileSystemStorage()
            name = fs.save("Manga/ "+ upload_file.name, upload_file)
            url =fs.url(name)
        print(url)
        manga.MangaName = request.POST['MangaName']
        manga.OrtherName = request.POST['OrtherName']
        manga.Slug = request.POST['Slug']
        manga.Image = name
        manga.Content = request.POST['Content']
        manga.Author= request.POST['Author']
        manga.Editor = request.POST['Editor']
        manga.StartDate = datetime.now()
        manga.EndDate = datetime.now()
        User = request.session['User_client']
        maUser = User_Comic.objects.get(pk = User)
        manga.User_Comic = maUser
        theloai = request.POST['Formality']
        nhomtruyen = request.POST['MangaType']
        manga.Formality =Formality.objects.get(pk=int(theloai))
        manga.MangaType = MangaType.objects.get(pk =int(nhomtruyen))
        if request.POST['MangaName'] == None or request.POST['Slug'] == None :
            return render(request,'client/dangkitruyen.html')
        else:
            manga.save()
            for item in request.POST.getlist('Category[]'):
                cateman = MangaCategory();
                cateman.Manga = manga
                cateman.Category = Category.objects.get(pk=int(item))
                cateman.DeleteDate =datetime.now()
                cateman.save()
            return redirect('tu-truyen', pk = maUser.pk )
    else:
        cate = Category.objects.exclude(id__in=[19,20,21]).order_by('pk')
        return render(request,'client/dangkitruyen.html',{'cate':cate})

def danhsachchuong(request, pk):
    manga = Manga.objects.get(pk=pk)
    cate = MangaCategory.objects.all()
    chap = Chap.objects.filter(Manga = manga, StatusPost = True).order_by('SttChap')
    Data ={
        'manga':manga,
        'cate':cate,
        'chap':chap
    }
    return render(request,'client/danhsachchuong.html',Data)

def tutruyen(request, pk):
    if pk == request.session['User_client']:
        user = User_Comic.objects.get(pk=pk)
        manga = Manga.objects.filter(User_Comic_id= pk)
        Data={
            'manga':manga ,
            'category':MangaCategory.objects.all(),
        }
        return render(request,'client/tutruyen.html',Data)
    else:
        raise Http404
def chitiettruyen(request,pk):
    manga = Manga.objects.get(pk=pk)
    if request.method == 'POST':
        MangaName = request.POST['MangaName']
        OrtherName = request.POST['OrtherName']
        Slug = request.POST['Slug']
        Content = request.POST['Content']
        Author= request.POST['Author']
        Editor = request.POST['Editor']
        theloai = request.POST['Formality']
        nhomtruyen = request.POST['MangaType']
        if bool(request.FILES.get('Image', False)) == True:
            Image =request.FILES['Image']
            if Image != '':
                manga.Image = Image
            manga.MangaName = MangaName
            manga.OrtherName = OrtherName
            manga.Slug = Slug
            manga.Content = Content
            manga.Author = Author
            manga.Editor = Editor
            manga.Formality =Formality.objects.get(pk=int(theloai))
            manga.MangaType = MangaType.objects.get(pk =int(nhomtruyen))
            manga.save()
        else:
            manga.MangaName = MangaName
            manga.OrtherName = OrtherName
            manga.Slug = Slug
            manga.Content = Content
            manga.Author = Author
            manga.Editor = Editor
            manga.Formality =Formality.objects.get(pk=int(theloai))
            manga.MangaType = MangaType.objects.get(pk =int(nhomtruyen))
            manga.save()
        # if request.POST.getlist('MangaCategory[]') != 'on':
        #     # nếu ko  checked thì loại
        #     for item  in request.POST.getlist('MangaCategory[]',''): 
        #         print("Thể loại hiện tai:"+item)
        #         cate = Category.objects.get(pk = int(item))
        #         delcateman = MangaCategory.objects.get(Manga=manga, Category=cate)
        #         delcateman.delete()  
        # else:
        #     # checked thì xử lý
        #     pass
        layidclick= MangaCategory.objects.exclude(Category_id__in = request.POST.getlist('MangaCategory[]')).filter(Manga =manga).distinct()
        if layidclick:
           layidclick.delete()
        else:
            pass 
        print(layidclick)
        for item1 in request.POST.getlist('Category[]'):
            print("Nhưng danh mục được click:"+ item1)
            cateman = MangaCategory()
            cateman.Manga = manga
            cateman.Category = Category.objects.get(pk=int(item1))
            cateman.DeleteDate =datetime.now()
            cateman.save()
        
            
        mancate = MangaCategory.objects.select_related('Category').filter(Manga =manga).distinct() 
        cate = Category.objects.exclude(id__in= MangaCategory.objects.select_related('Category').values_list('Category', flat=True ).filter(Manga =manga).distinct()).exclude(id__in=[19,20,21]) 
        Data ={
            'manga':manga,
            'cate':cate,
            'mancate':mancate,
            'success':'oke'
        }
        return render(request,'client/chitiettruyen.html',Data)
    else:    
        mancate = MangaCategory.objects.select_related('Category').filter(Manga =manga).distinct()
        cate = Category.objects.exclude(id__in= MangaCategory.objects.select_related('Category').values_list('Category', flat=True ).filter(Manga =manga).distinct()).exclude(id__in=[19,20,21]) 
        Data ={
            'manga':manga,
            'cate':cate,
            'mancate':mancate
        }
        return render(request,'client/chitiettruyen.html',Data)
def themchuong(request, pk):
    if request.method == "POST":
        manga = Manga.objects.get(pk=pk)
        chap = Chap()
        SttChap = request.POST['SttChap']
        Title = request.POST['Title']
        Content = request.POST['Content']
        DateUp = request.POST['DateUp']
        chap.SttChap = SttChap
        chap.Title = Title
        chap.Content =Content
        chap.DateUp = DateUp
        chap.DateEdit =DateUp
        chap.StatusPost =True
        chap.Manga =manga
        chap.save()
        manga.Chapnow=chap.SttChap
        manga.DateUpChap=chap.DateUp
        manga.save()
        return redirect('tu-truyen',pk=manga.User_Comic.pk)
    else:
        if Chap.objects.filter(Manga_id = pk).exists():
            sttchap= Chap.objects.filter(Manga_id=pk).last()
            valstt = sttchap.SttChap + 1
            Data ={
                'sttchap':valstt,
                'truyen':Manga.objects.get(pk=pk)
            }
            return render(request,'client/themchuong.html',Data)
        else:
            Data ={
                'sttchap':1,
                'truyen':Manga.objects.get(pk=pk)
            }
            return render(request,'client/themchuong.html',Data)
def editchuong(request, pk):
    chap = Chap.objects.get(pk =pk)
    if request.method == "POST":
        Content = request.POST['Content']
        DateUp = request.POST['DateUp']
        chap.Content =Content
        chap.DateUp = DateUp
        chap.DateEdit =datetime.now()
        chap.save()
        manga = Manga.objects.get(pk=chap.Manga.pk)
        manga.DateUpChap=chap.DateEdit
        manga.save()
        return redirect('danh-sach-chuong',pk = chap.Manga.pk)
    else:
        return render(request,'client/editchuong.html',{'chap':chap})
def xoachuong(request, pk):
    chap = Chap.objects.get(pk =pk)
    chap.StatusPost = False
    chap.save()
    return redirect('danh-sach-chuong',pk = chap.Manga.pk)
def send_dangkytruyen(request):
    manga = Manga()
    # if request.method == "POST":
    MangaName = request.GET.get('MangaName','None')
    OrtherName = request.GET.get('OrtherName','None')
    Slug = request.GET.get('Slug','None')
    Image = request.GET.get('Image','None')
    Content = request.GET.get('Content','None')
    Author = request.GET.get('Author','None')
    Editor = request.GET.get('Editor','None')
    StartDate = request.GET.get('StartDate','None')
    manga.MangaName = MangaName
    manga.OrtherName = OrtherName
    manga.Slug = Slug
    manga.Image = os.path.join(Image)
    manga.Content = Content
    manga.Author= Author
    manga.Editor = Editor
    manga.StartDate = datetime.now()
    manga.EndDate = datetime.now()
    User = request.session['User_client']
    maUser = User_Comic.objects.get(pk = User)
    manga.User_Comic = maUser
    manga.Formality = Formality.objects.get(pk=2)
    manga.MangaType = MangaType.objects.get(pk = 2)
    # f = Image.open(Image)
    # manga.Image =f;
    manga.save()
    # fs = FileSystemStorage()
    # name = fs.save("Manga/ "+ os.path.join(Image), os.path.join(Image))
    # url =fs.url(name)
    print(os.path.join(Image))
    data={
                'Success':'True',
        }
    return JsonResponse(data)

#------------------------------
def NextChap(request):
    SttChap = request.GET.get("SttChap",None)
    Mangapk = request.GET.get("MangaId",None)
    man = Manga.objects.get(pk = Mangapk)
    data ={
        'Success':Chap.objects.filter(SttChap = SttChap, Manga = man).exists()
    }
    if data['Success']:
        chap = Chap.objects.get(SttChap = SttChap, Manga = man)
        if chap.last():
            data['SttChap']=chap.SttChap
        else:
            data['SttChap'] = chap.SttChap+1  
    return JsonResponse(data,safe=False)

def theloai(request, pk ):
    cate = Category.objects.get(pk=pk)
    manga = MangaCategory.objects.filter(Category_id=pk).distinct()
    print(manga)
    page = request.GET.get('page', 1)
    paginator = Paginator(manga, 8)
    try:
        lstmanga= paginator.page(page)
    except PageNotAnInteger:
        lstmanga = paginator.page(1)
    except EmptyPage:
        lstmanga = paginator.page(paginator.num_pages)
    
    Data ={
        'checkcate':cate,
        'manga':lstmanga,
        'chap':Chap.objects.all(),
        'category':MangaCategory.objects.all(),
        'theloai':Category.objects.exclude(id__in=[19,20,21]).all()
    }
    return render(request, 'client/theloaitruyen.html', Data)

def share(request, pk):
    manga = Manga.objects.get(pk=pk);
    manga.Share = manga.Share + 1;
    manga.save()
    data={
        'success':'ok'
    }
    return JsonResponse(data)
def search(request):
    if request.method == 'GET':
        search_text= request.GET.get('search', None)
        if search_text is not None and search_text != u"":
            search_text = request.GET['search']
            statuss = Manga.objects.filter(MangaName__contains = search_text).filter(StatusPost=True)
        else:
            statuss = []
        Data={
            'manga':statuss ,
            'category':MangaCategory.objects.all(),
        }
        return render(request, "client/search.html",Data)

def binhluan(request, pk):
    chap = Chap.objects.get(pk=pk);
    taikhoan = request.GET.get("UserName", None);
    email = request.GET.get("Email", None);
    content = request.GET.get("Content", None);
    user = User_Comic()
    comment = Comment()
    if not request.session.get('User_client'):
        user.UserName = taikhoan
        user.Email  = email
        user.LevelUser = LevelUser.objects.get(pk=2)
        user.Group = Usergroup.objects.get(pk=3)
        user.Birthday = '1999-01-01'
        user.save()
        comment.Content=content
        comment.User_Comic = user
        comment.Chap =chap
        comment.Rating = 0
        comment.save()
        data = {
            'success':'oke'
        }
    else:
        users= User_Comic.objects.get(pk=request.session['User_client'])
        comment.Content=content
        comment.User_Comic = users
        comment.Chap =chap
        comment.Rating = 0 
        comment.save()
        data = {
            'success':'oke'
        }
    return JsonResponse(data)
def search_autocomplete(request):
    search_text = request.GET.get('search_text', None)
    if search_text is not None and search_text != u"":
            search_text = request.GET['search_text']
            statuss = Manga.objects.filter(MangaName__contains = search_text).filter(StatusPost=True)
    else:
            statuss = []
    data={
        'statuss': render_to_string("client/include/timkiem.html",{'statuss':statuss}),
    }
    return JsonResponse(data,safe=False); 

def tatkichhoat(request, Matruyen ):
    # Matruyen = request.Get.get('Matruyen', None)
    # if pk is not None and pk != u"":
       
    # else:
    #     Data = {
    #         'error':'oke'
    #     }
    manga = Manga.objects.get(pk = Matruyen)
    manga.StatusPost = False
    manga.save()
    data = {
        'success':'oke'
    }
    return JsonResponse( data, safe=False)
def theodoitruyen(request, Matruyen):
    if not request.session.get('User_client'):
        data = {
            'dangnhap':'oke'
        }
    else:
        users= User_Comic.objects.get(pk=request.session['User_client'])
        try:
            follow = Follow.objects.filter(Manga_id = Matruyen).get(User_Comic =users)
            if follow.StatusFollow == True:
                follow.StatusFollow= False
            else:
                follow.StatusFollow= True
            follow.save()
        except Follow.DoesNotExist :
            thedoi = Follow()
            thedoi.Manga = Manga.objects.get(pk = Matruyen)
            thedoi.User_Comic =users
            thedoi.StatusFollow =True
            thedoi.DateUnfollow = datetime.now()
            thedoi.save()
        data = {
            'succes':'oke'
        }
    return JsonResponse(data, safe=False)
