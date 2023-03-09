"""marvel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from characters.views import CharacterViewSet

router_character = DefaultRouter(trailing_slash=False)

router_character.register('api', CharacterViewSet, basename='get_and_store_character')
router_character.register('api', CharacterViewSet, basename='get_and_store_comics_and_teammates')
router_character.register('api', CharacterViewSet, basename='get_teammates')
router_character.register('api', CharacterViewSet, basename='get_all_characters')
router_character.register('api', CharacterViewSet, basename='get_all_comics')
router_character.register('api', CharacterViewSet, basename='get_character')

urlpatterns = [
    path('', include((router_character.urls, 'character'), namespace='character')),
   path('admin/', admin.site.urls),
]
