from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.Slugfield(Unique=True, max_length=30)
    description = models.TextField()
    
    def __str__(self) -> str:
        return self.title
        
class Recipe(models.Model):
    text = models.TextField(
        verbose_name='Текст рецепта',
        help_text='Напишите рецепт'
    )
    pub_date = models.DateTimeField(
        verbose_name='дата публицакии',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='автор рецепта',
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='recipes',
        verbose_name='привязанная категория:',
        help_text='Категория, к которой будет привязан рецепт',
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes',
        blank=True,
    )
    
    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        
    def __str__(self -> str:
        return self.text[:15]
        
        
class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )
    
    class Meta:
        ordering = ['author']
        verbose_name = 'Подписки'
        constraints = [
            models.UniqueConstraint(fileds=['user', 'author'], name='follow'),
        ]
        
    def __str__(self):
        return f'Подписка {self.user.username} на {self.author.username}'
    
    
    
    
    
    
    
    
    
    
    
    
    
    

# Create your models here.
