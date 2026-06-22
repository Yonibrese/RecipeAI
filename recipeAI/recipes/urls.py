from django.urls import path
from . import views

urlpatterns = [
    #auth views
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # recipe views
    path('', views.recipe_list, name='recipe_list'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/new/', views.recipe_create, name='recipe_create'),
    path('recipe/<int:pk>/edit/', views.recipe_edit, name='recipe_edit'),
    path('recipe/<int:pk>/delete/', views.recipe_delete, name='recipe_delete'),
    # AI Path
    path('recipe/generate/', views.ai_recipe_generator, name='generate_recipe'),
    path('recipe/api/enhance-instructions/', views.enhance_instructions, name='api_enhance_instructions')
]