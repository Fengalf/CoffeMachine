import os


def cls():
    '''
        Clears the command line window for a better and decluttered
        output of our program.
    '''
    os.system('cls' if os.name == 'nt' else 'clear')


def hit_enter():
    '''
        Asks the user to hit enter to proceed.
    '''
    input("\nPlease hit [Enter] to continue.")


def billing_process(coffee: dict) -> float:
    '''
        Returns True if the user has payed and either got their change
        or payed on the dot.
        \nReturns False if the user was not able to pay or aborted the
        payment process.
    '''

    # preparing the coin converter
    coin_dict: dict = {
        "D": 1.0,
        "h": 0.5,
        "q": 0.25,
        "d": 0.1,
        "n": 0.05,
        "p": 0.01,
    }

    cls()
    print(
        f"You are about to pay for a {coffee['name']}. That costs ${coffee['price']}")

    # Checking if the user is sure that they want to buy that coffee
    # Just in case they want to opt out
    has_aborted: bool = input(
        "\nDo you want to proceed? [Yes], [No] ").lower() == "no"

    while not has_aborted:
        # Cashing in the money
        cls()
        paying: bool = True
        payed: float = 0.0
        while paying:
            cls()
            print(f"Currently payed: ${payed}")
            print("Please enter a coin to proceed with the payment:")
            print(
                "[D]ollar, \n[h]alf dollar, \n[q]arter, \n[d]ime, \n[n]ickle, \n[p]ennie")
            inserted = input(
                "\nOr hit [Enter] to finish the payment process.")
            if inserted:
                payed += coin_dict[inserted]
            else:
                paying = False

        if payed == coffee["price"]:
            print("\nThat's on the dime.")
            return payed
        elif payed > coffee["price"]:
            print("\nWhoops, you over payed!")
            print(f"Here's your change of ${payed - coffee['price']}!")
            print("*Cling clong coins are dropping into the change shoot.*")
            return payed
        else:
            print("\nOh no, that was not enough.")
            print("Here's your money back.")
            print("*Cling clong coins are dropping into the change shoot.*")
            has_aborted = input(
                "Do you want to restart the payment process? [Yes], [No] ").lower() == "no"

    # Only one if statement without else, because if the statement
    # is correct, the function will be left regardless by returning false.
    if has_aborted:
        payed = 0.0
        return payed


def coffee_to_make(options: dict):
    '''
        Requests the user to choose a drink from the available options.
    '''
    cls()
    # asking the user what coffee they would like to drink
    print("Please chose one of the following coffees, by entering the number in square brackets:")
    for coffee in options.keys():
        print(f"[{coffee}] : {options[coffee]['name']}")

    user_choice: int = int(input("\nWhat's your choice? [1], [2], or [3]: "))
    cls()
    return user_choice


def main_menu() -> int:
    '''
        Prints the menu and returns an int for the selected menu item.
    '''

    cls()
    menu_options: dict = {
        1: "Make coffee",
        2: "Check resources",
        3: "Refill resources",
        9: "Power off"
    }

    menu_option_keys = [[x] for x in menu_options.keys()]

    print("Welcome to `Awesome Coffees`.")
    print("Please chose one of the following options, by entering the number in square brackets:")
    for option in menu_options.keys():
        print(f"[{option}] : {menu_options[option]}")
    user_choice = int(
        input(f"\nWhat's your choice? {menu_option_keys}: "))

    return user_choice


def resource_checker(resources: dict, ingredients: dict) -> bool:
    '''
        Returns True if all resources are available.
        \nIf there is a resource missing it prints what resource is missing
        \nand returns false.
    '''
    has_enough_resources: bool = True
    resource_avail_dict: dict = {
        "water": resources["water"] >= ingredients["water"],
        "coffee": resources["coffee"] >= ingredients["coffee"],
        "milk": resources["milk"] >= ingredients["milk"]
    }

    for resource_checked in resource_avail_dict.keys():
        if not resource_checked:
            print(f"There is not enough {resource_checked}, sorry.")
            has_enough_resources = False
            hit_enter()

    if has_enough_resources:
        print(resource_avail_dict)
        return True
    return False


