from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserEditForm, ImagenForm
from .models import Imagen
from django.contrib import messages
from django.db import IntegrityError 
from django.urls import reverse, reverse_lazy

def user_login(request):
    msg_login = "Bienvenido"
    auth_failed = False

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST or None)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect(reverse('base'))
                
            else:
                msg_login = 'Usuario o contraseña incorrectos'
                auth_failed = True
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form, 'msg_login': msg_login, 'auth_failed': auth_failed})

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Has cerrado sesión correctamente.')
    else:
        messages.info(request, 'No estabas autenticado.')

    return redirect(reverse_lazy('base'))

def user_register(request):
    msg_register = ''
    form = UserRegisterForm() 
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)  
                msg_register = 'Usuario registrado correctamente'

            except IntegrityError as e:
                if 'username' in str(e):  
                    msg_register = 'Ya existe un usuario con ese nombre de usuario'
                else:
                    msg_register = 'Error al registrar el usuario'
                messages.error(request, msg_register) 
        else:
            msg_register = 'Error al registrar el usuario' 

    return render(request, 'users/register.html', {'form': form, 'msg_register': msg_register})
    
@login_required
def user_profile(request):
    usuario = request.user

    if request.method == 'POST':
        miFormulario = UserEditForm(request.POST, request.FILES, instance=usuario)
        
        imagen_form = ImagenForm(request.POST, request.FILES)

        if miFormulario.is_valid():
            miFormulario.save()

            imagen = imagen_form.cleaned_data.get('imagen') if imagen_form.is_valid() else None
            if imagen:
                if hasattr(usuario, 'imagen'):
                    usuario.imagen.imagen = imagen
                    usuario.imagen.save()
                else:
                    Imagen.objects.create(user=usuario, imagen=imagen)

                messages.success(request, 'Imagen de perfil actualizada correctamente')
            else:
                messages.success(request, 'Perfil actualizado correctamente')
                
            return redirect('profile')

        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')

    else:
        miFormulario = UserEditForm(instance=usuario)
        imagen_form = ImagenForm()

    return render(request, 'users/profile.html', {
        'miFormulario': miFormulario,
        'imagen_form': imagen_form,
    })
