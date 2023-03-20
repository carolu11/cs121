"""
Student name(s): Carolyn Lu, Teresa Huang
Student email(s): cwlu@caltech.edu, thhuang@caltech.edu

This program includes all of the command-line functionalities of our Leetcode
Recommender System, incorporating both client and admin user features. Options
include logging in, creating users, getting a problem recommended, and checking
related data for a user.
"""
import sys  # to print error messages to sys.stderr
import mysql.connector
# To get error codes from the connector, useful for user-friendly
# error-handling
import mysql.connector.errorcode as errorcode

# Debugging flag to print errors when debugging that shouldn't be visible
# to an actual client. Set to False when done testing.
DEBUG = False


# ----------------------------------------------------------------------
# SQL Utility Functions
# ----------------------------------------------------------------------
def get_conn():
    """"
    Returns a connected MySQL connector instance, if connection is successful.
    If unsuccessful, exits.
    """
    try:
        conn = mysql.connector.connect(
          host='localhost',
          user='appadmin',
          # Find port in MAMP or MySQL Workbench GUI or with
          # SHOW VARIABLES WHERE variable_name LIKE 'port';
          port='3306',
          password='adminpw',
          database='finaldb'
        )
        print('Successfully connected.')
        return conn
    except mysql.connector.Error as err:
        # Remember that this is specific to _database_ users, not
        # application users. So is probably irrelevant to a client in your
        # simulated program. Their user information would be in a users table
        # specific to your database.
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR and DEBUG:
            sys.stderr('Incorrect username or password when connecting to DB.')
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            sys.stderr('Database does not exist.')
        elif DEBUG:
            sys.stderr(err)
        else:
            sys.stderr('An error occurred, please contact the administrator.')
        sys.exit(1)


# ----------------------------------------------------------------------
# Functions for Command-Line Options/Query Execution
# ----------------------------------------------------------------------
def add_users():
    '''
    Creates and adds new users to the database system. Note that it assumes the
    user does not exist. If the user exists, then the program crashes.
    '''
    cursor = conn.cursor()
    username = input('Create a username: ')
    password = input('Create a password: ')
    insert_username = '''
        INSERT INTO users (username, is_admin) VALUES 
            (\'%s\', 0);''' % (username, )
    sql = 'CALL sp_add_user(\'%s\', \'%s\');' % (username, password, )
    try:
        cursor.execute(insert_username)
        conn.commit()
        cursor.execute(sql)
        conn.commit()
        print("Successfully added new user!")
        show_options()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, please notify cwlu@caltech.edu ' + \
                       'and thhuang@caltech.edu!''')
            
def find_genres_answered():
    '''
    Finds the total number of problems completed under each genre given a
    user's inputted username.
    '''
    cursor = conn.cursor()
    try:
        inp = input("What is your username? ").strip()
        find_user_id = 'SELECT user_id FROM users WHERE username=\'%s\'' % (inp, )
        cursor.execute(find_user_id)
        rows = cursor.fetchall()
        if len(rows) == 0:
            print(f'No user found with username "{inp}"! ' + \
                   'Please create a new user or try again.')
            show_options()
            return
        else:
            user_id = rows[0][0]
        
        genres_answered = '''
            SELECT genre, COUNT(problem_id) AS num_answered 
            FROM genres NATURAL JOIN completed_problems
            WHERE user_id = %s
            GROUP BY genre 
            ORDER BY genre;''' % (user_id, )
        cursor.execute(genres_answered)
        rows = cursor.fetchall()
        print()
        if len(rows) == 0:
            print('No problems completed yet.')
        else:
            print('You have completed problems under the following genres:')
            for (genre, num) in rows:
                print(f'    {genre}, {num} problem(s)')

    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred when searching for genres of ' + \
                       'problems answered so far.')
            return
        
def find_num_problems_completed():
    '''
    Finds the total number of problems a user has completed given a user's 
    inputted username.
    '''
    cursor = conn.cursor()
    try:
        inp = input("What is your username? ").strip()
        find_user_id = 'SELECT user_id FROM users WHERE username=\'%s\'' % (inp, )
        cursor.execute(find_user_id)
        rows = cursor.fetchall()
        if len(rows) == 0:
            print(f'No user found with username "{inp}"! ' + \
                   'Please create a new user or try again.')
            show_options()
            return
        else:
            user_id = rows[0][0]
        
        problems_answered = '''
            SELECT num_problems_answered 
            FROM users 
            WHERE user_id = \'%s\'''' % (user_id, )
        cursor.execute(problems_answered)
        rows = cursor.fetchall()
        print()
        if len(rows) == 0:
            print('No problems completed yet.')
        else:
            print(f'You have completed {rows[0][0]} problem(s)!')

    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred when searching for the number ' + \
                       'of problems answered so far.')
            return
        
