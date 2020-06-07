from unidecode import unidecode
from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
# from django.template.defaultfilters import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify2
from django.urls import reverse
from django.core.files import File  # you need this somewhere
import urllib





def vi_slu(data):
    vietnamese_map = {
    ord(u'a'):'a',
    ord(u'á'):'a',
    ord(u'ã'):'a',
    ord(u'ạ'):'a',
    ord(u'à'):'a',
    ord(u'ả'):'a',
    ord(u'â'):'a',
    ord(u'ấ'):'a',
    ord(u'ẫ'):'a',
    ord(u'ậ'):'a',
    ord(u'ầ'):'a',
    ord(u'ẩ'):'a',
    ord(u'ă'):'a',
    ord(u'ắ'):'a',
    ord(u'ẵ'):'a',
    ord(u'ặ'):'a',
    ord(u'ằ'):'a',
    ord(u'ẳ'):'a',
    ord(u'b'):'b',
    ord(u'c'):'c',
    ord(u'd'):'d',
    ord(u'đ'):'d',
    ord(u'e'):'e',
    ord(u'ê'):'e',
    ord(u'ế'):'e',
    ord(u'ễ'):'e',
    ord(u'ệ'):'e',
    ord(u'ể'):'e',
    ord(u'ề'):'e',
    ord(u'g'):'g',
    ord(u'h'):'h',
    ord(u'i'):'i',
    ord(u'í'):'i',
    ord(u'ì'):'i',
    ord(u'ị'):'i',
    ord(u'ĩ'):'i',
    ord(u'ỉ'):'i',
    ord(u'k'):'k',
    ord(u'l'):'l',
    ord(u'm'):'m',
    ord(u'n'):'n',
    ord(u'o'):'o',
    ord(u'ò'):'o',
    ord(u'ó'):'o',
    ord(u'ọ'):'o',
    ord(u'õ'):'o',
    ord(u'ỏ'):'o',
    ord(u'ô'):'o',
    ord(u'ố'):'o',
    ord(u'ồ'):'o',
    ord(u'ỗ'):'o',
    ord(u'ộ'):'o',
    ord(u'ổ'):'o',
    ord(u'ơ'):'o',
    ord(u'ớ'):'o',
    ord(u'ờ'):'o',
    ord(u'ỡ'):'o',
    ord(u'ợ'):'o',
    ord(u'ở'):'o',
    ord(u'p'):'p',
    ord(u'q'):'q',
    ord(u'r'):'r',
    ord(u's'):'s',
    ord(u't'):'t',
    ord(u'u'):'u',
    ord(u'ú'):'u',
    ord(u'ù'):'u',
    ord(u'ũ'):'u',
    ord(u'ủ'):'u',
    ord(u'ụ'):'u',
    ord(u'ư'):'u',
    ord(u'ứ'):'u',
    ord(u'ừ'):'u',
    ord(u'ữ'):'u',
    ord(u'ử'):'u',
    ord(u'ự'):'u',
    ord(u'v'):'v',
    ord(u'x'):'x',
    ord(u'ý'): 'y', ord(u'ỳ'): 'y', ord(u'ỷ'): 'y', ord(u'ỹ'): 'y', ord(u'ỵ'): 'y',
    ord(u'Đ'): 'd',
    }
    slug = slugify(unidecode(data).translate(vietnamese_map))
    return slug


# Create your models here.
# 1/ Table --> User group
class Usergroup(models.Model):
    Name = models.CharField(max_length=50)
    CreateDate = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.Name

# 2/ Table -> Level


class LevelUser(models.Model):
    LevelName = models.CharField(max_length=100)
    CheckFollow = models.IntegerField()
    CheckView = models.IntegerField()

    def __str__(self):
        return self.LevelName  # TODO


# /3 Talbe ->Formality Truyen covert hay tự sáng tác
class Formality(models.Model):
    Name = models.CharField(max_length=100)
    Content = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.Name  # TODO


