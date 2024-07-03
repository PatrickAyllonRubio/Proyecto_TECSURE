# forms.py

from django import forms
from .models import Accion, User, Puerta

class AccionForm(forms.ModelForm):
    class Meta:
        model = Accion
        fields = ['usuario', 'puerta', 'fecha_actividad', 'hora_actividad']

class UserForm(forms.ModelForm):
    contraseña = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['nombre', 'apellido', 'correo', 'telefono', 'dni', 'foto', 'contraseña']

class PuertaForm(forms.ModelForm):
    class Meta:
        model = Puerta
        fields = ['codigo', 'ubicacion', 'estado_actual', 'foto']

