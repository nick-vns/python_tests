class ShoppingList(object):
    def __init__(self, list_name):
        self.list_name = list_name
        self.shopping_list = []

    def add_item(self, item):
        if not item in self.shopping_list:
            self.shopping_list.append(item)
            print("Added to the list: " + item)
        else:
            print(item + " already in a list")

    def remove_item(self, item):
        if item not in self.shopping_list:
            print("Item is not on a list.")
        else:
            self.shopping_list.remove(item)
            print(item + " removed from a list.")

    def view_list(self):
        print("Shopping list: ", self.list_name)
        print("----------------")
        for item in self.shopping_list:
            print(item)
