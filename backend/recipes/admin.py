from django.contrib import admin

from .models import Category, Recipe


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'category')
    list_editable = ('category',)
    serach_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
    
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Category)