def find_num_problems_asked():
    '''
    Finds the total number of problems asked to a user given their inputted
    username.
    '''
    cursor = conn.cursor()
    try:
        inp = input("What is your username? ").strip()
        find_user_id = 'SELECT user_id FROM users WHERE username=\'%s\'' % (inp, )
        cursor.execute(find_user_id)
        rows = cursor.fetchall()
        if len(rows) == 0:
            print(f'No user found with username "{inp}"! ' + \
                   'Please create a new user or try again.')
            show_options()
            return
        else:
            user_id = rows[0][0]
        
        problems_asked = 'SELECT num_problems_asked(\'%s\')' % (user_id, )
        cursor.execute(problems_asked)
        rows = cursor.fetchall()
        print()
        if len(rows) == 0:
            print('No problems asked yet.')
        else:
            print(f'{rows[0][0]} problem(s) have been asked!')

    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred when searching for the number ' + \
                       'of problems answered so far.')
            return

def choose_genre():
    '''
    Finds the next problem to recommend to the user out of the remaining
    problems from a specific genre, including its related information
    (problem name, description, difficulty, and genre). Note that this does not
    include problems that have already been asked to a given user or a user has
    already completed.
    Genres are case-insensitive.
    '''
    cursor = conn.cursor()
    all_genres = 'SELECT * FROM distinct_genres;'
    try:
        inp = input("What is your username? ").strip()
        find_user_id = 'SELECT user_id FROM users WHERE username=\'%s\'' % (inp, )
        cursor.execute(find_user_id)
        rows = cursor.fetchall()
        if len(rows) == 0:
            print(f'No user found with username "{inp}"! ' + \
                   'Please create a new user or try again.')
            show_options()
            return
        else:
            user_id = rows[0][0]

        cursor.execute(all_genres)
        rows = cursor.fetchall()
        for row in rows:
            print(row[0])
        inp = input("Enter a genre listed above: ").strip().lower()

        check_genre = '''
            SELECT * FROM distinct_genres WHERE genre = \'%s\';''' % (inp, )
        get_problems = '''
            SELECT problem_id, problem_name, problem_text, difficulty, genre 
                FROM genres NATURAL JOIN problems
                WHERE UPPER(genre) = UPPER(\'%s\') AND (problem_id NOT IN 
                    (SELECT problem_id 
                    FROM asked_problems NATURAL JOIN completed_problems
                    WHERE user_id=\'%s\'))
                ORDER BY problem_id;''' % (inp, user_id)
        
        cursor.execute(check_genre)
        rows = cursor.fetchall()
        if len(rows) == 0:
            print('Not a valid genre.')
            inp = input("Would you like to enter another genre (y/n)? ")
            inp = inp.strip().lower()
            if inp == 'yes' or inp == 'y':
                show_options()
            else:
                sys.exit(1)
            return

        cursor.execute(get_problems)
        rows = cursor.fetchall()
        if len(rows) == 0:
            print(f'No more remaining problems under the {inp} genre!')
            inp = input("Would you like to enter another genre (y/n)? ")
            inp = inp.strip().lower()
            if inp == 'yes' or inp == 'y':
                show_options()
            else:
                sys.exit(1)
            return
        print()
        print(f'Here is a recommended problem: {rows[0][1]}')
        print(f'Genre: {rows[0][4]}')
        print(f'Difficulty: {rows[0][3]}\n')
        print(f'Problem description:\n{rows[0][2]}\n')
        problem_id = rows[0][0]

        add_to_asked = '''
            INSERT INTO asked_problems (user_id, problem_id) VALUES 
                (%s,%s);''' % (user_id, problem_id)
        cursor.execute(add_to_asked)
        conn.commit()

        inp = input("Did you complete this problem (y/n)? ").strip().lower()
        if inp == 'yes' or inp == 'y':
            add_to_completed = '''
                INSERT INTO completed_problems (user_id, problem_id) VALUES 
                    (%s,%s);''' % (user_id, problem_id)
            cursor.execute(add_to_completed)
            conn.commit()   

        inp = input("Would you like to see this problem's solution (y/n)? ")
        inp = inp.strip().lower()
        if inp == 'yes' or inp == 'y':
            get_solutions = '''
                SELECT solution, link
                FROM solutions
                WHERE problem_id=\'%s\'''' % (problem_id, )
            cursor.execute(get_solutions)
            rows = cursor.fetchall()
            print(rows[0][0])
            print()
            print(f'Here is the link to the solution: {rows[0][1]}')       
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred in searching for available problems.')
            return

