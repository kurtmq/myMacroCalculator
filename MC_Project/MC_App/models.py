from django.db import models

# Create your models here.
from django.db import models

class Ingredient(models.Model):
    UNIT_CHOICES = [
        ('g', 'gram'),
        ('ml', 'milliliter'),
        ('pc', 'piece'),
        ('oz', 'ounce'),
        ('tbsp', 'tablespoon'),
        ('tsp', 'teaspoon'),
    ]

    name = models.CharField(max_length=100)
    serving_size_value = models.FloatField(help_text="Amount of one serving (e.g., 100)")
    serving_size_unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='g')
    servings_per_container = models.FloatField(help_text="How many servings are in one container")
    price = models.FloatField(help_text="Price of the whole container")
    calories = models.FloatField(help_text="Per serving")
    protein = models.FloatField(help_text="Per serving")
    carbs = models.FloatField(help_text="Per serving")
    fat = models.FloatField(help_text="Per serving")
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.serving_size_value}{self.serving_size_unit})"

    @property
    def price_per_serving(self):
        try:
            return self.price / self.servings_per_container
        except ZeroDivisionError:
            return 0

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    # Aggregate totals from related RecipeItems
    @property
    def total_calories(self):
        return sum(item.total_calories for item in self.items.all())

    @property
    def total_protein(self):
        return sum(item.total_protein for item in self.items.all())

    @property
    def total_carbs(self):
        return sum(item.total_carbs for item in self.items.all())

    @property
    def total_fat(self):
        return sum(item.total_fat for item in self.items.all())

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())


class RecipeItem(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='items'  # allows recipe.items.all()
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    sub_recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sub_items'
    )
    quantity = models.FloatField(default=1)

    def __str__(self):
        return f"{self.ingredient or self.sub_recipe} × {self.quantity}"

    # Computed properties (support both ingredient and sub-recipe)
    @property
    def total_calories(self):
        if self.ingredient:
            return self.ingredient.calories * self.quantity
        elif self.sub_recipe:
            return self.sub_recipe.total_calories * self.quantity
        return 0

    @property
    def total_protein(self):
        if self.ingredient:
            return self.ingredient.protein * self.quantity
        elif self.sub_recipe:
            return self.sub_recipe.total_protein * self.quantity
        return 0

    @property
    def total_carbs(self):
        if self.ingredient:
            return self.ingredient.carbs * self.quantity
        elif self.sub_recipe:
            return self.sub_recipe.total_carbs * self.quantity
        return 0

    @property
    def total_fat(self):
        if self.ingredient:
            return self.ingredient.fat * self.quantity
        elif self.sub_recipe:
            return self.sub_recipe.total_fat * self.quantity
        return 0

    @property
    def total_price(self):
        if self.ingredient:
            return self.ingredient.price_per_serving * self.quantity
        elif self.sub_recipe:
            return self.sub_recipe.total_price * self.quantity
        return 0
