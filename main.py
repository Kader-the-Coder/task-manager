'''Task Manager Program.'''

#=============================Comments=================================

# Disable annoying pylint messages:
# pylint: disable=invalid-name
# pylint: disable=too-many-function-args
# pylint: disable=no-name-in-module

#=========================Importing Libraries==========================
#region This section includes all libraries imported into the program

import os
from modules.display import clear_lines, print_wrap, print_columns, print_border
from modules.dates import get_date, input_date
from modules.task import Task
from modules.user import User

#endregion
#=============================Constants================================
#region This section contains all constants defined in this program

PROGRAM_NAME = "\033[1mHYPERION TASK MANAGER LTD.\033[0m"
DIRECTORY = os.path.dirname(__file__)
USER_TXT = os.path.join(DIRECTORY, "data/user.txt")
TASKS_TXT = os.path.join(DIRECTORY, "data/tasks.txt")
TASK_OVERVIEW_TXT = os.path.join(DIRECTORY, "data/task_overview.txt")
USER_OVERVIEW_TXT = os.path.join(DIRECTORY, "data/user_overview.txt")

#endregion
#==========================Initialize lists============================
#region This section initializes the core lists that will be used.

user_list = []
task_list = []

#endregion
#=============================Functions================================
#region This section includes all functions used in the program


def create_users():
    '''
    Creates a new user.txt file in the even the user.txt is missing 
    from working directory.
    NOTE: This function uses the "clear_lines" function.
    NOTE: This function uses the "header" function.
    '''
    header("\nFileError: The file \"user.txt\" is missing or corrupt."
          "Create new \"user.txt\" file?")
    while True:
        # Ask user if user would like to add a new user.
        choice = input("Input yes(y) or no(n)\n: ")

        # If you chooses to create new file:
        if choice[0].lower() == "y":
            with open(USER_TXT,"w", encoding='utf-8-sig') as file:
                file.write("admin, adm1n, admin")
                input("File successfully created."
                      "Please login in with the following credentials:\n\n"
                      "Username: admin\n"
                      "Password: adm1n\n\n"
                      "Press ENTER to continue.")
                break
        # If you chooses not create a new file, end the program.
        elif choice[0].lower() == "n":
            print("\nVery well. You have made your bed...")
            print("Now lie in it.")
            print("\nProgram has been terminated by user.")
            exit()

        else:
            # If user selected an incorrect option.
            input("incorrect input. Press ENTER to try again.")
            clear_lines(3)


def create_tasks():
    '''
    Creates a new tasks.txt file in the even the tasks.txt is missing 
    from working directory.
    NOTE: This function uses the "header" function.
    '''
    header("\nFileError: The file \"tasks.txt\" is missing or corrupt. "
          "A \"tasks.txt\" file with default tasks will be created.\n")
    input("Press enter to continue.")

    with open(TASKS_TXT,"w", encoding='utf-8-sig') as file:
        file.write("admin, Register Users with task_manager.py, "
                   "Use task_manager.py to add the usernames and "
                   "passwords for all team members that will be using "
                   "this program., 10 Oct 2019, 20 Oct 2019, No\n"
                   "admin, Assign initial tasks, Use task_manager.py "
                   "to assign each team member with appropriate tasks, "
                   "10 Oct 2019, 25 Oct 2019, No")
    input("\n\"tasks.txt\" successfully created. Press ENTER to log in")


def populate_users(file:str):
    """
    Populate 'user_list' with information from a given txt file.
    """
    # Ensure list is empty to prevent indexing errors
    user_list.clear()
    with open(file, "r", encoding='utf-8-sig') as _file:
        for lines in _file:
            # Interpret lines in file to create 'User' object
            user_data = lines.lower()
            user_data = user_data.strip()
            user_data = user_data.split(", ")
            # Create User object and add to user_list.
            user_obj = User(user_data[0], user_data[1], user_data[2])
            user_list.append(user_obj)


