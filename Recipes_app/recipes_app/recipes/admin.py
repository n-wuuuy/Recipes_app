from django.contrib import admin

from recipes.models import CookingSteps, Category, Product, Recipe


# Register your models here.

class StepsInline(admin.TabularInline):
    model = CookingSteps
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'time_create')
    list_filter = ('cooking_time', 'time_create', 'portion')
    search_fields = ('title', 'products__name', 'category__name', 'owner')
    inlines = [StepsInline]
    fieldsets = (
        (None, {
            'fields': (('title', 'owner', 'description'),)
        }),
        (None, {
            'fields': (('cooking_time', 'portion'),)
        }),
        (None, {
            'fields': (('products', 'category'),)
        }),
        (None, {
            'fields': (('picture', 'video'),)
        })
    )


@admin.register(CookingSteps)
class StepsAdmin(admin.ModelAdmin):
    list_display = ('title', 'recipe')
