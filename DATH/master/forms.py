from django import forms
from DB.models import Usergroup, LevelUser, Formality, MangaType, User_Comic, Category, Manga, MangaCategory, Chap, Comment, Follow,  Notifical
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor.fields import RichTextField
#-> Form User Group
class GroupForm(forms.ModelForm):
    class Meta:
        model = Usergroup
        fields = ('Name',)

# -> Form Level User
class LevelForm(forms.ModelForm):
    class Meta:
        model = LevelUser
        fields =('LevelName', 'CheckFollow', 'CheckView',)


class FormalityForm(forms.ModelForm):
    class Meta:
        model = Formality
        fields = "__all__"

class UserForm(forms.ModelForm):
     class Meta:
        model = User_Comic
        fields = "__all__"

class MangaTypeForm(forms.ModelForm):
     class Meta:
        model = MangaType
        fields = "__all__"

class CategoryForm(forms.ModelForm):
     class Meta:
        model = Category
        fields = "__all__"

class MangaForm(forms.ModelForm):
     class Meta:
        model = Manga
        fields = "__all__"
class MangaCateForm(forms.ModelForm):
     class Meta:
        model = MangaCategory
        fields = "__all__"


class ChapForm(forms.ModelForm):
    class Meta:
        model = Chap
        fields = ('SttChap', 'Title', 'Content', 'DateUp', 'DateEdit', 'Manga',)
        widgets = {
            'DateUp':forms.DateInput(
                attrs={'class':'form-control', 'placeholder':'yyyy/MM/dd', 'type':'date'}
            ),
            'DateEdit':forms.DateInput(
                attrs={'class':'form-control', 'placeholder':'yyyy/MM/dd', 'type':'date'}
            ),
            'Content':forms.Textarea(attrs={'style':'width: 835px;'})

        }

       
class LoginForm(forms.Form):
    Username = forms.CharField(label='Tài Khoản', max_length=30, widget=forms.TextInput(attrs={'placeholder':'Tài Khoản', 'type':'text','id':'user_login'}))
    Password = forms.CharField(label='Mật khẩu', widget=forms.TextInput(attrs={'placeholder':'Mật Khẩu', 'type':'password','id':'password_login'}))
   
