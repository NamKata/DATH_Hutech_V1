from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
urlpatterns = [
    path('', views.home_client, name='trang-chu'),
    path('thong-tin-ca-nhan/ma-nguoi-dung-<int:pk>/', views.info, name='info'),
    path('message/', views.message, name='message'),
    path('send/', views.send_messgae, name='send'),
    path('danh-sach-truyen-moi-cap-nhap/', views.truyenmoicapnhap, name='list-cap-nhap'),
    path('danh-sach-truyen-tranh/', views.truyentranh, name='list-tranh'),
    path('danh-sach-truyen-chu/', views.truyenchu, name='list-chu'),
    path('dang-ki-tai-khoan/', views.user_register, name='dang-ki'),
    path('gui-email-mat-khau/', views.sendmail_quenmatkhau, name='gmail-mk'),
    path('dang-nhap-tai-khoan/', views.user_login, name='dang-nhap'),
    path('truyen-tranh/<slug:Slug>/', views.manga_truyentranh, name='truyen-tranh'),
    path('truyen-chu/<slug:Slug>/', views.manga_truyenchu, name='truyen-chu'),
    path('truyen-tranh/<slug:Slug>/chương-<int:SttChap>', views.chap_truyentranh, name='truyen-tranh-chap'),
    path('truyen-chu/<slug:Slug>/chương-<int:SttChap>', views.chap_truyenchu, name='truyen-chu-chap'),
    path('tim-kiem-truyen/', views.search, name='tim-kiem'),
    path('tim-kiem-goi-y/', views.search_autocomplete, name='tim-kiem-goi-y'),
    path('kiem-tra-tai-khoan/', views.check_exists, name='kiem-tra'),
    path('kiem-tra-email/', views.check_exists_email, name='kiem-tra-email'),
    path('kiem-tra-tinh-trang-dang-nhap/', views.check_session_user, name='kiem-tra-dang-nhap'),
    path('dang-xuat/<int:pk>/', views.logout, name='dang-xuat'),
    path('truyen-theo-doi-cua-nguoi-dung-<int:pk>/', views.follow_comic, name='follow'),
    path('dang-ky-truyen/', views.dangkytruyen, name='dang-ky-truyen'),
    path('xac-nhan-dang-ky-truyen/', views.send_dangkytruyen, name='xac-nhan-dang-ky-truyen'),
    path('kich-hoat-dang-ky-nguoi-dung/<int:pk>',views.send_mail,name='kich-hoat-mail'),
    path('doi-mat-khau-nguoi-dung-<int:pk>/',views.doimatkhau, name='doi-mat-khau'),
    path('tu-truyen-cua-nguoi-dung-<int:pk>/',views.tutruyen, name='tu-truyen'),
    path('thong-tin-cua-truyen-co-ma-<int:pk>/', views.chitiettruyen, name='chitiettruyen'),
    path('them-chuong-truyen-co-ma-<int:pk>/', views.themchuong, name='themchuong'),
    path('danh-sach-chuong-<int:pk>/', views.danhsachchuong, name='danh-sach-chuong'),
    path('sua-chuong-<int:pk>/', views.editchuong, name='suachuong'),
    path('xoa-chuong-<int:pk>/', views.xoachuong, name='xoachuong'),
    path('next-chap/', views.NextChap, name='next-chap'),
    path('the-loai-truyen/', views.theloaitruyen ,name='theloai'),
    path('binh-luan-chap-co-ma-<int:pk>/', views.binhluan ,name='binhluan'),
    path('chia-se-truyen-ma-<int:pk>', views.share, name='share'),
    path('the-loai-truyen-<int:pk>/', views.theloai, name='the-loai-truyen'),
    path('tat-kich-hoat-truyen/<int:Matruyen>', views.tatkichhoat, name='sttkichhoat'),
    path('tinh-tran-theo-doi/<int:Matruyen>', views.theodoitruyen, name='theodoi'),
    path('reset-password/<int:pk>', views.reset_password, name='resetmk'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)