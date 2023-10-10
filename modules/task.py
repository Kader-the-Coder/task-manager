'''
This module defines all classes in task_manager.py.
Requires dates.py to be in the same directory to function.
'''

from dates import date_overdue


class Task():
    """
    A class representing all assigned tasks.
    """

    def __init__(self,
                 user:str,
                 name:str, description:str,
                 date_assigned:str,
                 date_due:str,
                 completed:bool = False) -> None:
           
        self.user = user
        self.name = name
        self.description = description
        self.date_assigned = date_assigned
        self.date_due = date_due
        self.completed = completed


    def get_overdue(self) -> str:
        """Returns True if task is overdue and False if not"""
        return date_overdue(self.date_due)


    def change_complete(self) -> None:
        """Change the completed status from True to False and visa versa"""
        self.completed = "No" if self.completed == "Yes" else "Yes"
