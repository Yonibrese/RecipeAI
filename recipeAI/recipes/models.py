from django.db import models
from django.contrib.auth.models import User

class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructions = models.TextField()

    image = models.ImageField(upload_to='recipe/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')

    def __str__(self):
        return self.title
    
    def __repr__(self):
        return self.title
    
class RecipeIngredient(models.Model):
    # This is a through model to represent the many-to-many relationship between Recipe and Ingredient
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=50, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.ingredient.name} for {self.recipe.title}"
    
    def __repr__(self):
        return f"{self.quantity} {self.unit} of {self.ingredient.name} for {self.recipe.title}"