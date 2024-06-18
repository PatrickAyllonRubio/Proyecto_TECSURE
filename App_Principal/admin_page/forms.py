# forms.py

from django import forms
from .models import Accion

class AccionForm(forms.ModelForm):
    class Meta:
        model = Accion
        fields = ['usuario', 'puerta', 'fecha_actividad', 'hora_actividad']
