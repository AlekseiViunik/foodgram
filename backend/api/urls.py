from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

v1 = DefaultRouter()

v1.register('tags', views.TagViewSet, basename='tags')
v1.register('recipes', views.RecipeViewSet, basename='recipes')
v1.register('ingredients', views.IngredientViewSet, basename='ingredients')
v1.register(
    'users/subscriptions',
    views.UserSubscribeViewSet,
    basename='users_subscribe'
)
v1.register(
    'users',
    views.UserSubscribeActionViewSet,
    basename='users_subscribe_action'
)

urlpatterns = [
    path(
        'recipes/download_shopping_cart/',
        views.CartDownloadView.as_view(),
        name='shopping_list_download'
    ),
    path('', include(v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
