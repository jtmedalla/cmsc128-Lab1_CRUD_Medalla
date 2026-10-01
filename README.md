**Which tech stack/backend/database you chose and why?**

The original plan was to use the C++, Qt, and SQLite tech stack for this project.
However, due to time constraints, I decided to pivot to using Python, PyQt6, and SQLite instead.

While not the best in UI/UX, the tech stack allows for rapid development due to its great writability. 

**Python** excels with its huge amount of available libraries for use to integrate features in the code. 

**SQLite** is an easy way to store data in a local database and is able to integrate SQL statements in the Python code.

**PyQt** is a great library for creating GUI applications, but it has a steep learning curve and requires more time to learn.

Overall, the tech stack is excellent in developing simple applications, like a to-do app.

**How to run the app locally (setup steps, dependencies, commands)**

To run locally, execute the following commands in the terminal:
```bash
# clone the repository
git clone

# change directory to the project folder
cd cmsc128-lab1_CRUD_Medalla

# create a virtual environment

# for linux 
python3 -m venv .venv

# for windows
python -m venv .venv

# activate the virtual environment
# for linux
source .venv/bin/activate

# for windows
.venv\Scripts\activate

# install dependencies
# install pip if not installed
# for linux
python3 -m ensurepip --upgrade

# for windows
python -m ensurepip --upgrade

# if installed
python -m pip install --upgrade pip

# then run the following command to install dependencies
pip install -r requirements.txt

# run the app
./run
```

**Example "API endpoints" or data operations (however your stack exposes CRUD — REST routes, Firestore calls, local DB queries, etc.)**
CRUD operations are done through the `SQLiteConn` class in `api/sqlite3_api.py`. The following methods are available for use:

- open() - Used to open the database connection. Automatically creates the database file if it does not exist.
- close() - Used to close the database connection.
- execute(query, params=None) - Used to execute a SQL query as string with optional parameters.
- add_entry(title, dateAdded, dateDue, priority, category, details, completion=False) - Used to add a new task entry to the database. Returns the id that the database assigned the entry
- remove_entry(taskID) - Used to remove a task entry from the database by its id.
- update_entry(taskID, title=None, dateAdded=None, dateDue=None, priority=None, category=None, details=None, completion=None) - Used to update a task entry in the database by its id.
- fetch_all_entries() - Used to fetch all task entries from the database. Returns a list of Task objects. or None if there are no entries in the database.
- fetch_entry_by_id(taskID) - Used to fetch a task entry from the database by its id. Returns a Task object or None if the entry does not exist.
- toggle_entry_completion(taskID) - Used to toggle the completion status of a task entry in the database by its id.
- add_user(username, password) - Used to add a new user to the database. Returns True if the user was added successfully, False if the user already exists.
- update_user_info(username, new_username=None, new_password=None) - Used to update a user's information in the database. Returns True if the user was updated successfully, False if the user does not exist.
- get_username_by_id(userID) - Used to fetch a username from the database by its id. Returns the username as a string or None if the user does not exist.
- authenticate_user(username, password) - Used to check if a user exists in the database with the corresponding password is correct. Returns the userID if the user exists and the password is correct, None otherwise.
- create_session(userID) - Used to create a new session for a user. Returns the session token if the session was created successfully, None otherwise.
- compare_token(candidate_token) - Used to compare a token stored in the database with the current session token. Returns the userID if the tokens match, None otherwise.
- restore_session() - Used to restore a session from a token. Returns the userID if the session was restored successfully, None otherwise.
- logout() - Used to log out the current user and delete the session token from the database. 
- username_exists(username, exlude_userID=None) - Used to check if a username exists in the database. Returns True if the username exists, False otherwise. If exclude_userID is provided, the method will ignore that userID when checking for existence.
- add_user(username, password, question_1, answer_1, question_2, answer_2) - Used to add a new user to the database with security questions. Returns True if the user was added successfully, False if the user already exists.
- reset_password(username, answer_1, answer_2, new_password) - Used to reset a user's password in the database. Returns True if the password was reset successfully, False if the user does not exist or the answers to the security questions are incorrect.

**Session Storage**
The session works by storing a token in the database that is associated with the userID. When a user logs in, a new session is created and the token is stored in the database. Additionally, a token is stored in the operating system's keyring. When the user opens the app again, the session is restored by comparing the token stored in the database with the current session token stored in the operating system. If they match, the user is logged in automatically.

**Password Recovery Mechanism**
The password recovery mechanism works by asking the user to answer two security questions that they set up when they created their account. If the answers are correct, the new password that the user provided is set. 

**Screenshots of the working app**

The application is currently migrating to a new GUI framework (from tkinter to PyQt6). After the migration is complete, this section would be updated with screenshots of the working app.

cmsc128-Indiv-Act1-finalX
cmsc128-Indiv-Act2-finalX