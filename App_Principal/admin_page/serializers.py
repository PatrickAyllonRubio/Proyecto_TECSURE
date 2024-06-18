from rest_framework import serializers
from .models import User, Puerta

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'nombre', 'apellido', 'correo', 'telefono', 'dni', 'foto', 'contraseña')

class PuertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Puerta
        fields = ('id', 'codigo', 'ubicacion', 'estado_actual', 'foto')
