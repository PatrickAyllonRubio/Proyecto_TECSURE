import os
import pytest
from io import BytesIO
from django.core.files import File
from rest_framework.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from admin_page.serializers import UserSerializer, PuertaSerializer
from admin_page.models import User, Puerta

@pytest.fixture
def mock_user_data():
    # Reemplaza 'path_to_image.png' con la ruta real a una imagen válida en tu sistema
    image_path = 'admin_page/static/imagenes/image_user.png'
    assert os.path.exists(image_path), f"No se encontró el archivo en {image_path}"

    with open(image_path, 'rb') as f:
        image_data = f.read()  # Lee los datos de la imagen
        mock_image = File(BytesIO(image_data), name=os.path.basename(image_path))

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
    return {
        'codigo': 'Puerta1',
        'ubicacion': 'Ubicacion1',
        'estado_actual': 'Abierta'
    }


@pytest.mark.django_db
def test_user_serializer_valid(mock_user_data):
    serializer = UserSerializer(data=mock_user_data)
    assert serializer.is_valid(), serializer.errors

@pytest.mark.django_db
def test_user_serializer_invalid():
    invalid_data = {
        'nombre': 'Test',
        'apellido': 'User',
        'correo': 'invalidemail',  # correo inválido
        'telefono': '123456789',
        'dni': '12345678A',
        'contraseña': 'testpassword'
    }
    serializer = UserSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert 'correo' in serializer.errors

@pytest.mark.django_db
def test_puerta_serializer_valid(mock_puerta_data):
    serializer = PuertaSerializer(data=mock_puerta_data)
    assert serializer.is_valid()
    puerta_instance = serializer.save()

    assert puerta_instance.codigo == mock_puerta_data['codigo']
    assert puerta_instance.ubicacion == mock_puerta_data['ubicacion']
    # Añade más aserciones según sea necesario para verificar que los datos se guardaron correctamente

@pytest.mark.django_db
def test_puerta_serializer_invalid():
    invalid_data = {
        'codigo': 'Puerta1',
        'ubicacion': '',  # ubicacion no puede estar vacío
        'estado_actual': 'Abierta'
    }
    serializer = PuertaSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert 'ubicacion' in serializer.errors
