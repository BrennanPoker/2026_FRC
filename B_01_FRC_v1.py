import pandas
from tabulate import tabulate
from datetime import date



# Functions go here
def make_statement(statement, decoration):
    """Emphasises heading by adding decoration
    at the start and end"""

    return f"{decoration * 3} {statement} {decoration * 3}"


def yes_no(question):
    """Checks that users enter yes / y or no / n to a question"""

    while True:
        response = input(question).lower()

        if response == "yes" or response == "y":
            return "yes"
        elif response == "no" or response == "n":
            return "no"
        else:
            print("Please enter yes (y) or no (n).\n")


def Instructions():
    make_statement(statement="Instructions", decoration="🎉")

    print('''

For each ticket holder enter ...
- Their name
- Their age
- The payment method (cash / credit)

The program will record the ticket sale and calculate the 
ticket cost (and the profit).

Once you have either sold all of the tickets or entered the 
exit code ('xxx'), the program will display the ticket 
sales information and write the data to a text file.

It will also choose one lucky ticket holder who wins the 
draw (their ticket is free)

    ''')


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

    # # loop to get expenses
    while True:

        # Get item name and check it's not blank
        item_name = not_blank("Item Name: ")

        # check users enter at least one variable expense
        if ((exp_type == "variable" and item_name == "xxx")
                and len(all_items) == 0):
            print("Oops - you have not entered anything. You need at least one item.")
            continue

        # end loop when users enter exit code
        elif item_name == "xxx":
            break

        # Get variable expenses item amount <enter> defaults to number of
        # products being made.
        if exp_type == "variable":
            amount = num_check(
                question=f"How many <enter for {how_many}>: ",
                num_type="integer",
                exit_code=""
            )

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
    expense_frame['Cost'] = expense_frame['Amount'] * expense_frame['$ / Item']

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
        expense_string = tabulate(expense_frame[['Item', 'Cost']],
                                  headers='keys',
                                  tablefmt='psql', showindex=False)

    # return the expenses panda and subtotal
    return expense_string, subtotal

def currency(x):
    """Formats numbers as currency ($0.00)"""
    return "${:.2f}".format(x)


# Main routine goes here

# initialise variables...

# assume we have no fixed expenses for now
fixed_subtotal = 0
fixed_panda_string = ""

print(make_statement(statement="Fund Raising Calculator", decoration="👍"))

print()
want_instructions = yes_no("Do you want to see the instructions? ")
print()

if want_instructions == "yes":
    Instructions()

print()

# Get product details...
product_name = not_blank("Product Name: ")
quantity_made = num_check(question="Quantity being made: ", num_type="integer")

# Get variable expenses...
print("Let's get the variable expenses...")
variable_expenses = get_expenses( "variable", quantity_made)

variable_panda_string = variable_expenses[0]
variable_subtotal = variable_expenses[1]

# ask user if they have fixed expenses and retrieve them
print()
has_fixed = yes_no("Do you have fixed expenses? ")

if has_fixed == "yes":
    fixed_expenses = get_expenses("fixed")

    fixed_panda_string = fixed_expenses[0]
    fixed_subtotal = fixed_expenses[1]

    # If the user has not entered any fixed expenses,
    # Set empty panda to "" so that is doesn't display
    if fixed_subtotal == 0:
        has_fixed = "no"
        fixed_panda_string = ""

total_expenses = variable_subtotal + fixed_subtotal
total_expenses_string = f"Total Expenses: ${total_expenses:.2f}"


# Get profit Goal here.

# strings / output area

# **** Get current date for heading and filename ****
today = date.today()

# Get day, month and year as individual strings
day = today.strftime("%d")
month = today.strftime("%m")
year = today.strftime("%Y")

# heading / strings...
main_heading_string = make_statement(statement=f"Fund Raising Calculator "
                f"({product_name}, {day}/{month}/{year})", decoration="=")
quantity_string = f"Quantity being made: {quantity_made}"
variable_heading_string = make_statement(statement="Variable Expenses", decoration="-")
variable_subtotal_string = f"Variable Expenses Subtotal: ${variable_subtotal:.2f}"

# set up strings if we have fixed costs
if has_fixed == "yes":
    fixed_heading_string = make_statement(statement="Fixed Expenses", decoration="-")
    fixed_subtotal_string = f"Fixed Expenses Subtotal: {fixed_subtotal:.2f}"

# set fixed cost strings to blank if we don't have fixed costs
else:
    fixed_heading_string = make_statement(statement="You have no Fixed Expenses", decoration="-")
    fixed_subtotal_string = "Fixed Expenses Subtotal: $0.00"

# List of strings to be outputted / written to file
to_write = [main_heading_string, quantity_string,
            "\n", variable_heading_string, variable_panda_string,
            variable_subtotal_string,
            "\n", fixed_heading_string, fixed_panda_string,
            fixed_subtotal_string, total_expenses_string]

# Print area
print()
for item in to_write:
    print(item)

# create file to hold data (add .txt extension)
file_name = f"{product_name}_{year}_{month}_{day}"
write_to = "{}.txt".format(file_name)

text_file = open(write_to, "w+")

# write the item to file
for item in to_write:
    text_file.write(item)

