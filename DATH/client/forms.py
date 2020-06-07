from django import forms
from django.utils.safestring import mark_safe
from DB.models import Usergroup, LevelUser, Formality, MangaType, User_Comic, Category, Manga, MangaCategory, Chap, Comment, Follow,  Notifical
import re

class RegisterForm(forms.Form):
    Username = forms.CharField(label='Tài Khoản', max_length=30, widget=forms.TextInput(attrs={'placeholder':'Tài Khoản', 'type':'text','id':'user_register'}))
    Email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'placeholder':'Email', 'type':'email','id':'email_register'}))
    Password = forms.CharField(label='Mật khẩu', widget=forms.TextInput(attrs={'placeholder':'Mật Khẩu', 'type':'password','id':'password_register'}))
    nPassword = forms.CharField(label='Nhập lại mật khẩu', widget=forms.TextInput(attrs={'placeholder':'Nhập Lại Mật Khẩu', 'type':'password','id':'npassword_register'}))

    def clean_nPassword(self):
        if 'Password' in self.cleaned_data:
            Password = self.cleaned_data['Password']
            nPassword = self.cleaned_data['nPassword']
            if Password == nPassword and Password:
                return nPassword
        raise forms.ValidationError("Mật khẩu không hợp lệ")

    def clean_Username(self):
        Username = self.cleaned_data['Username']
        # if not re.search(r'^\w+$', Username):
        #     raise forms.ValidationError("Tên tài khoản có kí tự đặc biệt")
        try:
            User_Comic.objects.get(UserName=Username)
        except User_Comic.DoesNotExist:
            return Username
        raise forms.ValidationError("Tài khoản đã tồn tại")
    def save(self):
        malv = LevelUser.objects.get(pk=2)
        magr = Usergroup.objects.get(pk=2)
        User_Comic.objects.create(UserName=self.cleaned_data['Username'], Email=self.cleaned_data['Email'], Password=self.cleaned_data['Password'], Birthday = '2001-01-01', Group = magr, LevelUser = malv)

class ImagePreviewWidget(forms.widgets.FileInput):
    def render(self, name, value, attrs=None, **kwargs):
        input_html = super().render(name, value, attrs=None, **kwargs)
        img_html = mark_safe(f'<br><br><img src="{value.url}"/>')
        return f'{input_html}{img_html}'
class Register_Manga(forms.ModelForm):
    class Meta:
        model = Manga
        fields = ('MangaName','Slug','OrtherName','Content','Author','Editor','Formality','MangaType','User_Comic','Image',)
        labels  = {
            'MangaName':'Tên Truyện',
            'Slug':'Đường Dẫn',
            'OrtherName':'Tên Khác',
            'Author':'Tác Giả',
            'Editor':'Người Dịch',
            'Formality':'Kiểu Truyện',
            'MangaType':'Nhóm Truyện',
            'Content':'Nội Dung',
            'User_Comic':'Người Đăng',
            'Image':'Ảnh',
        }
        widgets ={
            'MangaName':forms.TextInput(attrs={'class':'input','id':'MangaName'}),
            'Slug':forms.TextInput(attrs={'class':'input','id':'Slug'}),
            'OrtherName':forms.TextInput(attrs={'class':'input'}),
            'Author':forms.TextInput(attrs={'class':'input'}),
            'Editor':forms.TextInput(attrs={'class':'input'}),
            # 'Formality':forms.TextInput(attrs={'class':'input'}),
            # 'MangaType':forms.TextInput(attrs={'class':'input'}),
            # 'Image':forms.TextInput(attrs={'class':'input','id':'uploadavatar','onchange':'img_pathUrl(this)','style':'display: none;'}),
        }
        photo = forms.ImageField(widget=ImagePreviewWidget,)