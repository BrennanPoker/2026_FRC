# Functions go here
def make_statement(statement, decoration):
    """Emphasises heading by adding decoration
    at the start and end"""

    print(f"{decoration * 3} {statement} {decoration * 3}")


# Main Routine goes here
make_statement(statement= "Programming is Fun!", decoration="🎉")