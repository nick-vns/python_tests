import pickle


def display_recipe(recipe):
    print("Recipe:",
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


def search_ingredient(data):
    ingredients_list = data["all_ingredients"]
    indexed_ingredients_list = list(enumerate(ingredients_list, 1))

    for ingredient in indexed_ingredients_list:
        print("No. ", ingredient[0], ' - ', ingredient[1])

    try:
        choose_number = int(input("Enter a number for an ingredient: "))
        index = choose_number - 1
        ingredient_searched = ingredients_list[index]
        ingredient_searched = ingredient_searched
    except IndexError:
        print("Number is not on a list, try again.")
    except:
        print("Unexpected error occured.")
    else:
        for recipe in data["recipes_list"]:
            for recipe_in in recipe["ingredients"]:
                if (recipe_in == ingredient_searched):
                    print("The ingredient has been found in following recipe: ")
                    display_recipe(recipe)


filename = input("Enter the filename where recipes are stored: ")
try:
    recipes_file = open(filename, 'rb')
    data = pickle.load(recipes_file)
except FileNotFoundError:
    print("File wasn't found, try again.")
    data = {'recipes_list': [], 'all_ingredients': []}
except:
    print("Unexpected error, try again.")
    data = {'recipes_list': [], 'all_ingredients': []}
else:
    search_ingredient(data)
finally:
    recipes_file.close()
