from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import Integer, String
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

engine = create_engine("mysql://cf-python:password@localhost/my_database")

Base = declarative_base()


class Recipe(Base):
    __tablename__ = 'final_recipes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(50))

    def __repr__(self):
        return "<Recipe ID: " + str(self.id) + '-' + self.name + ">"

    def __str__(self):
        return "\nName: " + self.name + \
            "\nCooking Time (in minutes): " + str(self.cooking_time) + \
            "\nIngredients: " + str(self.ingredients) + \
            "\nDifficulty: " + str(self.difficulty) + "\n"


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def calc_difficulty(cooking_time, recipe_ingredients):
    print("Run the calc_difficulty with: ", cooking_time, recipe_ingredients)

    ingredients_len = len(recipe_ingredients)
    if (cooking_time < 10 and ingredients_len < 4):
        difficulty = "Easy"
    elif (cooking_time < 10 and ingredients_len >= 4):
        difficulty = "Medium"
    elif (cooking_time >= 10 and ingredients_len < 4):
        difficulty = "Intermediate"
    elif (cooking_time >= 10 and ingredients_len >= 4):
        difficulty = "Hard"
    else:
        print("Something went wrong, try again.")
    print("Difficulty: ", difficulty)
    return difficulty


def return_ingredients_as_list():
    recipes_list = session.query(Recipe).all()
    for recipe in recipes_list:
        print("Recipe: ", recipe)
        print("Ingredients : ", recipe.ingredients)
        recipe_ingredients_list = recipe.ingredients.split(", ")
        print(recipe_ingredients_list)


def create_recipe():
    recipe_ingredeints = []
    name_input = False
    cooking_time_input = False
    number_input = False

    while name_input == False:
        name = input("\nEnter the name of the recipe: ")
        if len(name) < 50:
            name_input = True

            while cooking_time_input == False:
                cooking_time = input(
                    "\nEnter cooking time for the recipe(min): ")
                if cooking_time.isnumeric() == True:
                    cooking_time_input = True
                else:
                    print("Incorrect input, enter a number. ")
        else:
            print("Enter a name with less than 50 characters.")

        while number_input == False:
            ingredients_input = input(
                "How many ingredients would you like to enter?: ")
            if ingredients_input.isnumeric() == True:
                number_input = True

                for _ in range(int(ingredients_input)):
                    ingredient = input("Enter an ingredient: ")
                    recipe_ingredeints.append(ingredient)

            else:
                number_input = False
                print("Enter a correct number.")

    recipe_ingredeints_str = ", ".join(recipe_ingredeints)
    print(recipe_ingredeints_str)
    difficulty = calc_difficulty(int(cooking_time), recipe_ingredeints)

    recipe_entry = Recipe(
        name=name,
        cooking_time=int(cooking_time),
        ingredients=recipe_ingredeints_str,
        difficulty=difficulty
    )
    print(recipe_entry)

    session.add(recipe_entry)
    session.commit()

    print("Recipe has been successfully saved. ")


def view_all_recipes():
    all_recipes = []
    all_recipes = session.query(Recipe).all()

    if len(all_recipes) == 0:
        print("The recipe list is empty.")
    else:
        print("\nAll recipes have been displayed: ")
        print("------------------------------------")

        for recipe in all_recipes:
            print(recipe)


def search_by_ingredient():
    if session.query(Recipe).count() == 0:
        print("Recipe list is empty.")
    else:
        results = session.query(Recipe.ingredients).all()
        print("Results: ", results)
        all_ingredients = []

        for recipe_ingredients_list in results:
            for recipe_ingredients in recipe_ingredients_list:
                recipe_ingredient_split = recipe_ingredients.split(", ")
                all_ingredients.extend(recipe_ingredient_split)

        print("List of ingredients: ", all_ingredients)

        all_ingredients = list(dict.fromkeys(all_ingredients))

        all_ingredients_list = list(enumerate(all_ingredients))

        print("\nAll ingredients:")
        print("------------------------")

        for index, tup in enumerate(all_ingredients_list):
            print(str(tup[0]+1) + ". " + tup[1])

        try:
            ingredient_searched_nber = input(
                "\nEnter the number of an ingredient: ")
            ingredients_nber_list_searched = ingredient_searched_nber.split(" ")
            ingredient_searched_list = []

            for ingredient_searched_nber in ingredients_nber_list_searched:
                ingredient_searched_index = int(ingredient_searched_nber) - 1
                ingredient_searched = all_ingredients_list[ingredient_searched_index][1]

                ingredient_searched_list.append(ingredient_searched)

            print("\nYou selected the ingredient(s): ", ingredient_searched_list)

            conditions = []
            for ingredient in ingredient_searched_list:
                like_term = "%"+ingredient+"%"
                condition = Recipe.ingredients.like(like_term)
                conditions.append(condition)
            searched_recipes = session.query(Recipe).filter(*conditions).all()

            print(searched_recipes)

        except:
            print(
                "Something went wrong, try again.")

        else:

            print("Searched recipes: ")
            for recipe in searched_recipes:
                print(recipe)




