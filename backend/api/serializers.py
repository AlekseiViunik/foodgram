from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from djoser.serializers import (
    PasswordSerializer,
    UserCreateSerializer,
    UserSerializer
)
from rest_framework import serializers

from recipes.models import (
    FavoriteRecipe,
    Ingredient,
    IngredientAmount,
    Recipe,
    ShoppingCart,
    Subscribe,
    Tag
)
from .fields import Base64ImageField

User = get_user_model()


class UserListSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None:
            return True
        return (
            request.user.is_authenticated
            and Subscribe.objects.filter(
                user=request.user,
                author=obj
            ).exists()
        )


class UserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')
        required_fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientEditSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    amount = serializers.IntegerField(required=True)
    
    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    unit = serializers.ReadOnlyField(source='ingredient.unit')

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'unit', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientAmountSerializer(
        many=True,
        source='recipe',
        required=True,
    )
    author = UserListSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_is_favorited_info(self, obj):
        request = self.context.get('request')
        return (
            request.user.is_authenticated
            and FavoriteRecipe.objects.filter(
                user=request.user,
                favorite_recipe=obj
            ).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return (
            request.user.is_authenticated
            and ShoppingCart.objects.filter(
                user=request.user,
                recipe=obj
            ).exists()
        )


class RecipeEditSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
        max_length=None,
        use_url=True
    )
    ingredients = IngredientEditSerializer(many=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    tags = serializers.ListField(write_only=True)

    class Meta:
        model = Recipe
        fields = ('__all__')

    def validate(self, data):
        name = data.get('name')
        if len(name) < 4:
            raise serializers.ValidationError(
                {'name': 'Должно быть минимум 4 символа'}
            )

        ingredients = data.get('ingredients')
        for ingredient in ingredients:
            if not Ingredient.objects.filter(id=ingredient['id']).exists():
                raise serializers.ValidationError(
                    {
                        'ingredients': f'Ингредиент с id: '
                                       f'{ingredient["id"]} отсутствует'
                    }
                )
            if ingredient.get('amount') < 1:
                raise serializers.ValidationError(
                    'Количество ингредиента должно быть минимум 1'
                )
        if len(ingredients) != len(set([item['id'] for item in ingredients])):
            raise serializers.ValidationError(
                'Ингредиенты не должны повторяться!'
            )
        if len(ingredients) == 0:
            raise serializers.ValidationError(
                'Добавьте хотя бы один ингредиент'
            )
                
        tags = data.get('tags')
        if not tags:
            raise serializers.ValidationError(
                'Добавьте хотя бы один тег'
            )

        cooking_time = data.get('cooking_time')
        if cooking_time > 600 or cooking_time < 1:
            raise serializers.ValidationError(
                {'cooking_time': 'Готовка должна длиться от 1 до 600 минут'}
            )
            
        return data

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            IngredientAmount.objects.bulk_create(
                [
                    IngredientAmount(
                        recipe=recipe,
                        ingredient_id=ingredient.get('id'),
                        amount=ingredient.get('amount'),
                    )
                ]
            )

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            instance.ingredients.clear()
            self.create_ingredients(ingredients, instance)
        if 'tags' in validated_data:
            instance.tags.set(validated_data.pop('tags'))
        return super().update(
            instance, validated_data)


class SetPasswordSerializer(PasswordSerializer):
    current_password = serializers.CharField(
        required=True,
        label='Текущий пароль'
    )

    def validate(self, data):
        user = self.context.get('request').user
        if data['new_password'] == data['current_password']:
            raise serializers.ValidationError(
                {'new_password': 'Введите несовпадающий с текущим пароль'}
            )
        check_current = check_password(data['current_password'], user.password)
        if check_current is False:
            raise serializers.ValidationError({
                "current_password": "Введен неверный пароль"})
        return data


class SubscribeRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        source='author.id',
        read_only=True
    )
    email = serializers.CharField(
        source='author.email',
        read_only=True
    )
    username = serializers.CharField(
        source='author.username',
        read_only=True
    )
    first_name = serializers.CharField(
        source='author.first_name',
        read_only=True
    )
    last_name = serializers.CharField(
        source='author.last_name',
        read_only=True
    )
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(
        source='author.recipe.count'
    )

    class Meta:
        model = Subscribe
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def validate(self, data):
        user = self.context.get('request').user
        author = self.context.get('author_id')
        if user.id == int(author):
            raise serializers.ValidationError({
                'errors': 'Нельзя подписаться на самого себя'})
        if Subscribe.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError({
                'errors': 'Вы уже подписаны на этого автора'})
        return data

    def get_recipes(self, obj):
        recipes = obj.author.recipe.all()
        return SubscribeRecipeSerializer(
            recipes,
            many=True
        ).data

    def get_is_subscribed(self, obj):
        subscribe = Subscribe.objects.filter(
            user=self.context.get('request').user,
            author=obj.author
        )
        if subscribe:
            return True
        return False


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source='favorite_recipe.id',
    )
    name = serializers.ReadOnlyField(
        source='favorite_recipe.name',
    )
    image = serializers.CharField(
        source='favorite_recipe.image',
        read_only=True,
    )
    cooking_time = serializers.ReadOnlyField(
        source='favorite_recipe.cooking_time',
    )

    class Meta:
        model = FavoriteRecipe
        fields = ('id', 'name', 'image', 'cooking_time')
        
    def validate(self, data):
        user = self.context.get('request').user
        recipe = self.context.get('recipe_id')
        if FavoriteRecipe.objects.filter(
            user=user,
            favorite_recipe=recipe
        ).exists():
            raise serializers.ValidationError(
                {'errors': 'Рецепт уже в избранном'}
            )
        return data


class ShoppingCartSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source='recipe.id',
    )
    name = serializers.ReadOnlyField(
        source='recipe.name',
    )
    image = serializers.CharField(
        source='recipe.image',
        read_only=True,
    )
    cooking_time = serializers.ReadOnlyField(
        source='recipe.cooking_time',
    )

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'cooking_time')

    def validate(self, data):
        user = self.context.get('request').user
        recipe = self.context.get('recipe_id')
        if ShoppingCart.objects.filter(
            user=user,
            recipe=recipe
        ).exists():
            raise serializers.ValidationError(
                {'errors': 'Рецепт уже в корзине'}
            )
        return data

