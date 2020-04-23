from django.db import models
from django.utils import timezone
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
    Password = models.CharField(max_length=25)
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
    Slug = models.SlugField()
    def __str__(self):
        return self.Name # TODO
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
    Content = models.TextField(null=True, blank=True)
    Author = models.CharField( max_length=100, null=True, blank=True)
    Editor = models.CharField(max_length= 100, null=True, blank=True)
    StartDate = models.DateField( blank=True)
    EndDate=models.DateField( blank=True)
    Share = models.IntegerField(default=0)
    StatusFinish = models.BooleanField(default=False)
    StatusPost = models.BooleanField(default= False)
    StatusDelete = models.BooleanField(default=False)
    Formality = models.ForeignKey(Formality, on_delete=models.CASCADE)
    User_Comic = models.ForeignKey(User_Comic, on_delete=models.CASCADE)
    MangaType = models.ForeignKey(MangaType, on_delete=models.CASCADE)
    CreateDate = models.DateTimeField(default=timezone.now)
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
    Content = models.TextField(null=True)
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
        return self.User_Comic+" - "+ self.Chap +" : "+ self.Content # TODO

# /11 Table -> Follow
class Follow(models.Model):
    Manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    User_Comic = models.ForeignKey(User_Comic, on_delete=models.CASCADE)
    StatusFollow = models.BooleanField(default=True)
    CreateDate = models.DateTimeField(default=timezone.now)
    DateUnfollow = models.DateTimeField()

# /12 Table -> Rating
class Rating(models.Model):
    Manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    User_Comic = models.ForeignKey(User_Comic, on_delete=models.CASCADE)
    Rating = models.IntegerField()
    CreateDate = models.DateTimeField(default= timezone.now)

# /13 Table -> Vote
class Vote(models.Model):
    Manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    User_Comic = models.ForeignKey(User_Comic, on_delete=models.CASCADE)
    Price = models.IntegerField(default=10)
    Quality = models.IntegerField()
    CreateDate =models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.Quality*self.Price # TODO

# /14 Table ->Notifical
class Notifical(models.Model):
    Follow = models.ForeignKey(Follow, on_delete=models.CASCADE)
    Content = models.CharField( max_length=150, null=True)
    CreateDate =models.DateTimeField(default=timezone.now) 
    SetTime=models.DateTimeField()
    StatusSet=models.BooleanField(default=False)
    def __str__(self):
        return self.Content # TODO