def populate_tasks(file:str):
    """
    Populate a 'task_list' with information from a given txt file.
    """
     # Clear list to prevent duplicates.
    task_list.clear()
    with open(file, "r", encoding='utf-8-sig') as _file:
        # Format each line to create 'Task' object
        for lines in _file:
            task_data = lines.strip()
            task_data = task_data.split(", ")
            # Create task object.
            task_obj = Task(task_data[0],
                            task_data[1],
                            task_data[2],
                            task_data[3],
                            task_data[4],
                            task_data[5])

            # Add task object to list.
            task_list.append(task_obj)


def reg_user():
    '''Register's a new user based on user input'''
    # Ask user to input new username, password and re-enter password.
    username = input_exist("Username: ",
                           user_list,
                           "name",
                           "Invalid name or username already exists.",
                           exists=False)
    password = input("Password: ")

    input_test("Confirm password: ",
               password,
               "Passwords do not match.")

    # update "user.txt" and "user_list" upon successfully entering a user .
    add_to_txt(f"\n{username}, {password}, user", USER_TXT, True)
    populate_users(USER_TXT)
    input(f"\n{username} successfully registered. Press ENTER to continue.\n")


def select_user(exclude:list=None):
    """
    Prints a list of all registered users which may be inputted.
    * exclude: The list of users (by name) to exclude when printing
    """
    # Creates an empty list if no names must be excluded
    if exclude is None:
        exclude = []

    temp_user_list = []
    for user_obj in user_list:
        if user_obj.name not in exclude:
            if user_obj not in temp_user_list:
                print(f"> {user_obj.name}")
                temp_user_list.append(user_obj)

    # Request ADMIN to select a user
    print()
    username = input_exist("Username: ",
                        user_list,
                        "name",
                        "Invalid username.",
                        "obj")
    return username


def add_task(admin:bool = True):
    """
    Requests, and then adds a task to the selected user.
    * admin (default True) is if user can assign anyone a task or not.
    * got_info (default False): Task information to add. If set to false,
                                information will be requested.
    * info must be given in the format: [name of task, task description, date due]
    NOTE: Uses "header" function.
    """
    # if 'User' object has the 'role' attr set to 'admin':
    if USERNAME.role == "admin" and admin:
        print("\nPlease select a user to assign a task to.\n"
                "To select a user, input their \"username\".\n")
        user = select_user()
    # if user is not ADMIN, then tasks can only be assigned to themselves.
    else:
        user = USERNAME

    header("\nTask Assigning\nBecause nobody has anything better to do.")
    print(f"\nAssigning task to {user.name}. Please complete the fields below:\n")

    # Request task information that must be assigned to selected user.
    # Request name of task.
    task_name = input_exist("       Task: ",
                            task_list,
                            "name",
                            "This task already exists",
                            "str",
                            False)
    # Request due date.
    print("   Date due: dd mm yyyy")
    date_due = input_date("           : ")
    clear_lines(2)
    # Format due date correctly in terminal if due date is valid.
    print(f"   Date due: {date_due}")
    # Request task description
    description = input_something("Description: ")

    # update "user.txt" and "user_list" upon successfully entering a user .
    add_to_txt(f"\n{user.name}, {task_name}, {description}, "
            f"{str(get_date())}, {date_due}, No", TASKS_TXT, True)
    populate_tasks(TASKS_TXT)
    input(f"\n\033[1m{task_name}\033[0m "
          "has been successfully assigned to "
          f"\033[1m{user.name}\033[0m.\n"
          "Press ENTER to continue.\n")


def view_all():
    """Prints a list of all currently assigned tasks"""
    # Create 4 lists for use in "print_columns" function
    task_name = []
    task_user = []
    task_date_due = []
    task_completed = []
    for obj in task_list:
        task_name.append(obj.name)
        task_user.append("Assigned to: " + obj.user)
        task_date_due.append(obj.date_due)
        task_completed.append("Completed" if obj.completed == "Yes"
                              else "Not completed")

    print_columns(task_name, task_date_due, task_user, task_completed,
                  72, "TASKS", "DATE DUE")


