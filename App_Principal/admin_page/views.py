from datetime import datetime
import calendar
import locale
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Q
from django.contrib.auth.hashers import check_password, make_password
from django.views.decorators.csrf import csrf_exempt
from django.db.models.functions import TruncMonth
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .decorators import include_admin_data
from .models import Administrador, User, Puerta, Horario, Accion
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
    # Obtener el usuario y sus datos asociados
    usuario = get_object_or_404(User, id=usuario_id)
    acciones = Accion.objects.filter(usuario=usuario)
    horarios = Horario.objects.filter(user=usuario)
    
    # Creación del archivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_usuario_{usuario_id}.pdf"'

    # Inicializar el lienzo del PDF
    p = canvas.Canvas(response, pagesize=letter)
    
    # Configurar fuentes y estilos
    p.setFont("Helvetica-Bold", 16)
    p.setFillColor(colors.black)

    # Título del reporte
    p.drawCentredString(300, 750, "Reporte de Usuario")
    p.setFont("Helvetica", 12)

    # Datos personales del usuario
    p.drawString(100, 720, "Datos Personales:")
    p.drawString(100, 700, f"Nombre: {usuario.nombre} {usuario.apellido}")
    p.drawString(100, 680, f"Correo electrónico: {usuario.correo}")
    p.drawString(100, 660, f"Teléfono: {usuario.telefono}")
    p.drawString(100, 640, f"DNI: {usuario.dni}")

    if usuario.foto:
        try:
            foto_path = usuario.foto.path
            p.drawImage(foto_path, 400, 640, width=100, height=100, mask='auto')
        except:
            pass

    p.line(100, 620, 500, 620)

    p.drawString(100, 600, "Horarios Asignados:")
    y = 580
    for horario in horarios:
        p.drawString(100, y, f"Día: {horario.get_dia_semana_display()}")
        p.drawString(250, y, f"Horario: {horario.hora_inicio.strftime('%H:%M')} - {horario.hora_fin.strftime('%H:%M')}")
        p.drawString(400, y, f"Puerta: {horario.puerta.codigo}")
        y -= 20

    p.line(100, y - 10, 500, y - 10)

    p.drawString(100, y - 30, "Acciones Registradas:")
    y -= 50
    for accion in acciones:
        p.drawString(100, y, f"Fecha: {accion.fecha_actividad.strftime('%d/%m/%Y')}")
        p.drawString(250, y, f"Hora: {accion.hora_actividad.strftime('%H:%M')}")
        p.drawString(400, y, f"Puerta: {accion.puerta.codigo}")
        y -= 20

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
            total_acciones = Accion.objects.count()

            usuarios = User.objects.all()

            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')    

            actions_by_month = Accion.objects.annotate(month=TruncMonth('fecha_actividad')).values('month').annotate(count=Count('id')).order_by('month')

            current_year = datetime.now().year
            months = [calendar.month_name[i] for i in range(1, 13)]
            actions_data_dict = {month: 0 for month in months}

            for action in actions_by_month:
                month_name = action['month'].strftime('%B')
                actions_data_dict[month_name] = action['count']

            actions_data = list(actions_data_dict.values())

            context = {
                'administrador': administrador,
                'total_usuarios': total_usuarios,
                'total_puertas': total_puertas,
                'total_acciones': total_acciones,
                'months': months,
                'actions_data': actions_data,
                'usuarios': usuarios
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
        return redirect('admin_page:login')
    if request.method == 'GET':
        user_id = request.GET.get('id')
        user = User.objects.get(id=user_id)
        return render(request, 'admin_page/editar_usuario.html', {'user': user, 'administrador': administrador})
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
    admin_id = request.session.get('admin_id')
    if admin_id:
        administrador = Administrador.objects.get(id=admin_id)
    else:
        return redirect('admin_page:login')
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_page:index')
    else:
        form = UserForm()
    return render(request, 'admin_page/crear_usuario.html', {'form': form , 'administrador': administrador})

    
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
        return redirect('admin_page:login')
    if request.method == 'GET':
        puerta_id = request.GET.get('id')
        puerta = Puerta.objects.get(id=puerta_id)
        return render(request, 'admin_page/editar_puerta.html', {'puerta': puerta, 'administrador': administrador})
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

@include_admin_data
def crear_puerta(request):
    admin_id = request.session.get('admin_id')
    if admin_id:
        administrador = Administrador.objects.get(id=admin_id)
    else:
        return redirect('admin_page:login')
    if request.method == 'POST':
        form = PuertaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_page:index')
    else:
        form = PuertaForm()
    return render(request, 'admin_page/crear_puerta.html', {'form': form,'administrador': administrador})


def horarios(request):
    admin_id = request.session.get('admin_id')
    if admin_id:
        administrador = Administrador.objects.get(id=admin_id)
    else:
        return redirect('admin_page:login')
    
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        search_user = request.GET.get('q', '').strip()
        
        # Filtra los usuarios por nombre si hay un término de búsqueda
        if search_user:
            users = User.objects.filter(Q(nombre__icontains=search_user) | Q(apellido__icontains=search_user))
        else:
            users = User.objects.all()
        
        # Obtén los horarios de los usuarios encontrados o todos los usuarios si no hay búsqueda
        horarios = Horario.objects.filter(user__in=users)  # Ajusta esto según tus modelos y relaciones
        
        # Prepara los datos de los usuarios para enviar como JSON
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
            for usuario in users
        ]
        
        return JsonResponse(usuarios_data, safe=False)
    
    users = User.objects.all()
    doors = Puerta.objects.all()
    return render(request, "admin_page/horarios.html", {'users': users, 'doors': doors, 'administrador': administrador})

