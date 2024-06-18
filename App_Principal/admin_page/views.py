from django.shortcuts import render, redirect
from .models import Administrador, User, Puerta, Horario, RegistroUsuario, Accion
from .decorators import include_admin_data
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from datetime import datetime
from reportlab.pdfgen import canvas
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from .models import User, Puerta
from .serializers import UserSerializer, PuertaSerializer
from .forms import AccionForm, UserForm, PuertaForm

class UserView(APIView):

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):

    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, user_id):
        user = User.objects.get(pk=user_id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        user = User.objects.get(pk=user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PuertaView(APIView):

    def get(self, request):
        puertas = Puerta.objects.all()
        serializer = PuertaSerializer(puertas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PuertaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PuertaDetailView(APIView):

    def get(self, request, puerta_id):
        puerta = Puerta.objects.get(pk=puerta_id)
        serializer = PuertaSerializer(puerta)
        return Response(serializer.data)

    def put(self, request, puerta_id):
        puerta = Puerta.objects.get(pk=puerta_id)
        serializer = PuertaSerializer(puerta, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, puerta_id):
        puerta = Puerta.objects.get(pk=puerta_id)
        puerta.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            administrador = Administrador.objects.get(nombre=username)
            if check_password(password, administrador.contraseña):
                request.session['admin_id'] = administrador.id
                return redirect('admin_page:index')
            else:
                error_message = 'El nombre de usuario o la contraseña son incorrectos.'
                return render(request, 'admin_page/login_page.html', {'error_message': error_message})
        except Administrador.DoesNotExist:
            error_message = 'El nombre de usuario o la contraseña son incorrectos.'
            return render(request, 'admin_page/login_page.html', {'error_message': error_message})

    return render(request, 'admin_page/login_page.html')

def password_reset(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        try:
            administrador = Administrador.objects.get(nombre=username, correo=email)
            return redirect('admin_page:reset_password', admin_id=administrador.id)
        except Administrador.DoesNotExist:
            messages.error(request, 'No se encontró una cuenta con ese nombre de usuario y correo.')

    return render(request, 'admin_page/login_page.html')

def reset_password(request, admin_id):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password == confirm_password:
            try:
                administrador = Administrador.objects.get(id=admin_id)
                administrador.contraseña = make_password(new_password)
                administrador.save()
                messages.success(request, 'Tu contraseña ha sido restablecida con éxito.')
                return redirect('admin_page:login')
            except Administrador.DoesNotExist:
                messages.error(request, 'Error al restablecer la contraseña. Intenta nuevamente.')
        else:
            messages.error(request, 'Las contraseñas no coinciden.')
    
    return render(request, 'admin_page/reset_password.html', {'admin_id': admin_id})

@include_admin_data
def index(request):
    admin_id = request.session.get('admin_id')
    if admin_id:
        try:
            administrador = Administrador.objects.get(id=admin_id)
            print(f"Administrador encontrado: {administrador.nombre} {administrador.apellido}")  # Debugging
            return render(request, 'admin_page/index.html', {'administrador': administrador})
        except Administrador.DoesNotExist:
            print("Administrador no encontrado.")  # Debugging
            return redirect('admin_page:login')
    else:
        print("No admin_id en la sesión.")  # Debugging
        return redirect('admin_page:login')

def generar_reporte_usuarios_pdf(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    registros = RegistroUsuario.objects.filter(user=usuario)

    # Creación del archivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_usuario_{usuario_id}.pdf"'

    # Generación del contenido del PDF
    p = canvas.Canvas(response)
    p.drawString(100, 800, f"Reporte de Usuario: {usuario.username}")

    y = 750
    for registro in registros:
        y -= 20
        p.drawString(100, y, f"Fecha de ingreso: {registro.hora_ingreso}")
        p.drawString(300, y, f"Fecha de salida: {registro.hora_salida}")

    p.showPage()
    p.save()

    return response

def dashboard(request):
    admin_id = request.session.get('admin_id')
    if admin_id:
        try:
            administrador = Administrador.objects.get(id=admin_id)
            total_usuarios = User.objects.count()
            total_puertas = Puerta.objects.count()
            total_registros = RegistroUsuario.objects.count()
            
            # Obtener la lista de usuarios
            usuarios = User.objects.all()

            # Datos para el gráfico de acciones
            current_year = datetime.now().year
            months = [f'{i:02d}' for i in range(1, 13)]
            actions_data = [
                RegistroUsuario.objects.filter(hora_ingreso__year=current_year, hora_ingreso__month=month).count()
                for month in range(1, 13)
            ]
            
            context = {
                'administrador': administrador,
                'total_usuarios': total_usuarios,
                'total_puertas': total_puertas,
                'total_registros': total_registros,
                'months': months,
                'actions_data': actions_data,
                'usuarios': usuarios  # Pasar la lista de usuarios al contexto
            }
            return render(request, 'admin_page/dashboard.html', context)
        except Administrador.DoesNotExist:
            return redirect('admin_page:login')
    else:
        return redirect('admin_page:login')

@include_admin_data
def lista_usuarios(request):
    admin_id = request.session.get('admin_id')
    if admin_id:
        administrador = Administrador.objects.get(id=admin_id)
    else:
        return redirect('admin_page:login')
    query = request.GET.get('q')
    
    if query:
        usuarios = User.objects.filter(dni__icontains=query)
    else:
        usuarios = User.objects.all()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        usuarios_data = [
            {
                'id': usuario.id,
                'nombre': usuario.nombre,
                'apellido': usuario.apellido,
                'correo': usuario.correo,
                'telefono': usuario.telefono,
                'dni': usuario.dni,
                'foto': usuario.foto.url if usuario.foto else ''
            }
            for usuario in usuarios
        ]
        return JsonResponse(usuarios_data, safe=False)
    
    return render(request, 'admin_page/usuarios.html', {'usuarios': usuarios, 'administrador': administrador})

@include_admin_data
def editar_usuario(request):
    admin_id = request.session.get('admin_id')
    if admin_id:
        administrador = Administrador.objects.get(id=admin_id)
    else:
        # Si no hay sesión de administrador, redirige a la página de inicio de sesión
        return redirect('admin_page:login')
    if request.method == 'GET':
        user_id = request.GET.get('id')
        user = User.objects.get(id=user_id)
        return render(request, 'admin_page/editar_usuario.html', {'user': user})
    elif request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        user.nombre = request.POST.get('nombre')
        user.apellido = request.POST.get('apellido')
        user.correo = request.POST.get('correo')
        user.telefono = request.POST.get('telefono')
        user.dni = request.POST.get('dni')
        if request.FILES.get('foto'):
            user.foto = request.FILES['foto']
        user.save()
        return redirect('admin_page:usuarios')
    else:
        return HttpResponse(status=405)
    
def crear_usuario(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_page:index')
    else:
        form = UserForm()
    return render(request, 'admin_page/crear_usuario.html', {'form': form})
    
@include_admin_data
def eliminar_usuario(request):
    if request.method == 'GET':
        user_id = request.GET.get('id')
        user = User.objects.get(id=user_id)
        user.delete()
        return redirect('admin_page:usuarios')

@include_admin_data
def lista_puertas(request):
    admin_id = request.session.get('admin_id')
    if admin_id:
        administrador = Administrador.objects.get(id=admin_id)
    else:
        # Si no hay sesión de administrador, redirige a la página de inicio de sesión
        return redirect('admin_page:login')
    
    query = request.GET.get('q')
    
    if query:
        puertas = Puerta.objects.filter(codigo__icontains=query)
    else:
        puertas = Puerta.objects.all()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        puertas_data = [
            {
                'id': puerta.id,
                'codigo': puerta.codigo,
                'ubicacion': puerta.ubicacion,
                'estado': puerta.estado_actual,
                'foto': puerta.foto.url if puerta.foto else ''
            }
            for puerta in puertas
        ]
        return JsonResponse(puertas_data, safe=False)
    
    return render(request, 'admin_page/puertas.html', {'puertas': puertas, 'administrador': administrador})


@include_admin_data
def editar_puerta(request):
    admin_id = request.session.get('admin_id')
    if admin_id:
        administrador = Administrador.objects.get(id=admin_id)
    else:
        # Si no hay sesión de administrador, redirige a la página de inicio de sesión
        return redirect('admin_page:login')
    if request.method == 'GET':
        puerta_id = request.GET.get('id')
        puerta = Puerta.objects.get(id=puerta_id)
        return render(request, 'admin_page/editar_puerta.html', {'puerta': puerta})
    elif request.method == 'POST':
        puerta_id = request.POST.get('puerta_id')
        puerta = Puerta.objects.get(id=puerta_id)
        puerta.codigo = request.POST.get('codigo')
        puerta.ubicacion = request.POST.get('ubicacion')
        puerta.estado_actual = request.POST.get('estado_actual')
        if request.FILES.get('foto'):
            puerta.foto = request.FILES['foto']
        puerta.save()
        return redirect('admin_page:puertas')
    else:
        return HttpResponse(status=405)
    
@include_admin_data
def eliminar_puerta(request):
    if request.method == 'GET':
        puerta_id = request.GET.get('id')
        puerta = Puerta.objects.get(id=puerta_id)
        puerta.delete()
        return redirect('admin_page:puertas')

def crear_puerta(request):
    if request.method == 'POST':
        form = PuertaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_page:index')
    else:
        form = PuertaForm()
    return render(request, 'admin_page/crear_puerta.html', {'form': form})

@include_admin_data
def horarios(request):
    admin_id = request.session.get('admin_id')
    if admin_id:
        administrador = Administrador.objects.get(id=admin_id)
    else:
        # Si no hay sesión de administrador, redirige a la página de inicio de sesión
        return redirect('admin_page:login')
    if request.method == 'POST':
        user = request.POST.get('user', '').strip()
        door = request.POST.get('door', '').strip()
        day = request.POST.get('day', '').strip().lower()
        time = request.POST.get('time', '').strip()

        if not day:
            return render(request, "admin_page/horarios.html", {'error': 'El día es obligatorio para la búsqueda.'})
        
        horarios = Horario.objects.filter(dia_semana__icontains=day)

        if user:
            horarios = horarios.filter(user__nombre__icontains=user)
        
        if door:
            horarios = horarios.filter(puerta__codigo__icontains=door)

        if time:
            horarios = horarios.filter(hora_inicio__lte=time, hora_fin__gte=time)

        users = User.objects.all()
        doors = Puerta.objects.all()
        return render(request, "admin_page/horarios.html", {'horarios': horarios, 'users': users, 'doors': doors})

    users = User.objects.all()
    doors = Puerta.objects.all()
    return render(request, "admin_page/horarios.html", {'users': users, 'doors': doors, 'administrador': administrador})

def lista_acciones(request, id=None):
    if id is not None:
        id = int(id)  # Convertir el id a entero si es necesario

        if isinstance(id, int):
            # Filtrar acciones por usuario o puerta según el tipo de id
            acciones = Accion.objects.filter(usuario_id=id)
        else:
            # Si id no es un entero, manejar el caso según tu lógica
            acciones = Accion.objects.all()
    else:
        acciones = Accion.objects.all()

    context = {'acciones': acciones}
    return render(request, 'admin_page/acciones_lista.html', context)


def agregar_accion(request):
    if request.method == 'POST':
        form = AccionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_page:acciones_lista')
    else:
        form = AccionForm()
    
    context = {'form': form}
    return render(request, 'admin_page/agregar_accion.html', context)