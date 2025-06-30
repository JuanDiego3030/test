from django.shortcuts import render
from .models import Prueba

# Create your views here.
def index(request):
    # Obtener parámetros de búsqueda y filtro
    busqueda = request.GET.get('busqueda', '').strip()
    socio = request.GET.get('socio', '')

    pruebas = Prueba.objects.all()

    if busqueda:
        pruebas = pruebas.filter(nombre__icontains=busqueda)
    if socio in ['si', 'no']:
        pruebas = pruebas.filter(socio=(socio == 'si'))

    return render(request, 'index.html', {
        'pruebas': pruebas,
        'busqueda': busqueda,
        'socio': socio,
    })
