# admin_page/decorators.py
from functools import wraps
from django.shortcuts import redirect
from .models import Administrador

def include_admin_data(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        admin_id = request.session.get('admin_id')
        if admin_id:
            try:
                administrador = Administrador.objects.get(id=admin_id)
                request.admin_data = administrador
            except Administrador.DoesNotExist:
                return redirect('admin_page:login')
        else:
            return redirect('admin_page:login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
