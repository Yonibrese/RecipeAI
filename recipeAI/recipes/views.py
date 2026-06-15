from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .ai_services import generate_ai_recipe
from . import models, forms

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('recipe_list')  # Redirect to a home page or dashboard after signup
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('recipe_list')  # Redirect to a home page or dashboard after login
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('recipe_list')
    
    # Fallback for standard links
    logout(request)
    return redirect('login')

# Recipe views
def recipe_list(request):
    recipes = models.Recipe.objects.all().order_by('-created_at')
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

def recipe_detail(request, pk):
    recipe = get_object_or_404(models.Recipe, pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

@login_required
def recipe_create(request):
    if request.method == 'POST':
        form = forms.recipeForm(request.POST)
        formset = forms.recipeIngredientFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            formset.instance = recipe
            formset.save()

            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = forms.recipeForm()
        formset = forms.recipeIngredientFormSet()
    return render(request, 'recipes/recipe_form.html', {'form': form, 'formset': formset})

@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(models.Recipe, pk=pk)
    if recipe.author != request.user:
        raise PermissionDenied("You do not have permission to edit this recipe.")
    
    if request.method == 'POST':
        form = forms.recipeForm(request.POST, instance=recipe)
        formset = forms.recipeIngredientFormSet(request.POST, instance=recipe)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = forms.recipeForm(instance=recipe)
        formset = forms.recipeIngredientFormSet(instance=recipe)
    return render(request, 'recipes/recipe_form.html', {'form': form, 'formset': formset, 'recipe': recipe})

# Delete View
@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(models.Recipe, pk=pk)
    if recipe.author != request.user:
        raise PermissionDenied("You do not have permission to delete this recipe.")
    
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, "Recipe deleted successfully.")
        return redirect('recipe_list')
    return redirect('recipe_list')
# AI View
@login_required
def ai_recipe_generator(request):
    if request.method == "POST":
        pantry_input = request.POST.get("pantry_input")

        if not pantry_input:
            messages.error(request, "Please type some ingredients first!")
            return redirect("generate_recipe")
        # This will send the API request to gemini and return a structured dictionary with the recipe data
        ai_data = generate_ai_recipe(pantry_input)

        if ai_data:
            # 1. Create and save the main parent Recipe object
            recipe = models.Recipe.objects.create(
                title=ai_data.get("title", "AI Generated Recipe"),
                description=ai_data.get("description", ""),
                instructions=ai_data.get("instructions", ""),
                author=request.user
            )
            # 2. Loop through the ingredients array inside the JSON response
            for ing in ai_data.get("ingredients", []):
                name = ing.get("name", "").strip().title()
                qty = ing.get("quantity", "")
                unit = ing.get("unit", "")

                if name:
                    # Leverage get_or_create to maintain clean tables and avoid duplicates
                    ingredient_obj, _ = models.Ingredient.objects.get_or_create(name=name)

                    models.RecipeIngredient.objects.create(
                        recipe=recipe,
                        ingredient=ingredient_obj,
                        quantity=qty,
                        unit=unit
                    )
            messages.success(request, "Your AI recipe has been created successfully!")
            return redirect("recipe_edit", pk=recipe.pk)
        else:
            messages.error(request, "Failed to communicate with AI. Please try again.")

    return render(request, "recipes/generate_recipe.html")