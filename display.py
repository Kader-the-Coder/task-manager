'''This module deals with some common terminal output functions'''
# pylint: disable=invalid-name
import os
import sys


def clear_lines(n:int = 1):
    """
    Clears from current line, n lines up.
    * n (default 1) must be a positive integer.
    * setting n to -1 clears the entire terminal.
    """
    if n != -1:
        for _ in range(n):
            sys.stdout.write('\x1b[1A' )    # Move cursor up.
            sys.stdout.write('\x1b[2K' )    # Erase line at cursor.
    else:
        # Repeated 2 times to get rid of that annoying scroll buffer.
        # Set to a higher value for smaller terminals
        # NOTE: Higher values results in terminal flickering
        for _ in range(2):
            os.system('cls' if os.name == 'nt' else 'clear')


def print_wrap(text:str, width:int):
    """
    Prints "text", wrapping after a set "width" of characters
    * text: The string to print.
    * width: The max length (In characters) of the string per line.
    """
    count = 0   # Keeps track of how many lines has been printed.
    length = len(text)
    if length > width:
        for i in range(0, length, width):
            # Ignore the "width" amount of characters.
            if i == 0:
                continue
            # Print all other lines in increments of "width"
            print(text[i - width:i])
            count += 1
        # Determine how many characters must still be printed.
        left = len(text) - (count) * width
        # Print remaining characters.
        print(text[length - left:])
    else:
        # If length of string is less than the width:
        print(text)


def print_columns(list1:list, list2:list, list3:list, list4:list,
                  width:int, header1:str, header2:str):
    """
    Tabulates and prints FOUR lists as follows:
    * list1: Appears top left
    * list2: Appears top right
    * list3: Appears bottom left
    * list4: Appears bottom right
    * width: How many characters wide the table must be.
    * header1: The header display on the left
    * header2: The header display on the right
    NOTE: All lists arguments must be equal in length.
    """

    B = "\033[1m"  # Start Bold string
    b = "\033[0m"  # Stop bold string
    U = "\033[4m"  # Start Underline
    u = "\033[0m"  # Stop underline

    # Format column headings
    # Calculate space between headers
    space = str(width - (len(header1)) - 1)   # -1 is an offset value.
    f1 = "{:>"+ space + "}"
    print(B,U)
    print(header1, f1.format(header2), end="")
    print(b,u)
    length = len(list1)
    count = 1   # For tracking position in table
    for i in range(length):
        # Format line 1 of each row.
        # Calculate space between elements of row 1
        space = str(width - (len(str(list1[i]))) - 4) # -4 is an offset
        f1 = "{:>2}"
        f2 = "{:>"+ space + "}"
        line = (f1.format(count)
                + ") "
                + B
                + str(list1[i])
                + b
                + f2.format(list2[i]))
        print(line)

        # Format line 2 of each row.
        # Calculate space between elements of row 2
        space = str(width - (len(str(list3[i]))) - 4) # -4 is an offset
        f1 = "{:>"+ space + "}"
        line = (U
                + " " * 4
                + str(list3[i])
                + f1.format(list4[i])
                + u)
        print(line)

        count += 1


def print_border(symbol:str):
    """Prints a 78 char long border for dividing sections"""
    for _ in range(72):
        # \x1b[2k prints "symbol" on the same line.
        sys.stdout.write(f'{symbol}\x1b[2k')
    print("")
