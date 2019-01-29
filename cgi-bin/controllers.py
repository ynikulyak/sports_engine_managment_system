import sportslib, hashlib, uuid 

# Regular user controllers

class About:

    """
    About action

    Parameters:
    database_connection (mysql.connector.connection) - MySQL database connection
    arguments (cgi.arguments - HTML form fields and GET arguments
    cookies (dict) - cookies as a dictionary
    """
    def execute(self, database_connection, arguments, cookies):
        # TODO: read database here
        return {}

class Home:

    """
    Home action

    Parameters:
    database_connection (mysql.connector.connection) - MySQL database connection
    arguments (cgi.arguments - HTML form fields and GET arguments
    cookies (dict) - cookies as a dictionary
    """
    def execute(self, database_connection, arguments, cookies):
    	# TODO: read database here
        return {}

import sportslib

# Admin related controllers

class AdminSports:

    sql = "SELECT * FROM sports ORDER BY sport_id"

    """
    Admin sports action

    Parameters:
    database_connection (mysql.connector.connection) - MySQL database connection
    arguments (cgi.arguments - HTML form fields and GET arguments
    cookies (dict) - cookies as a dictionary
	Returns:
	dictionary (dict) of contents variable to render
    """
    def execute(self, database_connection, arguments, cookies):
        cursor = database_connection.cursor()
        cursor.execute(self.sql)

        table = sportslib.HTMLTable("ID", "Sport", "Description", "Edit", "Delete")
        row = cursor.fetchone()
        while row is not None:
            link = sportslib.Link("admin_sport_edit", row[0], str(row[0]))
            edit_link = sportslib.Link("admin_sport_edit", row[0], "edit")
            delete_link = sportslib.Link("admin_sport_delete", row[0], "X")
            table.add_row(link, row[1], row[2], edit_link, delete_link)
            row = cursor.fetchone()

        return {
        	'TABLE_OF_SPORTS': table,
        	'logged_in_user_id': sportslib.get_logged_in_user_id()
        }


class AdminSportEdit:

    sql = "SELECT * FROM sports WHERE sport_id = %s LIMIT 1"

    """
    Admin add/edit sport action

    Parameters:
    database_connection (mysql.connector.connection) - MySQL database connection
    arguments (cgi.arguments - HTML form fields and GET arguments
    cookies (dict) - cookies as a dictionary
    """
    def execute(self, database_connection, arguments, cookies):
        sport_id = arguments.getvalue("id", "")
        data = {
            'id': sport_id, 
            'title': arguments.getvalue("title", ""),
            'description': arguments.getvalue("description", ""),
            'action_title': 'Add'
        }
        row = None
        if sport_id:
            cursor = database_connection.cursor()
            cursor.execute(self.sql, (sport_id,))
            row = cursor.fetchone()
            if not row:
                return data
            data['id'] = row[0]
            data['title'] = row[1]
            data['description'] = row[2] 
            data['action_title'] = 'Edit'
        return data

class AdminLogin:

    sql = "SELECT admin_id FROM admin WHERE admin_user_name = %s and admin_password = %s"

    """
    Admin login action

    Parameters:
    database_connection (mysql.connector.connection) - MySQL database connection
    arguments (cgi.arguments - HTML form fields and GET arguments
    cookies (dict) - cookies as a dictionary
    """
    def execute(self, database_connection, arguments, cookies):
        data = {
          'random_id': uuid.uuid1(), 
          'error': ''
        }
        login = arguments.getvalue("username", "").strip()
        password = hashlib.sha1(arguments.getvalue("password", "").encode('utf-8')).hexdigest()
        submit = arguments.getvalue("submit", "").strip()
        if login and password and submit:
            cursor = database_connection.cursor()
            cursor.execute(self.sql, (login, password))
            row = cursor.fetchone()
            if row:
                data['cookies'] = {
                    'auth': sportslib.build_auth_cookie(row[0])
                }
                # Redirect to sports list admin page.
                data['location'] = sportslib.Link('admin_sports').url()
                return data
        if submit:
            data['error'] = 'Wrong login or password.'
        if sportslib.get_logged_in_user_id():
            data['location'] = sportslib.Link('admin_sports').url()
        return data

class AdminLogout:

    """
    Admin logout action

    Parameters:
    database_connection (mysql.connector.connection) - MySQL database connection
    arguments (cgi.arguments - HTML form fields and GET arguments
    cookies (dict) - cookies as a dictionary
    """
    def execute(self, database_connection, arguments, cookies):
        return {
          'cookies': {
             'auth': '_',
          },
          'location': sportslib.Link('admin_login').url()
        }
