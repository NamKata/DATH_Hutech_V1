from django.contrib import admin
from DB.models import Usergroup, LevelUser, Formality, MangaType, User_Comic, Category, Manga, MangaCategory, Chap, Comment, Follow, Rating, Vote, Notifical
# Register your models here.
admin.site.register(Usergroup)
admin.site.register(LevelUser)
admin.site.register(Formality)
admin.site.register(User_Comic)
admin.site.register(MangaType)
admin.site.register(Category)
admin.site.register(Manga)
admin.site.register(MangaCategory)
admin.site.register(Chap)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Rating)
admin.site.register(Vote)
admin.site.register(Notifical)