def resource_printer(resources: dict):
    '''
        Prints the currently available resources in the machine.
    '''

    cls()
    print(f"There is:")
    for resource in resources:
        if resource != "money":
            if resource != "coffee":
                print(f"    {resources[resource]}ml of {resource}")
            else:
                print(f"    {resources[resource]}g of {resource}")
    print("left in the machine.")

    # print(
    #     f"Additionally the machine holds ${resources['money']} right now.")


def resource_remover(resources: dict, ingredients: dict) -> dict:
    '''
        Removes all resources that are needed for brewing a selected
        drink.
    '''
    resources["water"] = resources["water"] - ingredients["water"]
    resources["coffee"] = resources["coffee"] - ingredients["coffee"]
    resources["milk"] = resources["milk"] - ingredients["milk"]

    return resources


def coffee_machine():
    '''
        Boots up the coffee machine program.
    '''
    # setting up the coffee dictionary
    coffees: dict = {
        1: {
            "name": "Espresso",
            "water": 50,
            "coffee": 18,
            "milk": 0,
            "price": 1.5,
        },
        2: {
            "name": "Latte",
            "water": 200,
            "coffee": 24,
            "milk": 150,
            "price": 2.5,
        },
        3: {
            "name": "Cappuccino",
            "water": 250,
            "coffee": 24,
            "milk": 100,
            "price": 3,
        },
    }

    # preparing our ingredients
    resources_baseline: dict = {
        "milk": 1000,
        "coffee": 1000,
        "water": 10000,
        "money": 0,
    }

    # using the baseline to define our resources
    # upon starting the coffee machine
    resources = resources_baseline.copy()

    # keeping our machine alive so we don't get thirsty
    power_switch_is_on = True

    # keep running through the program while the power switch is on
    while power_switch_is_on:

        # booting up the main menu
        main_menu_selection = main_menu()

        # depending on the user's choice we display a separate sub menu now
        # different selection modes can be found in 'main_menu' description or
        # directly in the function
        if main_menu_selection == 1:

            # validating the coffee to make
            coffee_choice = coffee_to_make(coffees)

            # validating if the machine has enough resources left
            # in the tank to fulfill the request
            has_enough_resources: bool = resource_checker(
                resources=resources, ingredients=coffees[coffee_choice])

            # separating ways now depending if there's enough resources.
            # if there's not enough resources we require the user to refill
            # from the main menu.
            # if there are enough resources we require them to pay
            if has_enough_resources:
                # going through the payment process
                amount_payed: float = billing_process(coffees[coffee_choice])
                # if payment was successful we need to remove the ingredients
                # then hand out the coffee
                if amount_payed > 0:

                    resources["money"] = amount_payed
                    # overwriting the existing resources
                    resources = resource_remover(
                        resources=resources, ingredients=coffees[coffee_choice])
                    print(
                        f"\nHere's your {coffees[coffee_choice]['name']}. Enjoy!")
                else:
                    print("\nGoing back to the main menu.")
                hit_enter()
            else:
                print("You will have to refill the machine first with the \
                      \nrequired resource(-s).")

        elif main_menu_selection == 2:

            # simply checking our resources left
            resource_printer(resources=resources)
            hit_enter()

        elif main_menu_selection == 3:

            cls()
            print("Great, you have refilled all the resources!")
            print("You've earned a co-worker of the month badge!")

            # refilling the resources
            resources["water"] = resources_baseline["water"].copy()
            resources["coffee"] = resources_baseline["coffee"].copy()
            resources["milk"] = resources_baseline["milk"].copy()
            hit_enter()

        elif main_menu_selection == 9:

            # DANGER ZONE!!!
            # Turning off the coffee machine
            # NOT ADVISED!
            cls()
            power_switch_is_on = input(
                "\nDo you want to turn off the coffee machine?\nFor safety reasons, please enter [off] to do so, or hit enter to keep it on: "
            ) != "off"
        cls()


if __name__ == "__main__":
    coffee_machine()
