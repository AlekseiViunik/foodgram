from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from backend.settings import NUMBER_OF_RECIPES
from .forms import RecipeForm
from .models import Category, Follow, Recipe, User
from .paginator import paginator


def index(request):
    template = 'recipes/index.html'
    title = 'Последние рецепты'
    recipes = Recipe.objects.select_related('author', 'category').all()
    page_number = request.GET.get('page')
    page_obj = paginator(recipes, NUMBER_OF_RECIPES, page_number)
    context = {
        'title': title,
        'page_obj': page_obj,
        'index': True,
    }
    return render(request, template, context)

def category_recipes(request, slug):
    category = get_object_or_404(Category, slug=slug)
    template = 'recipes/category_list.html'
    title = 'Рецепты выбранной категории'
    recipes = category.recipes.select_related('author', 'category').all()
    page_number = request.GET.get('page')
    page_obj = paginator(recipes, NUMBER_OF_RECIPES, page_number)
    context = {
        'title': title,
        'Category': category,
        'page_obj': page_obj,
    }
    return render(request, template, context)

def profile(request, username):
    title = 'Прфоайл пользователя'
    template = 'recipes/profile.html'
    following = False
    author = get_object_or_404(User, username=username)
    recipes = author.recipes.select_related('author', 'category').all()
    page_number = request.GET.get('page')
    page_obj = paginator(recipes, NUMBER_OF_RECIPES, page_number)
    recipe_counter = recipes.count()
    
    if (
        not isinstance(request.user, AnonymousUser)
        and Follow.objects.filter(user=request.user)
    ):
        following = True
    
    context = {
        'title': title,
        'author': author,
        'page_obj': page_obj,
        'recipe_counter': recipe_counter,
        'following': following,
    }
    return render(request, template, context)

def recipe_detail(request, recipe_id):
    template = 'recipes/recipe_detail.html'
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipes = recipe.author.recipes.select_related('author', 'category').all()
    recipe_counter = recipes.count()
    context = {
        'recipe': recipe,
        'recipe_counter': recipe_counter,
    }
    return render(request, template, context)

@login_required
def recipe_create(request):
    template = 'recipes/create_recipe.html'
    form = RecipeForm(request.POST or None)
    is_edit = False
    if form.is_valid():
        new_recipe = form.save(commit=False)
        new_recipe.author = request.user
        new_recipe.save()
        return redirect('recipes:profile', request.user)
    context = {
        'form': form,
        'is_edit': is_edit,
    }
    return render(request, template, context)

@login_required
def recipe_edit(request, recipe_id):
    template = 'recipes/create_recipe.html'
    redir_template = 'recipes:recipe_detail'
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if recipe.author != request.user:
        return redirect(redir_template, recipe_id=recipe_id)
    is_edit = True
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe,
    )
    if form.is_valid():
        form.save()
        return redirect(redir_template, recipe_id=recipe_id)
    context = {
        'form': form,
        'recipe': recipe,
        'is_edit': is_edit,
    }
    return render(request, template,context)

@login_required
def follow_index(request):
    template = 'recipes/follow.html'
    title = 'Избраные авторы'
    recipes = Recipe.objects.select_related('author', 'category').filter(
        author__following__user=request.user
    )
    page_number = request.GET.get('page')
    page_obj = paginator(recipes, NUMBER_OF_RECIPES, page_number)
    context = {
        'title': title,
        'page_obj':page_obj,
        'following': True,
    }
    return render(request, template, context)

@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    user_fol = Follow.objects.filter(user=request.user, author=author)
    if request.user != author and not user_fol.exists():
        Follow.objects.create(user=request.user, author=author)
    return redirect('recipes:profile', author)

@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect('recipes:profile', author)