def view_mine(user_obj:object):
    """Prints a list of all user assigned tasks"""
    # Create 4 lists for use in "print_columns" function
    task_name = []
    task_user = []
    task_date_due = []
    task_completed = []
    for obj in task_list:
        if obj.user == user_obj.name:
            task_name.append(obj.name)
            task_user.append("Assigned to: " + obj.user)
            task_date_due.append(obj.date_due)
            task_completed.append("Completed" if obj.completed == "Yes"
                                else "Not completed")
    if task_name:
        print_columns(task_name, task_date_due, task_user, task_completed,
                      72, "TASKS", "DATE DUE")
    else:
        print("Yay! You have no assigned tasks at the moment.")


def view_task(task_obj:object) -> None:
    """Views all the info of a selected task of given user."""

    header(f"\nTask Viewer (All) -> {task_obj.user}\nAll of the tasks in one place.")

    # Create 4 lists for use in "print_columns" function
    task_name = [task_obj.name]
    task_user = [f"Assigned to: {task_obj.user}"]
    task_date_due = [task_obj.date_due]
    task_completed = ["completed" if task_obj.completed == "Yes" else "Not completed"]

    print_columns(task_name, task_date_due, task_user, task_completed,
                  72, "TASKS", "DATE DUE")

    # Print additional info about the task.
    print()
    print(f"Date assigned: {task_obj.date_assigned}")
    print()
    print("\033[1mDescription:\033[0m")
    description = f"{task_obj.description}"
    print_wrap(description, 72)
    print_border("_")


def modify_task(task_obj:object,
                user_obj:object | None = None,
                yes_no:bool | None = False,
                date_due:bool | None = False,
                new_user:bool | None = False,
                del_task:bool | None = False) -> None:
    """
    Modify the details of a task of a user.

    Set one of the parameters to true to modify.
    * yes_no: The completion status of task.
    * date_due: The due date of task.
    * new_user: The user of the task.
    * del_task: To delete the task.
    NOTE: Set only one keyword to True to avoid potential errors.
    """
    # Change task completion status
    if yes_no:
        task_obj.change_complete()
        input("\nTask completion status has been changed successfully.\n"
              "Press ENTER to continue.")
    # Delete task.
    elif del_task:
        if task_obj.completed == "Yes":
            task_list.remove(task_obj)
            input("\nTask has been successfully removed.\n"
                  "Press ENTER to return to previous menu.")
        else:
            input("\nOnly completed tasks may be removed.\n"
                  "Press ENTER to return to previous menu.")
            return None
    elif task_obj.completed == "No":
        # Change user assigned to task.
        if new_user:
            task_obj.user = user_obj.name
            input("\nNew user has been assigned successfully.\n"
                  "Press ENTER to continue.")
        # Change due date.
        if date_due:
            task_obj.date_due = input_date(": ")
            input("\nDue date of task has been changed successfully.\n"
                  "Press ENTER to continue.")
    else:
        input("\nCompleted tasks may not be modified.\n"
              "Press ENTER to retry input.")
        return None

    # Update txt file with changes to tasks
    update_tasks_txt(task_list, TASKS_TXT)


