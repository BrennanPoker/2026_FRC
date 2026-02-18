import pandas
def not_blank(question):
    """Checks that a user response is not blank"""

    while True:
        response = input(question)

        if response != "":
            return response

        print("Sorry, this can't be blank. Please try again.\n")

def num_check(question, num_type="float", exit_code=None):
    """Checks that response is a float / integer more than zero"""

    # Checks if the number is more than zero
    if num_type == "float":
        error = "Please enter a number more than 0."
    else:
        error = "Please enter an integer more than 0."

    while True:

        response = input(question)

        # check for exit code and return it if entered
        if response == exit_code:
            return response

        # check datatype is correct and that number
        # is more than zero
        try:

            if num_type == "float":
                response = float(response)
            else:
                response = int(response)

            if response > 0:
                return response
            else:
                print(error)

        except ValueError:
            print(error)

def get_expenses(exp_type, how_many):
    """Gets variable / fixed expenses and outputs
    panda (as a string and a subtotal of the expenses"""

    # Lists for panda
    all_items= []
    all_amounts = []
    all_dollar_per_item = []

    # Expenses dictionary
    expenses_dict = {
        "Item": all_items,
        "Amount": all_amounts,
        "$ / Item": all_dollar_per_item
    }

    # default amount to 1 for fixed expenses and
    # to avoid PEP 8 error for variable expenses
    amount = 1

    # Expenses dictionary

    # loop to get expenses
    while True:

        # Get item name and check it's not blank
        item_name = not_blank("Item Name: ")

        # check users enter at least one variable expense
        # NOTE: If you type the conditions without the brackets,
        # all on one line and then add in enters,
        # Pycharm wil add in the brackets and automatically.
        if ((exp_type == "variable" and item_name == "xxx")
                and len(all_items) == 0):
            print("Oops - you have not entered anything.  "
                  "You need at least one item.")
            continue

        elif item_name == "xxx":
            break

        # Get item amount <enter> defaults to number of
        # products being made.

        amount = num_check( f"How many <enter for {how_many}>: ",
                            "integer", "")

        if amount == "":
            amount = how_many

            cost = num_check( "Price for one? ",  "float")

            all_items.append(item_name)
            all_amounts.append(amount)
            all_dollar_per_item.append(cost)

        # make panda
        expense_frame = pandas.DataFrame(expenses_dict)

        # Calculate Now Cost
        expense_frame['Cost'] = expense_frame['Amount'] = expense_frame['$ / Item']

        # Calculate subtotal
        subtotal = expense_frame['Cost'].sum()

        # return the expenses panda and subtotal
        return expense_frame, subtotal



# Main routine starts here

quantity_made = num_check("Quantity being made: ",
                          "integer")

print()

print("Getting Variable Costs...")
variable_expenses = get_expenses("variable", quantity_made)
print()
variable_panda = variable_expenses[0]
variable_subtotal = variable_expenses[1]

print(variable_panda)
print(variable_subtotal)
