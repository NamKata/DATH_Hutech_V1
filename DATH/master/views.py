from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from DB.models import Usergroup, LevelUser, Formality, MangaType, User_Comic, Category, Manga, MangaCategory, Chap, Comment, Follow, Notifical
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import dateformat
from .forms import ChapForm, GroupForm, LevelForm, FormalityForm, UserForm, MangaTypeForm, MangaForm, CategoryForm, MangaCateForm, LoginForm
from django.template.loader import render_to_string

# Create your views here.

# def login_master(request):
#     username='Wrong username or password'
#     if request.method =='POST':
#         Username = request.POST['Username']
#         Password = request.POST['Password']
#         if Username == '' or Password == '':
#             return HttpResponse('404')
#         else:
#             user = User_Comic.objects.get(UserName = Username, Password = Password, Group = '1')
#             username = user.UserName
#             request.session['username'] = user.UserName
#             return (request,'master/index.html',{'username':user})
#             # request.session.set_expiry(15);
#             # return HttpResponseRedirect('/master/')
#     return render(request, 'login_register/login.html')
#     # return render(request, 'login_register/login.html',Data)

def home_master(request):
    # if request.session.has_key('username'):
    #     username = request.session['username']
    #     return render(request, 'master/home.html')
    # else:
    #     # myForm = LoginForm()
    # return redirect('/master/dang-nhap-he-thong')
    return render(request, 'master/home.html')

#############################


def table_user_group(request):
    data = Usergroup.objects.all().order_by('-CreateDate')
    return render(request, 'master/table_user_group.html', {'data': data})
# -> function cus -> suchas


