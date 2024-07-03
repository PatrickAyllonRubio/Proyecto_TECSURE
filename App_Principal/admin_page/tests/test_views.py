import pytest
from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer
from admin_page.models import Administrador, User, Puerta, Horario, Accion
from admin_page.views import (
    UserView,
    UserDetailView,
    PuertaView,
    PuertaDetailView,
    login,
    password_reset,
    reset_password,
    generar_reporte_usuarios_pdf,
    dashboard,
    lista_usuarios,
    editar_usuario,
    crear_usuario,
    eliminar_usuario,
    lista_puertas,
    editar_puerta,
    crear_puerta,
    horarios,
    ver_horarios,
    lista_acciones_usuarios,
    lista_acciones_puertas,
    agregar_accion,
    perfil_administrador,
)

# Marca todas las pruebas con django_db para permitir el acceso a la base de datos
pytestmark = pytest.mark.django_db

@pytest.fixture
def admin_user():
    # Crea un administrador de prueba
    return mixer.blend(Administrador)

@pytest.fixture
def user():
    # Crea un usuario de prueba
    return mixer.blend(User)

@pytest.fixture
def puerta():
    # Crea una puerta de prueba
    return mixer.blend(Puerta)

@pytest.fixture
def rf():
    # Crea una instancia de RequestFactory para simular peticiones HTTP
    return RequestFactory()

# Pruebas para las vistas de usuarios
def test_user_view_get(rf):
    request = rf.get('/api/users/')
    response = UserView.as_view()(request)
    assert response.status_code == 200

# Pruebas para las vistas de detalle de usuario
def test_user_detail_view_get(rf, user):
    request = rf.get(f'/api/users/{user.id}/')
    response = UserDetailView.as_view()(request, user_id=user.id)
    assert response.status_code == 200


def test_user_detail_view_delete(rf, user):
    request = rf.delete(f'/api/users/{user.id}/')
    response = UserDetailView.as_view()(request, user_id=user.id)
    assert response.status_code == 204

# Pruebas para las vistas de puertas
def test_puerta_view_get(rf):
    request = rf.get('/api/puertas/')
    response = PuertaView.as_view()(request)
    assert response.status_code == 200

# Pruebas para las vistas de detalle de puerta
def test_puerta_detail_view_get(rf, puerta):
    request = rf.get(f'/api/puertas/{puerta.id}/')
    response = PuertaDetailView.as_view()(request, puerta_id=puerta.id)
    assert response.status_code == 200

def test_puerta_detail_view_delete(rf, puerta):
    request = rf.delete(f'/api/puertas/{puerta.id}/')
    response = PuertaDetailView.as_view()(request, puerta_id=puerta.id)
    assert response.status_code == 204

# Pruebas para la vista de inicio de sesión
def test_login_view_get(rf):
    request = rf.get('/login/')
    response = login(request)
    assert response.status_code == 200

# Pruebas para la vista de reseteo de contraseña
def test_password_reset_view_get(rf):
    request = rf.get('/password_reset/')
    response = password_reset(request)
    assert response.status_code == 200

# Pruebas para la vista de restablecimiento de contraseña
def test_reset_password_view_get(rf, admin_user):
    request = rf.get(f'/reset_password/{admin_user.id}/')
    response = reset_password(request, admin_id=admin_user.id)
    assert response.status_code == 200

# Pruebas para la vista de generación de reporte de usuarios en PDF
def test_generar_reporte_usuarios_pdf_view(rf, user):
    request = rf.get(f'/generar_reporte_usuarios_pdf/{user.id}/')
    response = generar_reporte_usuarios_pdf(request, usuario_id=user.id)
    assert response.status_code == 200

# Pruebas para la vista de dashboard
def test_dashboard_view(rf, admin_user):
    request = rf.get('/dashboard/')
    request.session = {'admin_id': admin_user.id}
    response = dashboard(request)
    assert response.status_code == 200

# Pruebas para la vista de lista de usuarios
def test_lista_usuarios_view_get(rf, admin_user):
    request = rf.get('/lista_usuarios/')
    request.session = {'admin_id': admin_user.id}
    response = lista_usuarios(request)
    assert response.status_code == 200

# Pruebas para la vista de edición de usuario
def test_editar_usuario_view_get(rf, admin_user, user):
    request = rf.get('/editar_usuario/')
    request.session = {'admin_id': admin_user.id}
    request.GET = {'id': user.id}
    response = editar_usuario(request)
    assert response.status_code == 200

# Pruebas para la vista de creación de usuario
def test_crear_usuario_view_get(rf, admin_user):
    request = rf.get('/crear_usuario/')
    request.session = {'admin_id': admin_user.id}
    response = crear_usuario(request)
    assert response.status_code == 200


# Pruebas para la vista de eliminación de usuario
def test_eliminar_usuario_view_get(rf, admin_user, user):
    request = rf.get('/eliminar_usuario/')
    request.GET = {'id': user.id}
    request.session = {'admin_id': admin_user.id}
    response = eliminar_usuario(request)
    assert response.status_code == 302  # Redireccionamiento exitoso

# Pruebas para la vista de lista de puertas
def test_lista_puertas_view_get(rf, admin_user):
    request = rf.get('/lista_puertas/')
    request.session = {'admin_id': admin_user.id}
    response = lista_puertas(request)
    assert response.status_code == 200

# Pruebas para la vista de edición de puerta
def test_editar_puerta_view_get(rf, admin_user, puerta):
    request = rf.get('/editar_puerta/')
    request.session = {'admin_id': admin_user.id}
    request.GET = {'id': puerta.id}
    response = editar_puerta(request)
    assert response.status_code == 200

# Pruebas para la vista de creación de puerta
def test_crear_puerta_view_get(rf, admin_user):
    request = rf.get('/crear_puerta/')
    request.session = {'admin_id': admin_user.id}
    response = crear_puerta(request)
    assert response.status_code == 200


# Pruebas para la vista de horarios
def test_horarios_view_get(rf, admin_user):
    request = rf.get('/horarios/')
    request.session = {'admin_id': admin_user.id}
    response = horarios(request)
    assert response.status_code == 200

# Pruebas para la vista de ver horarios de usuario
def test_ver_horarios_view_get(rf, admin_user, user):
    request = rf.get(f'/ver_horarios/{user.id}/')
    request.session = {'admin_id': admin_user.id}
    response = ver_horarios(request, user_id=user.id)
    assert response.status_code == 200

# Pruebas para la vista de lista de acciones de usuarios
def test_lista_acciones_usuarios_view_get(rf, admin_user):
    request = rf.get('/lista_acciones_usuarios/')
    request.session = {'admin_id': admin_user.id}
    response = lista_acciones_usuarios(request)
    assert response.status_code == 200

# Pruebas para la vista de lista de acciones de puertas
def test_lista_acciones_puertas_view_get(rf, admin_user):
    request = rf.get('/lista_acciones_puertas/')
    request.session = {'admin_id': admin_user.id}
    response = lista_acciones_puertas(request)
    assert response.status_code == 200

# Pruebas para la vista de agregar acción de usuario
def test_agregar_accion_view_get(rf, admin_user, user, puerta):
    request = rf.get('/agregar_accion/')
    request.session = {'admin_id': admin_user.id}
    request.GET = {'user_id': user.id, 'puerta_id': puerta.id}
    response = agregar_accion(request)
    assert response.status_code == 200

# Pruebas para la vista de perfil de administrador
def test_perfil_administrador_view_get(rf, admin_user):
    request = rf.get('/perfil_administrador/')
    request.session = {'admin_id': admin_user.id}
    response = perfil_administrador(request)
    assert response.status_code == 200



