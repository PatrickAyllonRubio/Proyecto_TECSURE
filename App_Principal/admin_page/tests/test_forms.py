import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from admin_page.forms import AccionForm, UserForm, PuertaForm
from admin_page.models import User, Puerta

@pytest.fixture
def mock_image():
    # Crea un archivo de imagen falso para pruebas
    return SimpleUploadedFile('test_image.jpg', b'content', content_type='image/jpeg')

@pytest.fixture
def mock_user_data(mock_image):
    # Datos de ejemplo para el formulario de usuario
    return {
        'nombre': 'Test',
        'apellido': 'User',
        'correo': 'test@example.com',
        'telefono': '123456789',
        'dni': '12345678A',
        'foto': mock_image,
        'contraseña': 'testpassword'
    }

@pytest.fixture
def mock_puerta_data():
    # Datos de ejemplo para el formulario de puerta
    return {
        'codigo': 'Puerta1',
        'ubicacion': 'Ubicacion1',
        'estado_actual': 'Abierta'
    }

@pytest.mark.django_db
def test_accion_form_invalid():
    form_data = {
        'usuario': 1,
        'puerta': 1,
        'fecha_actividad': '2024-07-01',  # fecha_actividad es requerido
        # Falta hora_actividad
    }
    form = AccionForm(data=form_data)
    assert not form.is_valid()

@pytest.mark.django_db
def test_user_form_valid(mock_user_data):
    form = UserForm(data=mock_user_data)
    assert form.is_valid()

@pytest.mark.django_db
def test_user_form_invalid():
    form_data = {
        'nombre': 'Test',
        'apellido': 'User',
        'correo': 'invalidemail',  # correo inválido
        'telefono': '123456789',
        'dni': '12345678A',
        'contraseña': 'testpassword'
    }
    form = UserForm(data=form_data)
    assert not form.is_valid()
    assert 'correo' in form.errors

@pytest.mark.django_db
def test_puerta_form_valid(mock_puerta_data):
    form = PuertaForm(data=mock_puerta_data)
    assert form.is_valid()

@pytest.mark.django_db
def test_puerta_form_invalid():
    form_data = {
        'codigo': 'Puerta1',
        'ubicacion': '',  # ubicacion no puede estar vacío
        'estado_actual': 'Abierta'
    }
    form = PuertaForm(data=form_data)
    assert not form.is_valid()