def stats(stats_type):
    '''
    Generate statistics of a selected type
    * if type = "tasks": return task stats as list.
    * if type = "users": return user stats as list.
    '''
    task_num = len(task_list)

    def stats_tasks():
        '''Returns tasks statistics as a list'''
        task_completed = sum(1 for task in task_list if task.completed == "Yes")
        task_uncompleted = task_num - task_completed
        task_overdue = sum(1 for task in task_list if task.get_overdue())

        percentage_complete = round((task_completed / (task_num or 1)) * 100, 2)
        percent_incomplete = round((task_uncompleted / (task_num or 1)) * 100, 2)
        percent_overdue = round((task_overdue / (task_uncompleted or 1)) * 100, 2)

        return [task_num,
                task_completed,
                task_uncompleted,
                task_overdue,
                percentage_complete,
                percent_incomplete,
                percent_overdue]

    def stats_users():
        """
        Returns a dictionary with the key as a user object and a value
        a list of user stats.
        """
        temp_user_list = {}
        for user in user_list:
            user_task_list = [task for task in task_list
                              if task.user == user.name]
            user_tasks = len(user_task_list)
            user_completed = sum(1 for task in user_task_list
                                 if task.completed == "Yes")
            user_uncompleted = user_tasks - user_completed
            user_overdue = sum(1 for task in user_task_list
                               if task.get_overdue())

            percent_user_tasks = (user_tasks / (task_num or 1)) * 100
            percent_user_tasks = round(percent_user_tasks, 2)

            percent_user_completed = (user_completed / (user_tasks or 1)) * 100
            percent_user_completed = round(percent_user_completed)

            percent_user_uncompleted = 100 - percent_user_completed
            percent_user_overdue = (user_overdue / (user_tasks or 1)) * 100
            percent_user_overdue = round(percent_user_overdue, 2)

            temp_user_list[user] = [user_tasks,
                                    user_completed,
                                    user_uncompleted,
                                    user_overdue,
                                    percent_user_tasks,
                                    percent_user_completed,
                                    percent_user_uncompleted,
                                    percent_user_overdue]

        return temp_user_list

    if stats_type == "tasks":
        return stats_tasks()
    elif stats_type == "users":
        return stats_users()


def stats_generate():
    '''Generate to text files containing task and user statistics'''
    # Obtain information on tasks.
    stats_task = stats("tasks")
    # Format text of task overview.
    text = f'''
**************************TASK OVERVIEW********************************

Total tasks assigned: {stats_task[0]}

    Completed: {stats_task[1]} ({stats_task[4]}%)
Not completed: {stats_task[2]} ({stats_task[5]}%)
      Overdue: {stats_task[3]} ({stats_task[6]}%)
    
***********************************************************************
            '''

    add_to_txt(text, TASK_OVERVIEW_TXT, True, "w+")
    print("Task overview report generated.")

    # Obtain information on users
    stats_user = stats("users")
    # Format text of user overview.
    text = f'''
**************************USER OVERVIEW********************************

Total tasks assigned: {len(task_list)}
Total users registered: {len(user_list)}

-----------------------------------------------------------------------
    '''
    for user in stats_user:
        text += (f'''
{user.name}
Tasks assigned: {stats_user[user][0]} ({stats_user[user][4]}%)

    Completed: {stats_user[user][1]} ({stats_user[user][5]}%)
Not completed: {stats_user[user][2]} ({stats_user[user][6]}%)
      Overdue: {stats_user[user][3]} ({stats_user[user][7]}%)
-----------------------------------------------------------------------
                ''')
    add_to_txt(text, USER_OVERVIEW_TXT, True, "w+")
    print("User overview report generated.")


def stats_read(task:str, user:str):
    '''Prints stats from text file.
    * task: The file to retrieve task overview stats from.
    * user: The file to retrieve user overview stats from.
    '''

    try:
        # Attempt to open files
        task_file = open(task, "r", encoding='utf-8-sig')
        user_file = open(user, "r", encoding='utf-8-sig')
    except OSError:
        # If files do not exist, create them and open.
        stats_generate()
        task_file = open(task, "r", encoding='utf-8-sig')
        user_file = open(user, "r", encoding='utf-8-sig')

    header(f"\nStatistics\n\nHi {USERNAME.name}, "
           f"this is what's happening at {PROGRAM_NAME}:\n")   

    # Read and display task overview
    text = task_file.read()
    print(text)
    task_file.close()

    input("Press ENTER to view user overview")
    clear_lines(12)

    # Read and display user overview
    text = user_file.read()
    print(text)
    user_file.close()


