class Recipe(object):

    all_ingredients = []

    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.cooking_time = int
        self.difficulty = None

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_cooking_time(self):
        return self.cooking_time

    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time

    def add_ingredients(self, *args):
        self.ingredients = args
        self.update_all_ingredients()

    def get_ingredients(self):
        return self.ingredients

    def calc_difficulty(self, cooking_time, ingredients):
        ingredients_len = len(self.ingredients)
        if cooking_time < 10 and ingredients_len < 4:
            difficulty = "Easy"
        elif cooking_time < 10 and ingredients_len >= 4:
            difficulty = "Medium"
        elif cooking_time >= 10 and ingredients_len < 4:
            difficulty = "Intermediate"
        elif cooking_time >= 10 and ingredients_len >= 4:
            difficulty = "Hard"
        return difficulty

    def get_difficulty(self):
        difficulty = self.calc_difficulty(self.cooking_time, self.ingredients)
        output = str(self.cooking_time)
        self.difficulty = difficulty
        return output

    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients

    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            if ingredient not in self.all_ingredients:
                self.all_ingredients.append(ingredient)

    def __str__(self):
        return "Name: " + self.name + \
            "\nCooking Time (in minutes): " + str(self.cooking_time) + \
            "\nIngredients: " + str(self.ingredients) + \
            "\nDifficulty: " + str(self.difficulty) + "\n"


def recipe_search(data, search_term):
    print("Recipes that contain", search_term)
    print("--------------------------")
    for recipe in data:
        if recipe.search_ingredient(search_term):
            print(recipe)


recipes_list = []


tea = Recipe("Tea")
tea.add_ingredients("Water", "Tea Leaves", "Sugar")
tea.set_cooking_time(5)
tea.get_difficulty()

recipes_list.append(tea)

coffee = Recipe("Coffee")
coffee.add_ingredients("Coffee powder", "Water", "Sugar")
coffee.set_cooking_time(5)
coffee.get_difficulty()

recipes_list.append(coffee)

cake = Recipe("Cake")
cake.add_ingredients("Flour", "Sugar", "Eggs", "Milk",
                     "Butter", "Vanilla Essence")
cake.set_cooking_time(50)
cake.get_difficulty()

recipes_list.append(cake)

bannana_smoothie = Recipe("Banana Smoothie")
bannana_smoothie.add_ingredients("Bananas", "Milk", "Sugar", "Ice")
bannana_smoothie.set_cooking_time(5)
bannana_smoothie.get_difficulty()

recipes_list.append(bannana_smoothie)

print("Recipes List")
print("--------------------------")
for recipe in recipes_list:
    print(recipe)


for ingredient in ["Water", "Sugar", "Bananas"]:
    recipe_search(recipes_list, ingredient)
