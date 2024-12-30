from django import forms
from .models import Plato, Mesa, Reserva

class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre', 'descripcion', 'precio', 'categoria']

class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ['numero', 'capacidad']
    def clean_numero(self):
        numero = self.cleaned_data.get('numero')
        if Mesa.objects.filter(numero=numero).exists():
            raise forms.ValidationError(f"La mesa con el número {numero} ya está registrada.")
        return numero

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['nombre_cliente', 'mesa', 'fecha', 'hora']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}), 
            'hora': forms.TimeInput(attrs={'type': 'time'}),   
        }
    def clean(self):
        cleaned_data = super().clean()
        mesa = cleaned_data.get('mesa')
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')

        if mesa and fecha and hora:
            conflicto = Reserva.objects.filter(mesa=mesa, fecha=fecha).exists()
            if conflicto:
                raise forms.ValidationError(f"La mesa {mesa.numero} ya está reservada en esta fecha.")

        return cleaned_data
class BuscarPlatoForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=False)
    categoria = forms.ChoiceField(choices=[('', 'Todos')] + Plato.CATEGORIAS, required=False)

class BuscarReservaForm(forms.Form):
    nombre_cliente = forms.CharField(max_length=100, required=False)
    fecha = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    