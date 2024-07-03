import pytest
from django.utils import timezone
from admin_page.models import User, Administrador, RegistroUsuario, Puerta, Horario, Accion

@pytest.mark.django_db
class TestModels:

    def test_user_creation(self):
        user = User.objects.create(
            nombre="Juan",
            apellido="Pérez",
            correo="juan.perez@example.com",
            telefono="1234567890",
            dni="12345678A",
            contraseña="supersecurepassword"
        )
        assert user.nombre == "Juan"
        assert user.apellido == "Pérez"
        assert user.correo == "juan.perez@example.com"
        assert str(user) == "Juan Pérez"

    def test_administrador_creation(self):
        admin = Administrador.objects.create(
            nombre="Ana",
            apellido="García",
            correo="ana.garcia@example.com",
            telefono="0987654321",
            dni="87654321B",
            contraseña="securepassword"
        )
        assert admin.nombre == "Ana"
        assert admin.apellido == "García"
        assert admin.correo == "ana.garcia@example.com"
        assert str(admin) == "Ana García"

    def test_puerta_creation(self):
        puerta = Puerta.objects.create(
            codigo="P001",
            ubicacion="Entrada Principal",
            estado_actual="Abierta"
        )
        assert puerta.codigo == "P001"
        assert puerta.ubicacion == "Entrada Principal"
        assert str(puerta) == "Puerta P001 en Entrada Principal"

    def test_registro_usuario_creation(self, user, puerta):
        hora_ingreso = timezone.now()
        hora_salida = hora_ingreso + timezone.timedelta(hours=1)
        registro = RegistroUsuario.objects.create(
            user=user,
            puerta=puerta,
            hora_ingreso=hora_ingreso,
            hora_salida=hora_salida
        )
        assert registro.user == user
        assert registro.puerta == puerta
        assert registro.tiempo_total == timezone.timedelta(hours=1)
        assert str(registro) == f"Registro de {user.nombre} {user.apellido} en {puerta}"

    def test_horario_creation(self, user, puerta):
        horario = Horario.objects.create(
            user=user,
            puerta=puerta,
            dia_semana='lunes',
            hora_inicio="08:00:00",
            hora_fin="10:00:00"
        )
        assert horario.user == user
        assert horario.puerta == puerta
        assert horario.dia_semana == 'lunes'
        assert str(horario) == f"Horario de {user.nombre} {user.apellido} para la puerta {puerta.codigo} el lunes desde 08:00:00 hasta 10:00:00"

    def test_accion_creation(self, user, puerta):
        accion = Accion.objects.create(
            usuario=user,
            puerta=puerta,
            fecha_actividad=timezone.now().date(),
            hora_actividad="12:00:00"
        )
        assert accion.usuario == user
        assert accion.puerta == puerta
        assert str(accion) == f"Accion de {user.nombre} {user.apellido} en Puerta {puerta.codigo}"

@pytest.fixture
def user():
    return User.objects.create(
        nombre="Carlos",
        apellido="Sánchez",
        correo="carlos.sanchez@example.com",
        telefono="5551234567",
        dni="98765432C",
        contraseña="anothersecurepassword"
    )

@pytest.fixture
def puerta():
    return Puerta.objects.create(
        codigo="P002",
        ubicacion="Salida Emergencia",
        estado_actual="Cerrada"
    )