# 4/ Table -> User
class User_Comic(models.Model):
    UserName = models.CharField(max_length=100)
    Email = models.EmailField(max_length=254)
    Password = models.CharField(max_length=25, null=True, blank=True)
    Birthday = models.DateField()
    Address = models.CharField( max_length=150, null=True, blank=True)
    Phone = models.CharField(max_length=12, null=True, blank=True)
    Coins = models.IntegerField(default=0)
    NickName = models.CharField(max_length=100, null=True, blank=True)
    StatusEmail = models.BooleanField(default=False)
    StatusDelete = models.BooleanField(default=False)
    Image = models.ImageField(upload_to='User', max_length=150, null=True, blank=True)
    Content =models.CharField(max_length=150, null=True, blank=True)
    LevelUser = models.ForeignKey(LevelUser, on_delete=models.CASCADE)
    Group = models.ForeignKey(Usergroup, on_delete=models.CASCADE)
    CreateDate = models.DateTimeField(default=timezone.now)
    StatusGender = models.BooleanField(default=False)
  
    def __str__(self):
        return self.UserName  # TODO

# /5 Table -> MangaType 1 Truyentranh 2 TruyenChu
class MangaType(models.Model):
    Name = models.CharField(max_length=150)
    Slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.Name # TODO
    def get_absolute_url(self):
            return reverse('MangaType_detail', kwargs={'Slug': self.Name})
    def save(self, *args, **kwargs): # new
        if not self.Slug:
            self.Slug = slugify2(self.Name)
        return super().save(*args, **kwargs)


# /6 Table -> Category
class Category(models.Model):
    CategoryName = models.CharField(max_length=150)
    CategoryContent = models.CharField(max_length=500, null=True)
    CategorySlug = models.SlugField()
   
    def __str__(self):
        return self.CategoryName  # TODO


# /7 Table -> Manga
class Manga(models.Model):
    MangaName = models.CharField(max_length=250)
    OrtherName = models.CharField(max_length=250, null=True)
    Slug = models.SlugField()
    Image = models.ImageField(upload_to='Manga', max_length=150, null=True, blank=True)
    Content = RichTextField(null=True, blank=True)
    Author = models.CharField( max_length=100, null=True, blank=True)
    Editor = models.CharField(max_length= 100, null=True, blank=True)
    StartDate = models.DateField(auto_now = True,null=True, blank=True)
    EndDate=models.DateField(auto_now = True,null=True, blank=True)
    Share = models.IntegerField(default=0)
    StatusFinish = models.BooleanField(default=False)
    StatusPost = models.BooleanField(default= False)
    StatusDelete = models.BooleanField(default=False)
    Formality = models.ForeignKey(Formality, on_delete=models.CASCADE)
    User_Comic = models.ForeignKey(User_Comic, on_delete=models.CASCADE)
    MangaType = models.ForeignKey(MangaType, on_delete=models.CASCADE)
    CreateDate = models.DateTimeField(default=timezone.now)
    Chapnow = models.IntegerField(default=0)
    DateUpChap = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.MangaName # TODO


# /8 Table ->MangaCategory
class MangaCategory(models.Model):
    Manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    StatusDelete = models.BooleanField(default=False)
    CreateDate = models.DateTimeField(default=timezone.now)
    DeleteDate = models.DateTimeField()
    

# /9 Table ->Chap
class Chap(models.Model):
    SttChap = models.IntegerField(("Chap "))
    Title = models.CharField(max_length=200)
    Content = RichTextUploadingField(null=True, blank=True)
    Views = models.IntegerField(default=0)
    StatusPost = models.BooleanField(default=False)
    StatusEdit = models.BooleanField(default=False)
    DateUp = models.DateTimeField()
    DateEdit = models.DateTimeField()
    CreateDate = models.DateTimeField(default=timezone.now)
    Manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    def __str__(self):
        return self.Title # TODO

# /10 Table ->Comment
class Comment(models.Model):
    User_Comic = models.ForeignKey(User_Comic, on_delete=models.CASCADE)
    Chap = models.ForeignKey(Chap, on_delete=models.CASCADE)
    Content = models.CharField(max_length=500, null=True)
    Rating = models.IntegerField()
    CreateDate = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.Content # TODO

# /11 Table -> Follow
class Follow(models.Model):
    Manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    User_Comic = models.ForeignKey(User_Comic, on_delete=models.CASCADE)
    StatusFollow = models.BooleanField(default=True)
    CreateDate = models.DateTimeField(default=timezone.now)
    DateUnfollow = models.DateTimeField()



# /14 Table ->Notifical
class Notifical(models.Model):
    Follow = models.ForeignKey(Follow, on_delete=models.CASCADE)
    Content = models.CharField( max_length=150, null=True)
    CreateDate =models.DateTimeField(default=timezone.now) 
    SetTime=models.DateTimeField()
    StatusSet=models.BooleanField(default=False)
    def __str__(self):
        return self.Content # TODO