def attr_is_value(value, location, attr) -> bool:
    """
    Returns True if a value is equal to an attribute of an object inside
    given list.

    * value: The value to check.
    * location: The object or list in which to check for the attribute.
    * attr: The attribute of an object to compare with value.
    """
    try:
        if isinstance(location, list):
            for _, ele in enumerate(location):
                if getattr(ele, attr) == value:
                    return True

        if getattr(location, attr) == value:
            return True

        return False

    except AttributeError:
        return False


def attr_get_index(value, list_name, attr) -> (int | None):
    """
    Returns the index of an object that has an attribute of a given value.

    * value: The value to check.
    * location: The list in which to check for the attribute.
    * attr: The attribute of an object to compare with value.
    """
    if isinstance(list_name, list):
        for i, ele in enumerate(list_name):
            if getattr(ele, attr) == value:
                return i

    return None


def input_something(input_request:str, lines:int = 3) -> str:
    """Returns user input if it is not empty"""
    while True:
        user_input = input(input_request)
        if user_input.strip() == "":
            print("You did not input anything!.")
            input("Press ENTER to try again.")
            clear_lines(lines)
            continue
        return user_input


def input_test(input_request:str, expected_input:any, message:str) -> None:
    '''
    Compares user input to expected input
    * user_input: What user types in.
    * expected_input: What user is expected to type in.
    * message: Message to display if user input and expected differs

    NOTE: This function continues to ask user to input until
    it matches the expected input.
    '''
    while True:
        user_input = input_something(input_request)

        if user_input == expected_input:
            break

        input(f"{message}\n"
                "Press ENTER to try again")
        clear_lines(3)


def input_exist(input_request:str, location:list, attr:str,invalid_message:str,
                return_type:str = "obj", exists:bool = True) -> any:
    """
    Returns a value in given list if user input matches a attribute value

    * input_request: What to request user to type in.
    * location: Where to check for user_input.
    * attr: what attribute to compare with.
    * invalid_message: Message to display if input is invalid.
    * return_type (Default "obj"): What to return if input is valid:
      "obj", "str" or "str_case_sensitive"
    """
    while True:
        user_input = input_something(input_request)
        # If input exists:
        if attr_is_value(user_input.lower(), location, attr):
            if exists:
                if return_type == "obj":
                    user_input = user_list[attr_get_index(user_input.lower(), location, attr)]
                    return user_input
                if return_type == "str":
                    return user_input.lower()
                if return_type == "str_case_sensitive":
                    return user_input
            else:
                print(invalid_message)
        elif not exists:
            return user_input.lower()
        else:
            print(invalid_message)
        input("Press ENTER to try again.")
        clear_lines(3)


def add_to_txt(string:str, file_txt:str, case_sensitive:bool = False, method:str | None = "a+"):
    """
    Adds a string to a txt file.
    * string: The string to add.
    * file_txt: The txt file to add to.
    * case_sensitive (default false) changes all letters to lower case
    * method (default "a+"): The read method to use when opening a file.
    """
    with open(file_txt, method, encoding='utf-8-sig') as file:
        if case_sensitive:
            file.write(string)
        else:
            file.write(string.lower())


def update_tasks_txt(list_name:list, file_txt:str):
    """
    Updates a txt file with data from a list.

    * list_name: The list to update file with.
    * file_txt: The file to update.
    * Used primarily to update the tasks.txt file.

    Call after modifying a object that is stored in a txt file.
    """
    data = ""
    for task_obj in list_name:
        # convert each object in list to a line of information.
        data += (f"{task_obj.user}, "
                + f"{task_obj.name}, "
                + f"{task_obj.description}, "
                + f"{task_obj.date_assigned}, "
                + f"{task_obj.date_due}, "
                + f"{task_obj.completed}"
                + "\n")

    # Remove last "new line" to prevent creating empty lines
    data = data[:-1]

    # Writes new data to txt file.
    with open(file_txt, "w", encoding='utf-8-sig') as file:
        file.write(data)


