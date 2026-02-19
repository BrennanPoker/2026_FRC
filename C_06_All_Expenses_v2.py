import pandas
from tabulate import tabulate

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

def get_expenses(exp_type, how_many=1):
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
    amount = how_many # how_many defaults to 1
    how_much_question = "How much? $"

    # loop to get expenses
    while True:

        # Get item name and check it's not blank
        item_name = not_blank("Item Name: ")

        # check users enter at least one variable expense
        if ((exp_type == "variable" and item_name == "xxx")
                and len(all_items) == 0):
            print("Oops - you have not entered anything.  "
                  "You need at least one item.")
            continue

        # end loop when users enter exit code
        elif item_name == "xxx":
            break

        # Get variable expenses item amount <enter> defaults to number of
        # products being made.
        if exp_type == "variable":

            amount = num_check(question=f"How many <enter for {how_many}. ",
                               num_type="integer", exit_code="")

            # Allows users to push <enter> to default to number of items being made
            if amount == "":
                amount = how_many

            how_much_question = "Price for one? $"

        # Get price for item (question customised depending on expense type).
        price_for_one = num_check(how_much_question, num_type="float")

        all_items.append(item_name)
        all_amounts.append(amount)
        all_dollar_per_item.append(price_for_one)

        # make panda
        expense_frame = pandas.DataFrame(expenses_dict)

        # Calculate Now Cost
        expense_frame['Cost'] = expense_frame['Amount'] = expense_frame['$ / Item']

        # Calculate subtotal
        subtotal = expense_frame['Cost'].sum()

        # Apply currency formatting to currency columns
        add_dollars = ['Amount', '$ / Item', 'Cost']
        for var_item in add_dollars:
            expense_frame[var_item] = expense_frame[var_item].apply(currency)

        # make expense frame into a string with the desired columns
        if exp_type == "variable":
            expense_string = tabulate(expense_frame, 'keys',
                                      tablefmt='psql', showindex=False)
        else:
            expense_string = tabulate(expense_frame[['Item', 'Cost']], headers='keys',
                                      tablefmt='psql', showindex=False)

        # return the expenses panda and subtotal
        return expense_string, subtotal

def currency(x):
    """Formats numbers as currency ($0.00)"""
    return "${:.2f}".format(x)

# Main routine goes here

# Initialise ticket numbers
MAX_TICKETS = 5
tickets_sold = 0

# Initialise variables / non-default options from string checker
payment_ans = ('cash', 'credit')

# Ticket Price List
CHILD_PRICE = 7.50
ADULT_PRICE = 10.50
SENIOR_PRICE = 6.50

# Credit card surcharge (currently 5%)
CREDIT_SURCHARGE = 0.05

# lists to hold ticket details
all_names = []
all_ticket_costs = []
all_surcharges = []

mini_movie_dict = {
    'Name': all_names,
    'Ticket Price': all_ticket_costs,
    'Surcharge': all_surcharges
}



# Main routine starts here

quantity_made = num_check("Quantity being made: ",
                          "integer")

print()

print("Getting Variable Costs...")
variable_expenses = get_expenses("variable", quantity_made)
print()
variable_panda = variable_expenses[0]
variable_subtotal = variable_expenses[1]

print("Getting Fixed Costs...")
Fixed_expenses = get_expenses("fixed")
print()
fixed_panda = Fixed_expenses[0]
fixed_subtotal = Fixed_expenses[1]

# Temporary output area (for easy testing)

print("=== Variable Expenses ===")
print(variable_panda)
print(f"Variable subtotal: ${variable_subtotal:.2f}")
print()

print("=== Fixed Expenses ===")
print(fixed_panda)
print(f"Fixed Subtotal: ${fixed_subtotal:.2f}")

print()
total_expenses = variable_subtotal + fixed_subtotal
print(f"Total Expenses: ${total_expenses:.2f}")



