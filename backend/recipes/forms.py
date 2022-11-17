from django import forms

from .models import Recipe

class RecipeForm(forms.ModelForm:
    class Meta:
        model = Recipe
        fields = ('text', 'category', 'image')
        labels = {
            'text': ('Рецепт'),
            'category': ('Категория:'),
        }
        help_texts = {
            'text': ('напишите Ваш рецепт'),
            'category': ('Выберите из доступных:'),
        }
