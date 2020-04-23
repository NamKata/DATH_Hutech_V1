from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home_client, name='trang-chu'),
    path('info/', views.info, name='info'),
    path('online/', views.home_login, name='online'),
    path('more-manga/', views.more_manga, name='more-manga'),
    path('manga/<int:Manga_id>/', views.manga, name='manga'),
    path('chap/<int:id>/', views.chap, name='chap'),
    path('chapchu/<int:id>/', views.chap_chu, name='chapchu'),
    path('message/', views.message, name='message'),
    path('send/', views.send_messgae, name='send'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)