def find_max_user():
    '''
    Finds the total number of problems asked to a user given their inputted
    username.
    '''
    cursor = conn.cursor()
    try:
        get_user = '''
            SELECT username, num_problems_answered
            FROM users WHERE num_problems_answered = 
                (SELECT MAX(num_problems_answered) FROM users);'''
        cursor.execute(get_user)
        rows = cursor.fetchall()
        print()
        for row in rows:
            print(f'{row[0]} has completed {row[1]} problems!')
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred in searching for available problems.')
            return

def choose_difficulty():
    '''
    Finds the next problem to recommend to the user from a specific difficulty, 
    including its related information (problem name, description, difficulty,
    and genre). Note that this does not include problems that have
    already been asked to a given user or a user has already completed.
    Difficulties are case-insensitive.
    '''
    cursor = conn.cursor()
    try:
        inp = input("What is your username? ").strip()
        find_user_id = 'SELECT user_id FROM users WHERE username=\'%s\'' % (inp, )
        cursor.execute(find_user_id)
        rows = cursor.fetchall()
        if len(rows) == 0:
            print(f'No user found with username "{inp}"! ' + \
                   'Please create a new user or try again.')
            show_options()
            return
        else:
            user_id = rows[0][0]

        diff = input("Enter a desired difficulty (Easy, Medium, or Hard): ")
        diff = diff.strip().lower()

        if diff != 'easy' and diff != 'medium' and diff != 'hard':
            print(f'Invalid difficulty level!')
            inp = input("Would you like to enter another difficulty (y/n)? ")
            inp = inp.strip().lower()
            if inp == 'yes' or inp == 'y':
                show_options()
            else:
                sys.exit(1)
            return
        
        get_problems = '''
            SELECT problem_id, problem_name, problem_text, difficulty, genre
                FROM problems NATURAL JOIN genres
                WHERE UPPER(difficulty) = UPPER(\'%s\') AND (problem_id NOT IN 
                    (SELECT problem_id 
                    FROM asked_problems NATURAL JOIN completed_problems
                    WHERE user_id=\'%s\'))
                ORDER BY problem_id;''' % (diff, user_id)

        cursor.execute(get_problems)
        rows = cursor.fetchall()
        if len(rows) == 0:
            print(f'No more remaining problems under the {inp} difficulty!')
            inp = input("Would you like to enter another difficulty (y/n)? ")
            inp = inp.strip().lower()
            if inp == 'yes' or inp == 'y':
                show_options()
            else:
                sys.exit(1)
            return
        print()
        print(f'Here is a recommended problem: {rows[0][1]}')
        print(f'Genre: {rows[0][4]}')
        print(f'Difficulty: {rows[0][3]}\n')
        print(f'Problem description:\n{rows[0][2]}\n')
        problem_id = rows[0][0]

        add_to_asked = '''
            INSERT INTO asked_problems (user_id, problem_id) VALUES 
                (%s,%s);''' % (user_id, problem_id)
        cursor.execute(add_to_asked)
        conn.commit()

        inp = input("Did you complete this problem (y/n)? ").strip().lower()
        if inp == 'yes' or inp == 'y':
            add_to_completed = '''
                INSERT INTO completed_problems (user_id, problem_id) VALUES 
                    (%s,%s);''' % (user_id, problem_id)
            cursor.execute(add_to_completed)
            conn.commit()   

        inp = input("Would you like to see this problem's solution (y/n)? ")
        inp = inp.strip().lower()
        if inp == 'yes' or inp == 'y':
            get_solutions = '''
                SELECT solution, link
                FROM solutions
                WHERE problem_id=\'%s\'''' % (problem_id, )
            cursor.execute(get_solutions)
            rows = cursor.fetchall()
            print(rows[0][0])
            print()
            print(f'Here is the link to the solution: {rows[0][1]}')       
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred in searching for available problems.')
            return
        

