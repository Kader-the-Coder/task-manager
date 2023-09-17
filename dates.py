'''This module deals with all date related functions in "task_manage.py".'''
import sys
import calendar
from datetime import datetime


def get_date():
    """Returns today's date"""
    today = datetime.now()
    return today.strftime("%d %b %Y")


def date_overdue(date):
    """Returns True if given date is later than present date"""
    current_date = datetime.strptime(get_date(), '%d %b %Y')
    new_date_temp = datetime.strptime(date, '%d %b %Y')
    if new_date_temp.date() <= current_date.date():
        return True
    else:
        return False


def input_date(question:str):
    """
    Returns user-inputted date if the following criterion is met:
    * question: The question to ask the user.
    * The date is of the format dd mm yyyy.
    * The is not earlier than the current date.
    NOTE: Uses "get_date" function
    """

    
    def date_format():
        """
        Returns user inputted date as list if it is valid.
        Valid dates are of the form:
        * %d %b %Y
        * %d %B %Y
        * %d %M %Y
        NOTE: Returns a message stating if inputted date is not valid.
        """
        # Request user to input date.
        date = input(question)
        # Replace separators that user might include with a space.
        for symbol in ["/", "\\", ".", ",", "-", "_", "+"]:
            date = date.replace(symbol, " ")
        date = date.split(" ")

        new_date = []
        # Removing any empty elements resulted from double spaces.
        for i, date_value in enumerate(date):
            if date_value != "":
                new_date.append(date[i])
                
        # Check if user-input date is valid.
        if len(date) != 3:
            return "You did not input a valid date."

        # Covert numeric month to abbreviated words
        if new_date[1].isnumeric():
            # If month is a valid value
            if int(new_date[1]) <= 12:
                new_date[1] = calendar.month_abbr[int(date[1])]
            else:
                return "You did not input a valid month."

        # Cast date to string format.
        new_date = " ".join(new_date)

        # Check if user-input date is valid.
        try:
            new_date = datetime.strptime(new_date, '%d %b %Y').date()
            new_date = new_date.strftime('%d %b %Y')
        except ValueError:
            return "You did not input a valid date."

        if date_overdue(new_date):
            return f"Date must be later than {get_date()}"
        return new_date


    while True:
        # Request user to input date in the format dd mm yyy.
        date = date_format()
        # Check if date is valid by checking if length of date string
        # is less than shortest message.
        if len(date) < 31:
            return date
        else:
            # Display message and clear lines for re-input
            input(f"Invalid date. {date}. Press ENTER to try again")
            for _ in range(2):
                sys.stdout.write('\x1b[1A' )    # Move cursor up.
                sys.stdout.write('\x1b[2K' )    # Erase line at cursor.
