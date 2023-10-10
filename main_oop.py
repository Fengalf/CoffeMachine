from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine
from helper_tools import cls, hit_enter


def coffe_machine():
    main_menu = Menu()
    coffee_brewer = CoffeeMaker()
    money_handler = MoneyMachine()

    # our power switch
    machine_is_on = True

    # for the grammar bits
    vowels = ["a", "e", "i", "o", "u"]

    # keeping the machine alive
    while machine_is_on:
        # preparing our items that are on the menu
        items_on_menu: dict = {}

        # looping through all the items and prettily print them
        for count, item in enumerate(main_menu.get_items().split('/')):
            # making sure no empty values are added to our print1
            if item:
                print(f"[{count+1}]: {item}")
                items_on_menu[str(count+1)] = item

        user_choice = input(
            "Please press the number of the item you'd like to receive and hit enter to confirm: ")

        # Checking if the user input is actually within our item keys
        # In this if statement there's no 'else', so only valid entries will
        # actually give an output, else the user will loop through the main menu
        if user_choice in items_on_menu.keys():
            chosen_drink = main_menu.find_drink(items_on_menu[user_choice])

            # Checking if we have enough resources for the coffee to brew
            if coffee_brewer.is_resource_sufficient(chosen_drink):

                print(f"This will cost ${chosen_drink.cost}")
                # letting the consumer pay the costs of the coffee
                if money_handler.make_payment(chosen_drink.cost):
                    coffee_brewer.make_coffee(chosen_drink)
                    print(
                        f"\nHere's your '{chosen_drink.name}'. Enjoy!")

        # giving the possibility to check on the resources without having to open
        # the tanks.
        elif user_choice.lower() == "report":
            print("Here's a report of the current resources in the machine:")
            coffee_brewer.report()
            money_handler.report()

        # giving the possibility to turn off the machine.
        elif user_choice.lower() == "off" or user_choice.lower() == "shutdown":
            print("Shutting down the machine.")
            machine_is_on = False

        hit_enter()
        cls()


if __name__ == "__main__":
    coffe_machine()
