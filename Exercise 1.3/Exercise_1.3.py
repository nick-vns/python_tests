recipes_list = []
ingredients_list = []


def take_recipe():
    name = input("Enter the name of the recipe: ").capitalize()
    cooking_time = int(input("Enter cooking time in minuets: "))
    ingredients = input("Enter ingredients exp(Egg, Soy, etc): ").title()
    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients.split(", "),
    }
    return recipe


n = int(input("How many recipes would you like to enter? "))

for i in range(n):
    recipe = take_recipe()

    for ingredient in recipe["ingredients"]:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)
        # elif ingredient in ingredients_list:
        #     print("Ingredient in a list. ", ingredient)
    recipes_list.append(recipe)

for recipe in recipes_list:
    if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "Easy"
    elif recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4:
        recipe["difficulty"] = "Medium"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "Intermediate"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) >= 4:
        recipe["difficulty"] = "Hard"

    print("==============================")
    print(
        "Added to your recipe: ",
        "\n",
        "Recipe:",
        recipe["name"],
        "\n",
        "Cooking Time (min): ",
        recipe["cooking_time"],
        "\n",
        "Ingredients:",
        recipe["ingredients"],
        "\n",
        "Difficulty level:",
        recipe["difficulty"],
        "\n",
    )

print("All your ingredients: ")
for ingredient in ingredients_list:
    order = ingredients_list.sort()
    print(ingredient)

print("All your recipes: ")
for i in recipes_list:
    print(i)