def select_menu(menu_display:str, select:list, lines:int = 3):
    '''
    Presents user with menu option
    * menu_display: The menu to show
    * choice: A list of valid user inputs.
    * lines: Number of lines to clear if no valid option selected.
    NOTE: The list may only contain strings.
    NOTE: Makes use of the "clear_lines" function.
    '''
    while True:
        # Display menu and request input.
        options = input_something(menu_display, lines)
        options = options.lower().strip()
        # If user input is not one of the expected answers:
        if options in select:
            return options

        input("You have entered an invalid input.\n"
              "Press ENTER to try again.")
        clear_lines(lines)


def header(message:str = ""):
    """
    Clears and prints a header in the terminal.
    The message argument is optional.
    """
    clear_lines(-1)
    print(PROGRAM_NAME)
    print(message)


#endregion
#===========================Initialization===============================
#region This checks and and populates all files containing user and task
#       data

# Check to see if txt files exist, creating them with the default
# information if they dont.
try:
    populate_users(USER_TXT)
except OSError:
    create_users()
    populate_users(USER_TXT)

try:
    populate_tasks(TASKS_TXT)

except OSError:
    create_tasks()
    populate_tasks(TASKS_TXT)

#endregion
#===========================Login Section==============================
#region This section deals with user login and the implication thereof.

header("\nPlease enter your login details:\n")
# Request user name and password.
USERNAME = input_exist("Username: ", user_list, "name",
                       "That username does not exist.")
input_test("Password: ", USERNAME.password,
            "Invalid password.")

# If user who logged in is admin enable extra options.
if USERNAME.role == "admin":
    r = "r  - register a user\n"
    va = "va - view all tasks\n"
    gr = "gr - generate reports\n"
    ds = "ds - display statistics\n"
else:
    r = ""
    va = ""
    gr = ""
    ds = ""

#endregion
#===========================Menu Section 1==============================
#region Define menu options that will be displayed to user

menu = 'm'

menu_m = ("\nSelect one of the following options:\n"
          + r
          + "a  - add task\n"
          + va
          + "vm - view my tasks\n"
          + gr
          + ds
          + "e  - exit\n"
          + ": ")

menu_r = '''
Select one of the following options: \n         
r - register another user
m - main menu
: '''

menu_a = '''
Select one of the following options: \n            
a - add another task
m - main menu
: '''

menu_v_ = '''
input a task number to view the corresponding task\n
m - return to previous menu
: '''

menu_va = '''
Select one of the following options: \n            
1 - change task completion status.
2 - Assign to different user.
3 - Change due date.
4 - Remove task.
m - return to previous menu
: '''

menu_vm = '''
Select one of the following options: \n            
1 - change task completion status
m - return to previous menu
: '''

#endregion
#===========================Menu Section 2==============================
#region This section mainly handles user interaction with the program

