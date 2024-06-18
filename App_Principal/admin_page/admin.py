from django.contrib import admin
from .models import User, Administrador, RegistroUsuario, Puerta, Horario, Accion

# Register your models here.

admin.site.register(User)
admin.site.register(Administrador)
admin.site.register(RegistroUsuario)
admin.site.register(Puerta)
admin.site.register(Horario)
admin.site.register(Accion)