from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.db.models import Sum
from django.contrib import messages
import json

def hello_world(request):
    return render(request, 'MC_App/hello_world.html')

# View all ingredients
def ingredient_list(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'MC_App/ingredient_list.html', {'ingredients': ingredients})


# Add a new ingredient (no forms.py)
def ingredient_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        serving_size_value = request.POST.get('serving_size_value')
        serving_size_unit = request.POST.get('serving_size_unit')
        servings_per_container = request.POST.get('servings_per_container')
        price = request.POST.get('price')
        calories = request.POST.get('calories')
        protein = request.POST.get('protein')
        carbs = request.POST.get('carbs')
        fat = request.POST.get('fat')
        notes = request.POST.get('notes')

        Ingredient.objects.create(
            name=name,
            serving_size_value=serving_size_value,
            serving_size_unit=serving_size_unit,
            servings_per_container=servings_per_container,
            price=price,
            calories=calories,
            protein=protein,
            carbs=carbs,
            fat=fat,
            notes=notes,
        )
        return redirect('ingredient_list')

    units = Ingredient.UNIT_CHOICES
    return render(request, 'MC_App/ingredient_create.html', {'units': units})


# Recipes (placeholders for now)
def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'MC_App/recipe_list.html', {'recipes': recipes})


def recipe_create(request):
    ingredients = Ingredient.objects.all()
    recipes = Recipe.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        notes = request.POST.get('notes')
        recipe = Recipe.objects.create(name=name, notes=notes)

        # Parse JSON list of ingredient items
        items_json = request.POST.get('items')
        if items_json:
            items = json.loads(items_json)
            for item in items:
                ing_id = item.get('id')
                qty = float(item.get('serving', 1))
                try:
                    ing = Ingredient.objects.get(id=ing_id)
                    RecipeItem.objects.create(recipe=recipe, ingredient=ing, quantity=qty)
                except Ingredient.DoesNotExist:
                    pass

        # Parse JSON list of recipe items (sub-recipes)
        recipe_items_json = request.POST.get('recipe_items')
        if recipe_items_json:
            recipe_items = json.loads(recipe_items_json)
            for item in recipe_items:
                recipe_id = item.get('id')
                qty = float(item.get('quantity', 1))
                try:
                    sub_recipe = Recipe.objects.get(id=recipe_id)
                    # Avoid circular reference: don't add recipe to itself
                    if sub_recipe.id != recipe.id:
                        RecipeItem.objects.create(recipe=recipe, sub_recipe=sub_recipe, quantity=qty)
                except Recipe.DoesNotExist:
                    pass

        return redirect('recipe_list')

    return render(request, 'MC_App/recipe_create.html', {
        'ingredients': ingredients,
        'recipes': recipes,
    })

def ingredient_edit(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)

    if request.method == 'POST':
        ingredient.name = request.POST.get('name')
        ingredient.serving_size_value = request.POST.get('serving_size_value')
        ingredient.serving_size_unit = request.POST.get('serving_size_unit')
        ingredient.servings_per_container = request.POST.get('servings_per_container')
        ingredient.price = request.POST.get('price')
        ingredient.calories = request.POST.get('calories')
        ingredient.protein = request.POST.get('protein')
        ingredient.carbs = request.POST.get('carbs')
        ingredient.fat = request.POST.get('fat')
        ingredient.notes = request.POST.get('notes')
        ingredient.save()
        return redirect('ingredient_list')

    return render(request, 'MC_App/ingredient_edit.html', {'ingredient': ingredient})

def ingredient_delete(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)

    if request.method == 'POST':
        name = ingredient.name
        ingredient.delete()
        messages.success(request, f'Ingredient "{name}" was deleted successfully.')
        return redirect('ingredient_list')

    return render(request, 'MC_App/ingredient_confirm_delete.html', {'ingredient': ingredient})

def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    ingredients = Ingredient.objects.all()
    recipes = Recipe.objects.exclude(pk=pk)

    if request.method == 'POST':
        recipe.name = request.POST.get('name')
        recipe.notes = request.POST.get('notes')
        recipe.save()

        # Clear old items
        recipe.items.all().delete()

        # Parse incoming JSON
        items = json.loads(request.POST.get('items', '[]'))
        recipe_items = json.loads(request.POST.get('recipe_items', '[]'))

        # Add ingredient items
        for item in items:
            ing = Ingredient.objects.get(id=item['id'])
            RecipeItem.objects.create(recipe=recipe, ingredient=ing, quantity=item['serving'])

        # Add sub-recipes
        for rec in recipe_items:
            sub = Recipe.objects.get(id=rec['id'])
            RecipeItem.objects.create(recipe=recipe, sub_recipe=sub, quantity=rec['quantity'])

        messages.success(request, f'Recipe "{recipe.name}" updated successfully.')
        return redirect('recipe_list')

    # Preload the current recipe items
    recipe_items = recipe.items.all()
    return render(request, 'MC_App/recipe_edit.html', {
        'recipe': recipe,
        'ingredients': ingredients,
        'recipes': recipes,
        'recipe_items': recipe_items
    })


def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.method == 'POST':
        name = recipe.name
        recipe.delete()
        messages.success(request, f'Recipe "{name}" was deleted successfully.')
        return redirect('recipe_list')

    return render(request, 'MC_App/recipe_confirm_delete.html', {'recipe': recipe})
