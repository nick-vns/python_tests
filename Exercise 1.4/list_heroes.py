def display(file):
    heroes = []
    for line in file:
        line = line.rstrip("\n")
        hero_name = line.split(', ')[0]
        first_appearance = line.split(", ")[1]
        heroes.append([hero_name, first_appearance])
    heroes.sort(key=lambda hero: hero[1])
    for hero in heroes:
        print("-------------------------------------")
        print("Superhero: " + hero[0])
        print("First year of appearance: " + hero[1])


filename = input("Enter the file where you stored your superheroes: ")
try:
    file = open(filename, 'r')
    display(file)
except FileNotFoundError:
    print("File doesn't exist.")
except:
    print("Unexpected error.")
else:
    file.close()
finally:
    print("Goodbye!")
