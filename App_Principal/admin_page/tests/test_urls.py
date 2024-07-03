import pytest
from django.test import Client
from django.urls import reverse

from admin_page.models import Puerta, User

@pytest.mark.django_db
def test_login_url(client: Client):
    response = client.get(reverse('admin_page:login'))
    assert response.status_code == 200  # Verifica que la página de login responda con 200 OK

@pytest.mark.django_db
def test_password_reset_url(client: Client):
    response = client.get(reverse('admin_page:password_reset'))
    assert response.status_code == 200  # Verifica que la página de reseteo de contraseña responda con 200 OK

@pytest.mark.django_db
def test_reset_password_url(client: Client):
    # Suponiendo que tienes un admin_id válido en tu base de datos para esta prueba
    response = client.get(reverse('admin_page:reset_password', kwargs={'admin_id': 1}))
    assert response.status_code == 200  # Verifica que la página de reseteo de contraseña por ID de admin responda con 200 OK

@pytest.mark.django_db
def test_dashboard_url(client: Client):
    response = client.get(reverse('admin_page:index'))
    assert response.status_code == 302  # Verifica que la vista redirige (código 302)
    assert response.url == '/'  # Verifica que redirige a la página principal

@pytest.mark.django_db
def test_perfil_administrador_url(client: Client):
    url = reverse('admin_page:perfil_administrador')
    response = client.get(url)
    assert response.status_code == 302  # Verifica que la vista redirige (código 302)
    assert response.url == '/'  # Verifica que redirige a la página principal

@pytest.mark.django_db
def test_update_admin_photo_url(client: Client):
    url = reverse('admin_page:update_admin_photo')
    response = client.get(url)
    assert response.status_code == 302  # Verifica que redirige (código 302)

@pytest.mark.django_db
def test_generar_reporte_usuarios_pdf_url(client: Client):
    response = client.get(reverse('admin_page:generar_reporte_usuarios_pdf', kwargs={'usuario_id': 1}))
    assert response.status_code == 404  # Verifica que la vista responda con código 404

@pytest.mark.django_db
def test_crear_usuario_url(client: Client):
    url = reverse('admin_page:crear_usuario')
    response = client.get(url)
    assert response.status_code == 302  # Verifica que redirige (código 302)

@pytest.mark.django_db
def test_crear_puerta_url(client: Client):
    url = reverse('admin_page:crear_puerta')
    response = client.get(url)
    assert response.status_code == 302  # Verifica que redirige (código 302)

@pytest.mark.django_db
def test_usersapi_url(client: Client):
    response = client.get(reverse('admin_page:usersapi'))
    assert response.status_code == 200  # Verifica que la API de usuarios responda con 200 OK

@pytest.mark.django_db
def test_puerta_detail_url(client: Client):
    puerta = Puerta.objects.create(codigo='puerta1')
    response = client.get(reverse('admin_page:puerta_detail', kwargs={'puerta_id': puerta.id}))
    assert response.status_code == 200  # Verifica que la vista responda con código 200 OK