def delete_recipe():
    if session.query(Recipe).count() == 0:
        print("Recipe list is empty.")

    else:
        results = session.query(Recipe).with_entities(
            Recipe.id, Recipe.name).all()
        print("Results: ", results)
        print("List of available recipes: ")

        for recipe in results:
            print("\nID: ", recipe[0])
            print("Name: ", recipe[1])
        recipe_id_to_delete = (
            input("\nEnter an ID's number to delete a recipe:  "))
        recipe_to_delete = session.query(Recipe).filter(
            Recipe.id == recipe_id_to_delete).one()

        print("\nYou're about to delete the following recipe: ")
        print(recipe_to_delete)

        delete_confirm = input(
            "\nPlease confirm to delete the following recipe y/n: ")
        if delete_confirm == "y":
            session.delete(recipe_to_delete)
            session.commit()
            print("\nRecipe has been deleted successfully.")
        else:
            return None


def edit_recipe():
    if session.query(Recipe).count() == 0:
        print("Recipe list is empty.")
    else:
        result = session.query(Recipe).with_entities(
            Recipe.id, Recipe.name).all()
        print("Result: ", result)
        print("List of available recipes: ")

        for recipe in result:
            print("\nID: ", recipe[0])
            print("Name: ", recipe[1])

        recipe_id_to_edit = int(
            input("\nEnter the ID of the recipe you want to change: "))
        print(session.query(Recipe).with_entities(Recipe.id).all())

        recipes_id_tup_list = session.query(Recipe.id).all()
        recipes_id_list = []

        for recipe_tup in recipes_id_tup_list:
            print(recipe_tup[0])
            recipes_id_list.append(recipe_tup[0])
        print(recipes_id_list)

        if recipe_id_to_edit not in recipes_id_list:
            print("Number you choose doesn't exist, try again.")
        else:
            recipe_to_edit = session.query(Recipe).filter(
                Recipe.id == recipe_id_to_edit).one()

        print("\nYou are about to edit the following recipe: ")
        print(recipe_to_edit)
        column_for_update = int(input(
            "\nChoose the value you want to be updated(1. name, 2. cooking time, 3. ingredients): "))
        updated_value = (input("\nEnter new value: "))
        print("Choice: ", updated_value)

        if column_for_update == 1:
            print("Updating name for the recipe. ")
            session.query(Recipe).filter(Recipe.id == recipe_id_to_edit).update(
                {Recipe.name: updated_value})
            session.commit()
        elif column_for_update == 2:
            print("Updating cooking time for the recipe. ")
            session.query(Recipe).filter(Recipe.id == recipe_id_to_edit).update(
                {Recipe.cooking_time: updated_value})
            session.commit()
        elif column_for_update == 3:
            print("Updating ingredients for the recipe. ")
            session.query(Recipe).filter(Recipe.id == recipe_id_to_edit).update(
                {Recipe.ingredients: updated_value})
            session.commit()
        else:
            print("Wrong input, plesase try again.")
        updated_difficulty = calc_difficulty(
            recipe_to_edit.cooking_time, recipe_to_edit.ingredients)
        print("Difficulty: ", updated_difficulty)
        recipe_to_edit.difficulty = updated_difficulty
        session.commit()
        print("Successfully updated. ")


def main_menu():
    choice = ""
    while (choice != "quit"):
        print("\n======================================================")
        print("\nMain Menu:")
        print("-------------")
        print("Pick a choice:")
        print("   1. Create a new recipe")
        print("   2. Search for a recipe by ingredient")
        print("   3. Edit an existing recipe")
        print("   4. Delete a recipe")
        print("   5. View all recipes")
        print("\n   Type 'quit' to exit the program.")
        choice = input("\nYour choice: ")
        print("\n======================================================\n")

        if choice == "1":
            create_recipe()
        elif choice == "2":
            search_by_ingredient()
        elif choice == "3":
            edit_recipe()
        elif choice == "4":
            delete_recipe()
        elif choice == "5":
            view_all_recipes()
        else:
            if choice == "quit":
                print("Bye!\n")
            else:
                print("Something went wrong, please try again.")

main_menu()
session.close()
