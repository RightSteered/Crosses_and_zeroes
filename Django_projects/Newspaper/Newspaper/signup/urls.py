from django.urls import path, include
from .views import upgrade

urlpatterns = [
    path('', include('protect.urls')),
    path('upgrade/', upgrade, name='upgrade')
]