import django_filters
from .models import Recipe, Category

class RecipeFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr='icontains', 
        label = 'Search Title',
        widget=django_filters.widgets.forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by title'})
    )

    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        label='Filter by Category',
        widget=django_filters.widgets.forms.Select(attrs={'class': 'form-control'})
    )

    class meta:
        model = Recipe
        fields = ['title', 'category']