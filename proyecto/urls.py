from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('app1.urls')),
    path('app2/', include('app2.urls')),
]