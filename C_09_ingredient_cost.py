import pandas
from tabulate import tabulate


# Functions go here
def make_statement(statement, decoration):
    """Emphasizes heading by adding decoration"""

    return f"\n{decoration * 3} {statement} {decoration * 3}\n"

def not_blank(question):
    """Checks that a user response is not blank"""

    while True:
        response = input(question)

        if response != "":
            return response

        print("Sorry, this can't be blank. Please try again.\n")

def num_check(question, num_type="float"):
    """Checks that response is a float / integer more than zero"""

    # Checks if the number is more than zero
    if num_type == "float":
        error = "Please enter a number more than 0."
    else:
        error = "Please enter an integer more than 0."

    while True:
        try:

            if num_type == "float":
                response = float(input(question))
            else:
                response = int(input(question))

            if response > 0:
                return response
            else:
                print(error)

        except ValueError:
            print(error)

def ingredient_cost_used(cost, amount_bought, amount_needed):
    """Calculates cost of amount used"""

    return round((amount_needed / amount_bought) * cost, 2)

def convert_amount(amount, unit):
    """Converts units to smaller base units"""

    conversions = {
        "l": ("ml", 1000),
        "kg": ("g", 1000),
        "ml": ("ml", 1),
        "g": ("g", 1)
    }

    new_unit, multiplier = conversions[unit]
    return amount * multiplier, new_unit

def get_ingredients():
    """Gets ingredient data with validation"""

    # Lists for dataframe
    all_names = []
    all_types = []
    amount_bought_list = []
    amount_needed_list = []
    cost_list = []
    cost_used_list = []
    total_recipe_cost = 0

    # Ingredient dictionary
    ingredient_dict = {
        "Ingredient": all_names,
        "Type": all_types,
        "Amount Bought": amount_bought_list,
        "Amount Needed": amount_needed_list,
        "Cost ($)": cost_list,
        "Cost Used ($)": cost_used_list
    }

    # Ingredient loop
    while True:

        # Get ingredient name
        name = not_blank("Ingredient name (or 'xxx' to stop): ")

        # Check user enters at least one ingredient
        if name == "xxx" and len(all_names) == 0:
            print("You must enter at least one ingredient.\n")
            continue

        # End loop
        elif name == "xxx":
            break

        # Choose ingredient type
        while True:
            ingred_type = input(
                "Type (whole / liquid / solid): ").lower()

            if ingred_type in [
                "whole", "w", "liquid", "l", "solid", "s"]:
                break

            print("Please choose 'whole', 'liquid', or 'solid'.\n")

        # Convert shortcuts into full words
        if ingred_type in ["whole", "w"]:
            ingred_type = "whole"

        elif ingred_type in ["liquid", "l"]:
            ingred_type = "liquid"

        else:
            ingred_type = "solid"

        # whole ingredients
        if ingred_type == "whole":

            unit = "item(s)"

            needed = num_check("How many needed? ", "integer")

            while True:
                bought = num_check("How many bought? ", "integer")

                if bought >= needed:
                    break

                print(
                    "Amount bought cannot be smaller than amount needed.\n")

        # liquid / solid ingredients
        else:

            if ingred_type == "liquid":
                valid_units = ["ml", "l"]
                unit_text = "ml / L"

            else:
                valid_units = ["g", "kg"]
                unit_text = "g / kg"

            while True:
                unit = input(f"Unit ({unit_text}): ").lower()

                if unit in valid_units:
                    break

                print(f"Please enter {unit_text}.\n")

            needed = num_check(
                f"Amount needed ({unit}): ", "float")

            while True:
                bought = num_check(
                    f"Amount bought ({unit}): ", "float")

                if bought >= needed:
                    break

                print(
                    "Amount bought cannot be smaller than amount needed.\n")

            bought, new_unit = convert_amount(bought, unit)
            needed, new_unit = convert_amount(needed, unit)

            unit = new_unit

        # Get cost information
        cost = num_check(
            f"Cost of {bought} {unit} ($): ", "float")

        used_cost = ingredient_cost_used(
            cost, bought, needed)
        total_recipe_cost += used_cost

        # Store data
        all_names.append(name)
        all_types.append(ingred_type)

        amount_bought_list.append(f"{bought} {unit}")
        amount_needed_list.append(f"{needed} {unit}")

        cost_list.append(f"${cost:.2f}")
        cost_used_list.append(f"${used_cost:.2f}")

    # Create dataframe
    ingredient_frame = pandas.DataFrame(ingredient_dict)

    # Make dataframe into a table
    ingredient_string = tabulate(
        ingredient_frame,
        headers='keys',
        tablefmt='psql',
        showindex=False
    )

    ingredient_string += (
        f"\nTotal Recipe Cost: ${total_recipe_cost:.2f}"
    )

    return ingredient_string


# Main routine goes here

print(make_statement("Recipe Ingredient Calculator", "🥘"))

# Get ingredients
ingredients = get_ingredients()

# Output area
print(make_statement("Ingredient Summary", "="))
print(ingredients)