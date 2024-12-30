from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Plato, Mesa, Reserva
from restaurant.forms import PlatoForm, MesaForm, ReservaForm, BuscarPlatoForm, BuscarReservaForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse, reverse_lazy


@login_required
def menu(request):
    if request.method == 'POST':
        form = PlatoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = PlatoForm()

    buscar_form = BuscarPlatoForm(request.GET)
    platos = Plato.objects.all()

    if buscar_form.is_valid():
        nombre = buscar_form.cleaned_data.get('nombre')
        categoria = buscar_form.cleaned_data.get('categoria')

        if nombre:
            platos = platos.filter(nombre__icontains=nombre)
        if categoria:
            platos = platos.filter(categoria=categoria)

        if not platos.exists():
            buscar_form.add_error(None, "No se ha encontrado ese plato.")

    return render(
        request,
        'restaurant/menu.html',
        {'form': form, 'buscar_form': buscar_form, 'platos': platos}
    )

def eliminar_plato(request, plato_id):
    plato = get_object_or_404(Plato, id=plato_id)
    if request.method == 'POST':
        plato.delete()
        return redirect('menu')  
    return render(request, 'restaurant/eliminar_plato.html', {'plato': plato})

def ver_plato(request, plato_id):
    plato = get_object_or_404(Plato, id=plato_id)
    return render(request, 'restaurant/ver_plato.html', {'plato': plato})


def editar_plato(request, plato_id):
    plato = get_object_or_404(Plato, id=plato_id)
    if request.method == 'POST':
        form = PlatoForm(request.POST, instance=plato)
        if form.is_valid():
            form.save()
            return redirect('ver_plato', plato_id=plato.id)  
    else:
        form = PlatoForm(instance=plato)
    return render(request, 'restaurant/editar_plato.html', {'form': form, 'plato': plato})

@login_required
def mesas(request):
    if request.method == 'POST':
        form = MesaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mesas')
    else:
        form = MesaForm()
    mesas = Mesa.objects.all().order_by('numero')
    return render(request, 'restaurant/mesas.html', {'form': form, 'mesas': mesas})

def eliminar_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)  
    if request.method == 'POST':  
        mesa.delete()  
        return redirect(reverse_lazy('mesas')) 
    
    return redirect(reverse_lazy('mesas'))  

@login_required
def reservas(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reservas')
    else:
        form = ReservaForm()
    buscar_form = BuscarReservaForm(request.GET)
    reservas = Reserva.objects.all().order_by('fecha', 'hora')
    mensaje = None 

    if buscar_form.is_valid():
        nombre_cliente = buscar_form.cleaned_data.get('nombre_cliente')
        fecha = buscar_form.cleaned_data.get('fecha')
        if nombre_cliente:
            reservas = reservas.filter(nombre_cliente__icontains=nombre_cliente)
        if fecha:
            reservas = reservas.filter(fecha=fecha)
        if not reservas.exists():
            mensaje = "No se encontró ninguna reserva con los criterios especificados."
            buscar_form.add_error(None, mensaje)
    
    return render(request, 'restaurant/reservas.html', {
        'form': form, 
        'buscar_form': buscar_form, 
        'reservas': reservas
    })

def ver_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    return render(request, 'restaurant/ver_reserva.html', {'reserva': reserva})

def editar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            return redirect('ver_reserva', reserva_id=reserva.id)
    else:
        form = ReservaForm(instance=reserva)
    return render(request, 'restaurant/editar_reserva.html', {'form': form, 'reserva': reserva})
def eliminar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if request.method == 'POST':
        reserva.delete()
        return redirect(reverse_lazy('reservas'))
    return redirect(reverse_lazy('reservas'))

def base(request):
    bienvenida = "Bienvenido"
    return render(request, 'restaurant/base.html', {'bienvenida': bienvenida})

def about_me(request):
    presentacion = """¡Hola! Soy Gaston Zarate tengo 28 años y soy el creador de este sitio web.
    Soy licenciado en Kinesiologia y fisioterapia y actualmente me dedico a ello, pero ademas estoy aprendiendo a programar
    en Python, el framework Django y javascript.
    Siempre estoy buscando maneras de mejorar y ofrecer lo mejor de mi.
    Espero que disfrutes de este sitio web y si tienes alguna sugerencia, no dudes en contactarme.
    Gracias por tu visita!"""
    
    return render(request, 'restaurant/about_me.html', {'presentacion': presentacion})

