from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home_master, name='master'),
    path('table/user-group/', views.table_user_group, name='tblusergroup'),
    path('talbe/level-user/', views.table_level_user, name='tblleveluser'),
    path('table/formality/', views.table_formality, name='tblformality'),
    path('table/comment/', views.table_comment, name='tblcomment'),
    path('table/rate/', views.table_rate, name='tblrate'),
    path('table/vote/', views.table_vote, name='tblvote'),
    path('table/notifical/', views.table_notifical, name='tblnotifical'),
    path('table/category/', views.table_category, name='tblcategory'),
    path('table/manga-type/', views.table_manga_type, name='tblmangatype'),
    path('table/manga-category/', views.table_manga_category, name='tblmangacategory'),
    path('table/user/', views.table_user, name='tbluser'),
    path('table/manga/', views.table_manga, name='tblmanga'),
    path('table/chap/', views.table_chap, name='tblchap'),
]