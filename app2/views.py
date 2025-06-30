from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import User_admin
from .crud import crear_prueba, obtener_pruebas, eliminar_prueba


def login(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        password = request.POST.get('password', '')

        try:
            user = User_admin.objects.get(nombre=nombre)
            if user.bloqueado:
                messages.error(request, 'Usuario bloqueado')
            elif user.password == password or check_password(password, user.password):
                request.session['user_admin_id'] = user.id
                return redirect('control')
            else:
                messages.error(request, 'Contraseña incorrecta')
            return render(request, 'login.html')
        except User_admin.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')
            return render(request, 'login.html')

    return render(request, 'login.html')


def control(request):
    user_id = request.session.get('user_admin_id')
    if not user_id:
        messages.error(request, 'Debe iniciar sesión primero')
        return redirect('login')
    try:
        user = User_admin.objects.get(id=user_id)
    except User_admin.DoesNotExist:
        messages.error(request, 'Usuario no encontrado')
        return redirect('login')

    # CRUD Prueba
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        fecha = request.POST.get('fecha')
        socio = request.POST.get('socio') == 'on'
        if nombre and fecha:
            crear_prueba(nombre, fecha, socio)
            messages.success(request, 'Registro creado correctamente')
        else:
            messages.error(request, 'Todos los campos son obligatorios')

    if request.method == 'POST' and 'eliminar_id' in request.POST:
        eliminar_prueba(request.POST.get('eliminar_id'))
        messages.success(request, 'Registro eliminado')

    pruebas = obtener_pruebas()
    return render(request, 'control.html', {'pruebas': pruebas})