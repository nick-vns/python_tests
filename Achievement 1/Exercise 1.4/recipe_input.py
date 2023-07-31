import pickle


def calc_difficulty(recipe):
    if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4:
        difficulty = "Easy"
    elif recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4:
        difficulty = "Medium"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4:
        difficulty = "Intermediate"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) >= 4:
        difficulty = "Hard"
    return difficulty


def take_recipe():
    name = input("Enter your recipe's name: ")
    cooking_time = int(input("Enter cooking time(min): "))
    ingredients = input(
        "Enter ingredients exp(Soy, Eggs, Water): ").title()
    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients.split(", "),
    }
    recipe["difficulty"] = calc_difficulty(recipe)
    return recipe


recipes_list = []
all_ingredients = []

filename = input("Enter the filename to open your recipes: ")
try:
    recipes_file = open(filename, "rb")
    data = pickle.load(recipes_file)
except FileNotFoundError:
    print("File has not been found, creating a new file.")
    data = {'recipes_list': [], "all_ingredients": []}
except:
    print("Unexpected error occured, try again.")
    data = {'recipes_list': [], "all_ingredients": []}
else:
    recipes_file.close()
finally:
    recipes_list = data["recipes_list"]
    all_ingredients = data["all_ingredients"]

n = int(input("How many recipes would you like to enter? "))

for i in range(n):
    recipe = take_recipe()

    for ingredient in recipe["ingredients"]:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)
    recipes_list.append(recipe)

data = {"recipes_list": recipes_list, "all_ingredients": all_ingredients}

new_file = input("Enter a new file name: ")
with open(new_file, "wb") as f:
    pickle.dump(data, f)
