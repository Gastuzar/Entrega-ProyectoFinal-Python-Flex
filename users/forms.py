from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Imagen

class UserRegisterForm(UserCreationForm):    
    email = forms.EmailField()
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserEditForm(forms.ModelForm):  
    email = forms.EmailField(label='Ingrese su email: ')
    password1 = forms.CharField(
        label='Ingrese su nueva contraseña: ', 
        widget=forms.PasswordInput, 
        required=False  
    )
    password2 = forms.CharField(
        label='Confirme su nueva contraseña: ', 
        widget=forms.PasswordInput, 
        required=False
    )
    imagen = forms.ImageField(label='Seleccione una imagen de perfil: ', required=False)

    class Meta:
        model = User
        fields = ['email', 'imagen'] 

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        password1 = self.cleaned_data.get('password1')
        if password1:
            user.set_password(password1)

        if commit:
            user.save()
        return user

class ImagenForm(forms.ModelForm):
    class Meta:
        model = Imagen
        fields = ['imagen']

    def __init__(self, *args, **kwargs):
        super(ImagenForm, self).__init__(*args, **kwargs)
        self.fields['imagen'].widget.attrs.update({'class': 'form-control'})
        


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario: ')
    password = forms.CharField(label='Contraseña: ', widget=forms.PasswordInput)
