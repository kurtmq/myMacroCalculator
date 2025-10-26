from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.hello_world, name='hello_world'),
    path('ingredients/', views.ingredient_list, name='ingredient_list'),
    path('ingredients/add/', views.ingredient_create, name='ingredient_create'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipes/add/', views.recipe_create, name='recipe_create'),
    path('ingredients/<int:pk>/edit/', views.ingredient_edit, name='ingredient_edit'),
    path('ingredients/<int:pk>/delete/', views.ingredient_delete, name='ingredient_delete'),
    path('recipes/<int:pk>/edit/', views.recipe_edit, name='recipe_edit'), 
    path('recipes/<int:pk>/delete/', views.recipe_delete, name='recipe_delete'),
]