while True:
    # Main Menu.
    if menu == 'm':
        header(f"Welcome back {USERNAME.name}. We missed you... Is that weird?")
        menu = input(menu_m).lower().strip()

    # Registering a new user (Only visible to ADMIN).
    elif menu == 'r' and USERNAME.role == "admin":
        header("\nUser registration\nPlease enter new user credentials.\n")
        # Registers a new user
        reg_user()
        # Request user to input options from "menu_r"
        header("\nUser registration\nPlease enter new user credentials.\n")
        menu = select_menu(menu_r,["m", "r"],8)

    # Assigning a new task.
    elif menu == 'a':
        header("\nTask Assigning\nBecause nobody has anything better to do.")

        add_task()

        # Request user to input options from "menu_a"
        header("\nTask Assigning\nBecause nobody has anything better to do.")
        menu = select_menu(menu_a,["m", "a"],8)

    # View all tasks (Only visible to ADMIN).
    elif menu == 'va' and USERNAME.role == "admin":
        header("\nTask Viewer (All)\nAll of the tasks in one place.")
        view_all()

        # create "temp list" in order to use the function "select_menu".
        # Index all tasks
        temp_list = [str(num) for num in range(1, len(task_list) + 1)]
        # Include "m" for the option of exiting to main menu.
        temp_list.append("m")

        # Request user to input options from "menu_v_"
        menu = select_menu(menu_v_, temp_list, 7)
        # Return to main menu if user selected "m".
        if menu == "m":
            continue
        # Else check if user selected a valid task number.
        if menu in temp_list:
            # Store selected task in variable
            task_selected = task_list[int(menu) - 1]
            while True:
                # Request user to input options from "menu_va"
                view_task(task_selected)
                menu = select_menu(menu_va, ["1", "2", "3", "4", "m"], 11)
                # Change completion status.
                if menu == "1":
                    modify_task(task_selected, yes_no=True)
                # Change assigned user.
                elif menu == "2":
                    clear_lines(8)
                    user_selected = select_user([task_selected.user])
                    modify_task(task_selected, user_selected, new_user=True)
                # Change due date.
                elif menu == "3":
                    clear_lines(8)
                    print("Please input the new due date.")
                    print("  dd mm yyyy:")
                    modify_task(task_selected, date_due=True)
                # Remove task.
                elif menu == "4":
                    modify_task(task_selected, del_task=True)
                    menu = "va"
                    break
                else:
                    menu = "va"
                    break


    # Viewing all tasks of logged in user.
    elif menu == 'vm':
        header(f"\nTask Viewer\n\nHi {USERNAME.name}, this is what you still need to do.\n")
        view_mine(USERNAME)

        # create "temp list" in order to use the function "select_menu".
        # Index tasks of only iterating over tasks assigned to user.
        count = iter(str(num) for num in range(1, len(task_list) + 1))
        temp_list = [next(count) for task in task_list if task.user == USERNAME.name]
        # Include "m" for the option of exiting to main menu.
        temp_list.append("m")

        # Request user to input options from "menu_v_"
        menu = select_menu(menu_v_, temp_list, 7)

        for num in temp_list:
            # Check if user chose a valid task.
            if menu == num:
                # If user decides to return to main menu:
                if menu == "m":
                    break
                # If user decides to view a selected task:
                # Determine the selected task.
                task_selected = task_list[int(menu) - 1]
                while True:
                    view_task(task_selected)
                    # Request user to input options from "menu_vm"
                    menu = select_menu(menu_vm, ["1", "m"], 7)
                    # If user decides to change the completion status of selected task:
                    if menu == "1":
                        modify_task(task_selected, yes_no=True)
                        view_task(task_selected)
                    else:
                        menu = "vm"
                        break

    # Generate reports (Only visible to ADMIN)
    elif menu == 'gr' and USERNAME.role == "admin":
        header("Generating reports...\n")
        stats_generate()
        input("Press ENTER to return to main menu.")
        menu = "m"
    # Viewing statistics (Only visible to ADMIN).
    elif menu == 'ds' and USERNAME.role == "admin":
        #read stats from text file
        stats_read(TASK_OVERVIEW_TXT, USER_OVERVIEW_TXT)
        # Return to main menu.
        input("Press ENTER to return to main menu.")
        menu = 'm'
    # Print exit message upon user exit.
    elif menu == 'e':
        header("\nGoodbye!!!\nSee you again soon...\n")
        exit()
    # Return to main menu after incorrect input from user.
    else:
        if menu != "-1":   # See comment on last line
            input("You have entered an invalid input."
                  "Press ENTER to return try again.")
        menu = "m"
#endregion
