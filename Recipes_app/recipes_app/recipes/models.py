from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    name = models.CharField(max_length=256)
    weight = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.name}-{self.weight}'

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Recipe(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    picture = models.ImageField(upload_to='recipes_picture/')
    cooking_time = models.TimeField(default=0)
    time_create = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    portion = models.PositiveSmallIntegerField()
    video = models.URLField()

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'


class CookingSteps(models.Model):
    title = models.CharField(max_length=256)
    instruction = models.TextField(blank=True)
    picture = models.ImageField(upload_to='steps_picture/')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}-{self.recipe}'

    class Meta:
        verbose_name = 'Cooking_step'
        verbose_name_plural = 'Cooking_steps'