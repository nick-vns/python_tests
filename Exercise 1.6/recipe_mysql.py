import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    passwd='password'
)
cursor = conn.cursor()

cursor.execute('CREATE DATABASE IF NOT EXISTS task_database')

cursor.execute('USE task_database')

cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
id INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(50),
ingredients VARCHAR(255),
cooking_time INT,
difficulty VARCHAR(20)
)''')


def main_menu(conn, cursor):
    pick = ""
    while (pick != "quit"):
        print("\n======================================================")
        print("\nMain Menu:")
        print("-------------")
        print("Pick an action:")
        print("   1. Create a new recipe")
        print("   2. Search for a recipe by ingredient")
        print("   3. Update an existing recipe")
        print("   4. Delete a recipe")
        print("   5. View all recipes")
        print("\n   Type 'quit' to exit the program.")
        pick = input("\nYour action: ")
        print("\n======================================================\n")

        if pick == '1':
            create_recipe(conn, cursor)
        elif pick == '2':
            search_recipe(conn, cursor)
        elif pick == '3':
            update_recipe(conn, cursor)
        elif pick == '4':
            delete_recipe(conn, cursor)
        elif pick == '5':
            view_all_recipes(conn, cursor)


def create_recipe(conn, cursor):
    recipe_ingredients = []
    name = input("\nEnter a name for the recipe: ")
    cooking_time = int(input("Enter cooking time in (min): "))
    ingredients = input("Enter ingredients exp(Soy, Milk, Eggs): ").title()
    recipe_ingredients.append(ingredients)
    difficulty = calc_difficulty(cooking_time, recipe_ingredients)
    recipe_ingredients_str = ", ".join(recipe_ingredients)
    sql = 'INSERT INTO Recipes (name, cooking_time, ingredients, difficulty) VALUES (%s, %s, %s, %s)'
    val = (name, cooking_time, recipe_ingredients_str, difficulty)

    cursor.execute(sql, val)
    conn.commit()
    print("Recipe has been saved.")


def calc_difficulty(cooking_time, recipe_ingredients):
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


def search_recipe(conn, cursor):
    all_ingredients = []
    cursor.execute('SELECT ingredients FROM Recipes')
    result = cursor.fetchall()
    for recipe_ingredients_list in result:
        for recipe_ingredients in recipe_ingredients_list:
            recipe_ingredients_split = recipe_ingredients.split(", ")
            all_ingredients.extend(recipe_ingredients_split)

    all_ingredients = list(dict.fromkeys(all_ingredients))
    all_ingredients_list = list(enumerate(all_ingredients))

    print("\nAll ingredients in a list: ")
    print("-----------------------------")

    for index, tup in enumerate(all_ingredients_list):
        print(str(tup[0] + 1) + '. ' + tup[1])

    try:
        ingredient_searched_index = int(
            input("\nEnter ingredient's number from a list: ")) - 1
        ingredient_searched = all_ingredients_list[ingredient_searched_index][1]
        print("\nYour ingredient is:", ingredient_searched)
    except:
        print("Something went wrong, try again.")

    else:
        print("\nRecipes with picked ingredient:  ")
        print("-------------------------------------------------------")

        cursor.execute("SELECT * FROM Recipes WHERE ingredients LIKE %s",
                       ('%' + ingredient_searched + '%',))

        result_recipes_searched = cursor.fetchall()
        for row in result_recipes_searched:
            print("\nID: ", row[0])
            print("name: ", row[1])
            print("ingredients: ", row[2])
            print("cooking_time: ", row[3])
            print("difficulty: ", row[4])


def update_recipe(conn, cursor):
    view_all_recipes(conn, cursor)
    recipe_id = int(input("\nEnter recipe's ID to update it: "))
    column_update = str(input(
        "\nEnter data you want to update, select from('name', cooking_time', 'ingredients'): "))

    updated_value = (input("\nEnter new value for the recipe: "))
    print("New value:", updated_value)

    if column_update == 'name':
        cursor.execute("UPDATE Recipes SET name = %s WHERE id = %s",
                       (updated_value, recipe_id))
        print("Recipe has been updated.")

    elif column_update == 'cooking_time':
        cursor.execute(
            "UPDATE Recipes SET cooking_time = %s WHERE id = %s", (updated_value, recipe_id))
        cursor.execute("SELECT * FROM Recipes WHERE id = %s", (recipe_id,))
        updated_recipe_result = cursor.fetchall()

        name = updated_recipe_result[0][1]
        recipe_ingredients = tuple(updated_recipe_result[0][2].split(','))
        cooking_time = updated_recipe_result[0][3]

        updated_difficulty = calc_difficulty(cooking_time, recipe_ingredients)
        print("Difficulty updated to:", updated_difficulty)
        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s",
                       (updated_difficulty, recipe_id))
        print("Recipe has been updated.")

    elif column_update == 'ingredients':
        cursor.execute(
            "UPDATE Recipes SET ingredients = %s WHERE id = %s", (updated_value, recipe_id))
        cursor.execute("SELECT * FROM Recipes WHERE id = %s", (recipe_id,))
        updated_recipe_result = cursor.fetchall()
        print('Updated ingredients:', updated_recipe_result)

        name = updated_recipe_result[0][1]
        recipe_ingredients = tuple(updated_recipe_result[0][2].split(','))
        cooking_time = updated_recipe_result[0][3]
        difficulty = updated_recipe_result[0][4]

        updated_difficulty = calc_difficulty(cooking_time, recipe_ingredients)
        print("Difficulty updated to:", updated_difficulty)
        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s",
                       (updated_difficulty, recipe_id))
        print("Recipe has been updated.")

    conn.commit()


def delete_recipe(conn, cursor):
    view_all_recipes(conn, cursor)
    recipe_id_delete = (input("\nEnter the ID of the recipe to delete it: "))
    cursor.execute("DELETE FROM Recipes WHERE id = %s", (recipe_id_delete,))

    conn.commit()
    print("\nRecipe has been successfully deleted.")


def view_all_recipes(conn, cursor):
    print("\nAll recipes have been displayed: ")
    print("------------------------------------")

    cursor.execute("SELECT * FROM Recipes")
    result = cursor.fetchall()

    for row in result:
        print("\nID: ", row[0])
        print("Name: ", row[1])
        print("Ingredients: ", row[2])
        print("Cooking Time: ", row[3])
        print("Difficulty: ", row[4])


main_menu(conn, cursor)
print("Goodbye\n")
