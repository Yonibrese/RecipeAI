from django import forms
from django.forms import inlineformset_factory
from .models import Recipe, RecipeIngredient, Ingredient, Category


class recipeForm(forms.ModelForm):
    category = forms.CharField(
        max_length=100,
        required=False,
        widget = forms.TextInput(attrs={
            'class':'form-control',
            'placeholder': 'select Type or category of recipe',
            'list': 'categories-datalist'
        })
    )

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'category', 'image', 'instructions']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter recipe title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.category:
            self.initial['category'] = self.instance.category.name

    def clean_category(self):
        category_name=self.cleaned_data.get('category')
        if category_name:
            category_name = category_name.strip().title()
            category_obj, created = Category.objects.get_or_create(name=category_name)
            return category_obj
        return None

class RecipeIngredientForm(forms.ModelForm):
    ingredient = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ingredient name'})
    )

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity', 'unit']
        widgets = {
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'quantity (optional)'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'unit (optional)'}),
        }
    
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       if self.instance and self.instance.pk and self.instance.ingredient:
            self.initial['ingredient'] = self.instance.ingredient.name      

    def clean_ingredient(self):
        ingredient_name = self.cleaned_data['ingredient'].strip()
        ingredient, created = Ingredient.objects.get_or_create(name=ingredient_name)
        return ingredient

# This factory links the parent (Recipe) to the child (RecipeIngredient)
recipeIngredientFormSet = inlineformset_factory(
    Recipe, 
    RecipeIngredient, 
    form=RecipeIngredientForm, 
    extra=1, 
    can_delete=True)