def ver_horarios(request, user_id):
    admin_id = request.session.get('admin_id')
    if admin_id:
        administrador = Administrador.objects.get(id=admin_id)
    else:
        return redirect('admin_page:login')
    usuario = get_object_or_404(User, id=user_id)
    horarios = Horario.objects.filter(user=usuario).order_by('dia_semana', 'hora_inicio')
    
    context = {
        'usuario': usuario,
        'horarios': horarios,
        'administrador': administrador
    }
    return render(request, 'admin_page/ver_horarios.html', context)

@include_admin_data
def lista_acciones_usuarios(request, usuario_id=None):
    admin_id = request.session.get('admin_id')
    if admin_id:
        administrador = Administrador.objects.get(id=admin_id)
    else:
        return redirect('admin_page:login')
    if usuario_id:
        usuario = get_object_or_404(User, id=usuario_id)
        acciones = Accion.objects.filter(usuario=usuario)
    else:
        acciones = Accion.objects.all()

    context = {'acciones': acciones,'administrador': administrador}
    return render(request, 'admin_page/acciones_lista_usuarios.html', context)

@include_admin_data
def lista_acciones_puertas(request, puerta_id=None):
    admin_id = request.session.get('admin_id')
    if admin_id:
        administrador = Administrador.objects.get(id=admin_id)
    else:
        return redirect('admin_page:login')
    if puerta_id:
        puerta = get_object_or_404(Puerta, id=puerta_id)
        acciones = Accion.objects.filter(puerta=puerta)
    else:
        acciones = Accion.objects.all()

    context = {'acciones': acciones,'administrador': administrador}
    return render(request, 'admin_page/acciones_lista_puertas.html', context)

@include_admin_data
def agregar_accion(request):
    admin_id = request.session.get('admin_id')
    if admin_id:
        administrador = Administrador.objects.get(id=admin_id)
    else:
        return redirect('admin_page:login')
    if request.method == 'POST':
        form = AccionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_page:index')
    else:
        form = AccionForm()
    
    context = {'form': form, 'administrador': administrador}
    return render(request, 'admin_page/agregar_accion.html', context)
 

def perfil_administrador(request):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('admin_page:login')  
    
    try:
        administrador = Administrador.objects.get(id=admin_id)
    except Administrador.DoesNotExist:
        return redirect('admin_page:login')  

    return render(request, 'admin_page/perfil_admin.html', {'administrador': administrador})

@csrf_exempt
@login_required
def update_admin_profile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            admin_id = request.session.get('admin_id')

            administrador = get_object_or_404(Administrador, id=admin_id)

            # Actualizar los campos del administrador con los datos recibidos
            administrador.nombre = data.get('nombre', administrador.nombre)
            administrador.apellido = data.get('apellido', administrador.apellido)
            administrador.correo = data.get('correo', administrador.correo)
            administrador.telefono = data.get('telefono', administrador.telefono)
            administrador.dni = data.get('dni', administrador.dni)

            administrador.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method or no data sent'})

@csrf_exempt
@login_required
def update_admin_photo(request):
    if request.method == 'POST' and request.FILES['foto']:
        try:
            admin_id = request.session.get('admin_id')
            administrador = Administrador.objects.get(id=admin_id)
            administrador.foto.delete(save=False) 

            administrador.foto = request.FILES['foto']
            administrador.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method or no file uploaded'})