# ----------------------------------------------------------------------
# Functions for Logging Users In
# (only logs in, doesn't add users)
# ----------------------------------------------------------------------
def login():
    '''
    Logs the user in given the user inputted username and password.
    '''
    cursor = conn.cursor()

    while True:
        username = input('Username: ')
        password = input('Password: ')
        sql = "SELECT authenticate(\'%s\', \'%s\');" % (username, password, )
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            if len(rows) == 0:
                print('Account not found!')
                continue
            else: 
                if rows[0][0] == 1:
                    print("Successfully logged in!\n")
                    show_options()
                    return
                else:
                    print("Incorrect password/account not found!\n")
                    show_options()
                    break
        except mysql.connector.Error as err:
            if DEBUG:
                sys.stderr(err)
                sys.exit(1)
            else:
                sys.stderr('Error, could not login! Please notify ' + \
                           'cwlu@caltech.edu and thhuang@caltech.edu!')


# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------
def show_options():
    """
    Displays options users can choose in the application, such as
    viewing <x>, filtering results with a flag (e.g. -s to sort),
    sending a request to do <x>, etc.
    """
    print('What would you like to do? ')
    print('  (c) - Create a new account')
    print('  (l) - Login')
    print('  (i) - Get genres of problems answered so far')
    print('  (ii) - Get number of problems answered')
    print('  (iii) - Get number of problems asked')
    print('  (g) - Find a problem with a certain genre to practice')
    print('  (d) - Find a problem with a certain difficulty to practice')
    print('  (t) - Find user with most problems answered')
    print('  (p) - Enter a password to unlock admin responsibilities')
    print('  (q) - quit')
    print()
    ans = input('Enter an option: ').lower()
    if ans == 'q':
        quit_ui()
    elif ans == 'l':
        login()
    elif ans == 'i':
        find_genres_answered()
    elif ans == 'ii':
        find_num_problems_completed()
    elif ans == 'iii':
        find_num_problems_asked()
    elif ans == 'g':
        choose_genre()
    elif ans == 'd':
        choose_difficulty()
    elif ans == 't':
        find_max_user()
    elif ans == 'c':
        add_users()
    elif ans == 'p':
        inp = input("Enter the password: ")
        if inp.lower().strip() == 'welovecoding':
            print("Successfully entered admin portal!")
            print()
            show_admin_options()
        else:
            print("Incorrect password.")
            show_options()
    elif ans == '':
        sys.exit(1)  

def show_admin_options():
    """
    Displays admin user specific features, such as logging in to an admin 
    account and adding new users.
    """
    print('What would you like to do? ')
    print('  (l) - Login')
    print('  (a) - Create and add new users')
    print('  (q) - Quit')
    print()
    ans = input('Enter an option: ').lower()
    if ans == 'q':
        quit_ui()
    elif ans == 'l':
        login()
    elif ans == 'c':
        add_users()
    elif ans == '':
        sys.exit(1)

def quit_ui():
    """
    Quits the program, printing a good bye message to the user.
    """
    print('Good bye!')
    exit()


def main():
    """
    Main function for starting things up.
    """
    show_options()


if __name__ == '__main__':
    conn = get_conn()
    main()