def save_group_form(request, form, template_name):
    data = dict()
    if request.method == "POST":
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            group = Usergroup.objects.all().order_by('-CreateDate')
            data['html_book_list'] = render_to_string('master/list/group.html', {
                'data': group
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(
        template_name, context, request=request)
    return JsonResponse(data)
# -> add


def table_group_add(request):
    if request.method == "POST":
        form = GroupForm(request.POST)
    else:
        form = GroupForm()
    return save_group_form(request, form, 'master/add/addgroup.html')
# ->edit


def table_group_edit(request, pk):
    group = get_object_or_404(Usergroup, pk=pk)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
    else:
        form = GroupForm(instance=group)
    return save_group_form(request, form, 'master/edit/editgroup.html')
# ->delete


def table_group_delete(request, pk):
    group = get_object_or_404(Usergroup, pk=pk)
    data = dict()
    if pk == int(1) or pk == int(2) or pk == int(3):
        data['trangchu'] = True
    else:
        if request.method == 'POST':
            group.delete()
            # This is just to play along with the existing code
            data['form_is_valid'] = True
            groups = Usergroup.objects.all().order_by('-CreateDate')
            data['html_book_list'] = render_to_string('master/list/group.html', {
                'data': groups
            })
        else:
            context = {'group': group}
            data['html_form'] = render_to_string('master/delete/deletegroup.html',
                                                 context,
                                                 request=request,
                                                 )
    return JsonResponse(data)

#############################


def table_level_user(request):
    data = LevelUser.objects.all().order_by('id')
    return render(request, 'master/table_level_user.html', {'data': data})

# ->save ->suchas


def save_level_form(request, form, template_name):
    data = dict()
    if request.method == "POST":
        if form.is_valid():
            form.save()
            data['request'] = True
            level = LevelUser.objects.all().order_by('id')
            data['list'] = render_to_string('master/list/level.html', {
                'data': level
            })
        else:
            data['request'] = False
    context = {'form': form}
    data['modal_form'] = render_to_string(
        template_name, context, request=request)
    return JsonResponse(data)
# ->add


def table_level_add(request):
    if request.method == "POST":
        form = LevelForm(request.POST)
    else:
        form = LevelForm()
    return save_level_form(request, form, 'master/add/addlevel.html')
# ->edit


def table_level_edit(request, pk):
    group = get_object_or_404(LevelUser, pk=pk)
    if request.method == 'POST':
        form = LevelForm(request.POST, instance=group)
    else:
        form = LevelForm(instance=group)
    return save_level_form(request, form, 'master/edit/editlevel.html')
# ->delete


def table_level_delete(request, pk):
    group = get_object_or_404(LevelUser, pk=pk)
    data = dict()
    if pk == int(1) or pk == int(2) or pk == int(3):
        data['trangchu'] = True
    else:
        if request.method == 'POST':
            group.delete()
            # This is just to play along with the existing code
            data['request'] = True
            groups = LevelUser.objects.all().order_by('id')
            data['list'] = render_to_string('master/list/level.html', {
                'data': groups
            })
        else:
            context = {'level': group}
            data['modal_form'] = render_to_string('master/delete/deletelevel.html',
                                                  context,
                                                  request=request
                                                  )
    return JsonResponse(data)
#############################


def table_formality(request):
    data = Formality.objects.all().order_by('id')
    return render(request, 'master/table_formality.html', {'data': data})


#-> hàm chung
def save_formaily_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['request']=True
            formal = Formality.objects.all().order_by('id')
            data['list']=render_to_string('master/list/formality.html',{'data':formal})
        else:
            data['request']=False
    context = {'form':form}
    data['modal_form']=render_to_string(template_name, context, request=request)
    return JsonResponse(data)
#->add
def table_formality_add(request):
    if request.method == 'POST':
        form = FormalityForm(request.POST)
    else:    
        form = FormalityForm()
    return save_formaily_form(request, form, 'master/add/addbody.html')

def table_formality_edit(request, pk):
    get_data = get_object_or_404(Formality, pk=pk)
    if pk == int(1) or pk == int(2) :
        form = FormalityForm(instance=get_data)
    elif request.method == 'POST':
        form = FormalityForm(request.POST,instance=get_data)
    else:
        form = FormalityForm(instance=get_data)
    return save_formaily_form(request, form, 'master/edit/editbody.html')
def table_formality_delete(request, pk ):
    get_data = get_object_or_404(Formality, pk=pk)
    data = dict()
    if pk == int(1) or pk == int(2) :
            data['trangchu'] = True
    else:
        if request.method == 'POST':
            get_data.delete()
            # This is just to play along with the existing code
            data['request'] = True
            formal = Formality.objects.all().order_by('id')
            data['list']=render_to_string('master/list/formality.html',{'data':formal})
        else:
            context = {'data': get_data}
            data['modal_form'] = render_to_string('master/delete/deletebody.html',
                                                  context,
                                                  request=request
                                                  )
    return JsonResponse(data)
#############################


def table_user(request):
    data = User_Comic.objects.filter(Group=2).order_by('-CreateDate')
    return render(request, 'master/table_user.html', {'data': data})
#->hamn chung
def save_user_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['request']=True
            user = User_Comic.objects.filter(Group=2).order_by('-CreateDate')
            data['list']=render_to_string('master/list/formality.html',{'data':user})
        else:
            data['request']=False
    context = {'form':form}
    data['modal_form']=render_to_string(template_name, context, request=request)
    return JsonResponse(data)
#->add
def table_user_add(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
    else:    
        form = UserForm()
    return save_user_form(request, form, 'master/add/adduser.html')

def table_user_edit(request, pk):
    get_data = get_object_or_404(User_Comic, pk=pk)
    if pk == int(1):
        form = UserForm(instance=get_data)
    elif request.method == 'POST':
        form = UserForm(request.POST,request.FILES,instance=get_data)
    else:
        form = FormalityForm(instance=get_data)
    return save_user_form(request, form, 'master/edit/edituser.html')
def table_user_delete(request, pk ):
    get_data = get_object_or_404(User_Comic, pk=pk)
    data = dict()
    if pk == int(1) or pk == int(2) :
            data['trangchu'] = True
    else:
        if request.method == 'POST':
            get_data.delete()
            # This is just to play along with the existing code
            data['request'] = True
            user = User_Comic.objects.filter(Group=2).order_by('-CreateDate')
            data['list']=render_to_string('master/list/formality.html',{'data':user})
        else:
            context = {'data': get_data}
            data['modal_form'] = render_to_string('master/delete/deleteuser.html',
                                                  context,
                                                  request=request
                                                  )
    return JsonResponse(data)
#############################


def table_manga_type(request):
    data = MangaType.objects.all().order_by('id')
    return render(request, 'master/table_manga_type.html', {'data': data})

def save_type_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['request']=True
            mantype = MangaType.objects.all().order_by('id')
            data['list']=render_to_string('master/list/type.html',{'data':mantype})
        else:
            data['request']=False
    context = {'form':form}
    data['modal_form']=render_to_string(template_name, context, request=request)
    return JsonResponse(data)
#->add
def table_type_add(request):
    if request.method == 'POST':
        form = MangaTypeForm(request.POST)
    else:    
        form = MangaTypeForm()
    return save_type_form(request, form, 'master/add/addtype.html')

def table_type_edit(request, pk):
    get_data = get_object_or_404(MangaType, pk=pk)
    if pk == int(1):
        form = MangaTypeForm(instance=get_data)
    elif request.method == 'POST':
        form = MangaTypeForm(request.POST, instance=get_data)
    else:
        form = MangaTypeForm(instance=get_data)
    return save_type_form(request, form, 'master/edit/edittype.html')
def table_type_delete(request, pk ):
    get_data = get_object_or_404(MangaType, pk=pk)
    data = dict()
    if pk == int(1) or pk == int(2) :
            data['trangchu'] = True
    else:
        if request.method == 'POST':
            get_data.delete()
            # This is just to play along with the existing code
            data['request'] = True
            mantype = MangaType.objects.all().order_by('id')
            data['list']=render_to_string('master/list/type.html',{'data':mantype})
        else:
            context = {'data': get_data}
            data['modal_form'] = render_to_string('master/delete/deletetype.html',
                                                  context,
                                                  request=request
                                                  )
    return JsonResponse(data)
#############################


def table_category(request):
    data = Category.objects.all().order_by('id')
    return render(request, 'master/table_category.html', {'data': data})

def save_cate_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['request']=True
            cate = Category.objects.all().order_by('id')
            data['list']=render_to_string('master/list/cate.html',{'data':cate})
        else:
            data['request']=False
    context = {'form':form}
    data['modal_form']=render_to_string(template_name, context, request=request)
    return JsonResponse(data)
#->add
def table_cate_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
    else:    
        form = CategoryForm()
    return save_cate_form(request, form, 'master/add/addcate.html')

def table_cate_edit(request, pk):
    get_data = get_object_or_404(Category, pk=pk)
    if pk == int(1):
        form = CategoryForm(instance=get_data)
    elif request.method == 'POST':
        form = CategoryForm(request.POST, instance=get_data)
    else:
        form = CategoryForm(instance=get_data)
    return save_cate_form(request, form, 'master/edit/editcate.html')

def table_cate_delete(request, pk ):
    get_data = get_object_or_404(Category, pk=pk)
    data = dict()
    if pk == int(1) or pk == int(2) :
            data['trangchu'] = True
    else:
        if request.method == 'POST':
            get_data.delete()
            # This is just to play along with the existing code
            data['request'] = True
            cate = Category.objects.all().order_by('id')
            data['list']=render_to_string('master/list/cate.html',{'data':cate})
        else:
            context = {'data': get_data}
            data['modal_form'] = render_to_string('master/delete/deletecate.html',
                                                  context,
                                                  request=request
                                                  )
    return JsonResponse(data)
#############################


def table_manga(request):
    data = Manga.objects.all().order_by('MangaName')
    return render(request, 'master/table_manga.html', {'data': data})

# >>>>>>>>>>>> Add


def table_manga_add(request):
    add = Manga()
    if request.method == 'GET':
        kieutruyen = Formality.objects.all()
        theloai = Category.objects.all()
        nhomtruyen = MangaType.objects.all()
        nguoidung = User_Comic.objects.filter(Group=2)
        Data = {
            'kieu': kieutruyen,
            'tl': theloai,
            'nhom': nhomtruyen,
            'user': nguoidung
        }
        return render(request, 'master/addmanga.html', Data)
    else:

        MangaName = request.POST['MangaName']
        MangaSlug = request.POST['MangaSlug']
        OrtherName = request.POST['OrtherName']
        Author = request.POST['Author']
        Editor = request.POST['Editor']
        StartDate = request.POST['StartDate']
        EndDate = request.POST['EndDate']
        # Formality = request.POST['kieutruyen']
        Content = request.POST['NoiDung']
        # StatusPost =request.POST['StatusPost']
        Image = request.FILES['Image']
        lst = Category.objects.all()
        if MangaName != None and MangaSlug != None and Content != None:
            add.MangaName = MangaName
            add.Slug = MangaSlug
            add.OrtherName = OrtherName
            add.Author = Author
            add.Editor = Editor
            add.StartDate = StartDate
            add.EndDate = EndDate
            add.Image = Image
            add.Content = Content
            add.MangaType = MangaType.objects.get(pk=1)
            add.User_Comic = User_Comic.objects.get(pk=2)
            add.Formality = Formality.objects.get(pk=1)
            add.save()
            for Ma in lst:
                cate = MangaCategory()
                cate.Manga = add
                cate.Category = Ma
                cate.DeleteDate = StartDate
                cate.save()
            return redirect('/master/table/manga/')
        else:
            return redirect('/master/table/manga/add/')

#############################


def table_manga_category(request):
    manga = Manga.objects.all().order_by('MangaName')
    data = MangaCategory.objects.all().order_by('Manga')
    Data = {
        'data': data,
        'manga': manga,
    }
    return render(request, 'master/table_manga_category.html', Data)
# -> Add
def save_mancate_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['request']=True
            manga = Manga.objects.all().order_by('MangaName')
            data1 = MangaCategory.objects.all().order_by('Manga')
            Data = {
                'data': data1,
                'manga': manga,
            }
            data['list']=render_to_string('master/list/mancate.html',Data)
        else:
            data['request']=False
    context = {'form':form}
    data['modal_form']=render_to_string(template_name, context, request=request)
    return JsonResponse(data)
#->add
def table_mancate_add(request):
    if request.method == 'POST':
        form = MangaCateForm(request.POST)
    else:    
        form = MangaCateForm()
    return save_mancate_form(request, form, 'master/add/addmancate.html')

def table_mancate_edit(request, pk):
    get_data = get_object_or_404(MangaCategory, pk=pk)
    if pk == int(1):
        form = MangaCateForm(instance=get_data)
    elif request.method == 'POST':
        form = MangaCateForm(request.POST, instance=get_data)
    else:
        form = MangaCateForm(instance=get_data)
    return save_mancate_form(request, form, 'master/edit/editmancate.html')

def table_mancate_delete(request, pk ):
    get_data = get_object_or_404(MangaCategory, pk=pk)
    data = dict()
    if pk == int(1) or pk == int(2) :
            data['trangchu'] = True
    else:
        if request.method == 'POST':
            get_data.delete()
            # This is just to play along with the existing code
            data['request'] = True
            manga = Manga.objects.all().order_by('MangaName')
            data1 = MangaCategory.objects.all().order_by('Manga')
            Data = {
                'data': data1,
                'manga': manga,
            }
            data['list']=render_to_string('master/list/mancate.html',Data)
        else:
            context = {'data': get_data}
            data['modal_form'] = render_to_string('master/delete/deletemancate.html',
                                                  context,
                                                  request=request
                                                  )
    return JsonResponse(data)

def chap_create(request):
    data = dict()
    if request.method == 'POST':
        form = ChapForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            return redirect('/master/table/chap/')
        else:
            data['form_is_valid'] = False
            context = {'form': form}
            html_form = render_to_string(
                'master/add/addchap.html', context, request=request,)
            return JsonResponse({'html_form': html_form})
    else:
        form = ChapForm()
    context = {'form': form}
    html_form = render_to_string(
        'master/add/addchap.html', context, request=request,)
    return JsonResponse({'html_form': html_form})

#############################


def table_chap(request):
    manga = Manga.objects.all().order_by('MangaName')
    data = Chap.objects.all()
    Data = {
        'manga': manga,
        'data': data
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
