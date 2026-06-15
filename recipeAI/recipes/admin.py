from django.contrib import admin
from . import models

class RecipeIngredientInline(admin.TabularInline):
    model = models.RecipeIngredient
    extra = 3
    autocomplete_fields = ['ingredient']

@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at']
    search_fields = ['title', 'description', 'instructions']
    inlines = [RecipeIngredientInline]

@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']