'''
This module defines all users in task_manager.py.
Requires dates.py to be in the same directory to function.
'''


class User():
    """
    A class representing all registered users.
    """

    def __init__(self, name:str, password:str, role:str) -> None:
        self.name = name
        self.password = password
        self.role = role


a = [User("A","1234","admin"), User("B","5678","normal user")]

b = getattr(a[1], "name")


print(b)