from django.db import models
from datetime import timedelta

class User(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    dni = models.CharField(max_length=20, unique=True)
    foto = models.ImageField(upload_to='user_photos/', blank=True, null=True)
    contraseña = models.CharField(max_length=128)
    huella = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Administrador(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    dni = models.CharField(max_length=20, unique=True)
    foto = models.ImageField(upload_to='admin_photos/', blank=True, null=True)
    contraseña = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"



class Puerta(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    ubicacion = models.CharField(max_length=100)
    estado_actual = models.CharField(max_length=50)
    foto = models.ImageField(upload_to='puerta_photos/', blank=True, null=True)

    def __str__(self):
        return f"Puerta {self.codigo} en {self.ubicacion}"

class Horario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='horarios')
    puerta = models.ForeignKey(Puerta, on_delete=models.CASCADE)
    dia_semana = models.CharField(max_length=10, choices=[
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sábado')
    ])
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"Horario de {self.user.nombre} {self.user.apellido} para la puerta {self.puerta.codigo} el {self.dia_semana} desde {self.hora_inicio} hasta {self.hora_fin}"

class Accion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    puerta = models.ForeignKey(Puerta, on_delete=models.CASCADE)
    fecha_actividad = models.DateField()
    hora_actividad = models.TimeField()

    def __str__(self):
        return f"Accion de {self.usuario.nombre} {self.usuario.apellido} en Puerta {self.puerta.codigo}"
    
class RegistroUsuario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registros')
    puerta = models.ForeignKey('Puerta', on_delete=models.CASCADE, related_name='registros')
    hora_ingreso = models.DateTimeField()
    hora_salida = models.DateTimeField()

    @property
    def tiempo_total(self):
        if self.hora_ingreso and self.hora_salida:
            return self.hora_salida - self.hora_ingreso
        return timedelta()

    def __str__(self):
        return f"Registro de {self.user.nombre} {self.user.apellido} en {self.puerta}"