from django.urls import path
from admin_page.views import *
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'admin_page'

urlpatterns = [
    path('', login, name='login'),
    path('password_reset/', password_reset, name='password_reset'),
    path('reset_password/<int:admin_id>/', reset_password, name='reset_password'),
    path('index/', dashboard, name='index'),
    path('index/generar-reporte-usuario-pdf/<int:usuario_id>/', views.generar_reporte_usuarios_pdf, name='generar_reporte_usuarios_pdf'),
    path('index/usuarios/', lista_usuarios, name='usuarios'),
    path('index/usuarios/editar/', editar_usuario, name='editar_usuario'),
    path('index/usuarios/eliminar/', eliminar_usuario, name='eliminar_usuario'),
    path('index/puertas/', lista_puertas, name='puertas'),
    path('index/puertas/editar/', editar_puerta, name='editar_puerta'),
    path('index/puertas/eliminar/', eliminar_puerta, name='eliminar_puerta'),
    path('index/horarios/', horarios, name='horarios'),
    
    path('index/acciones/', views.lista_acciones, name='acciones_lista'),
    path('index/acciones/agregar/', views.agregar_accion, name='agregar_accion'),
    path('index/usuarios/<int:id>/', views.lista_acciones, name='acciones_usuario'),
    path('index/puertas/<int:id>/', views.lista_acciones, name='acciones_puerta'),
    
    path('usersapi/', views.UserView.as_view(), name='users'),
    path('usersapi/<int:user_id>/', views.UserDetailView.as_view(), name='user_detail'),
    
    path('puertaapi/', views.PuertaView.as_view(), name='puertasapi'),
    path('puertaapi/<int:puerta_id>/', views.PuertaDetailView.as_view(), name='puerta_detail'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
