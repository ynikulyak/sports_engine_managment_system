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
            table.add_row(link, row[1], row[2], edit_link, 'X')
            row = cursor.fetchone()

        return {'TABLE_OF_SPORTS': table}


class AdminSportEdit:

    select_sql = "SELECT * FROM sports WHERE sport_id = %s LIMIT 1"
    insert_sql = "INSERT INTO sports (sport_name, sport_description) VALUES (%s, %s)"
    update_sql = "UPDATE sports SET sport_name = %s, sport_description = %s WHERE sport_id = %s LIMIT 1"


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
            'title': arguments.getvalue("title", "").strip(),
            'description': arguments.getvalue("description", "").strip(),
            'action_title': 'Add',
            'error': ''
        }
        if "save" == arguments.getvalue("submit", ""):
            return self.save(database_connection, arguments, cookies, data)
        row = None
        if sport_id:
            cursor = database_connection.cursor()
            cursor.execute(self.select_sql, (sport_id,))
            row = cursor.fetchone()
            if not row:
                data['error'] = 'Sport ' + sport_id + ' not found.'
                return data
            data['id'] = row[0]
            data['title'] = row[1]
            data['description'] = row[2] 
            data['action_title'] = 'Edit'
        return data

    def save(self, database_connection, arguments, cookies, data):
        if data['title'] == '' or data['description'] == '':
            data['error'] = 'All fields are required'
            return data
        cursor = database_connection.cursor()
        if data['id'] == '':
            cursor.execute(self.insert_sql, (data['title'], data['description']))
        else:
            cursor.execute(self.update_sql, (data['title'], data['description'], data['id']))
        database_connection.commit()
        data['location'] = sportslib.Link('admin_sports').url()
        return data


class AdminPlayers:

    sql = "SELECT * FROM player ORDER BY player_id"

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

        table = sportslib.HTMLTable("ID", "First Name", "Last Name", "Position", "Edit", "Delete")
        row = cursor.fetchone()
        while row is not None:
            link = sportslib.Link("admin_player_edit", row[0], str(row[0]))
            edit_link = sportslib.Link("admin_player_edit", row[0], "edit")
            table.add_row(link, row[1], row[2], row[3], edit_link, 'X')
            row = cursor.fetchone()

        return {'TABLE_OF_PLAYERS': table}


class AdminPlayerEdit:

    select_sql = "SELECT * FROM player WHERE player_id = %s LIMIT 1"
    insert_sql = "INSERT INTO player (player_first_name, player_last_name, player_position) VALUES (%s, %s, %s)"
    update_sql = "UPDATE player SET player_first_name = %s, player_last_name = %s, player_position = %s WHERE player_id = %s LIMIT 1"


    """
    Admin add/edit sport action

    Parameters:
    database_connection (mysql.connector.connection) - MySQL database connection
    arguments (cgi.arguments - HTML form fields and GET arguments
    cookies (dict) - cookies as a dictionary
    """
    def execute(self, database_connection, arguments, cookies):
        player_id = arguments.getvalue("id", "")
        data = {
            'id': player_id, 
            'first_name': arguments.getvalue("first_name", "").strip(),
            'last_name': arguments.getvalue("last_name", "").strip(),
            'player_position': arguments.getvalue("player_position", "").strip(),
            'action_title': 'Add',
            'error': ''
        }
        if "save" == arguments.getvalue("submit", ""):
            return self.save(database_connection, arguments, cookies, data)
        row = None
        if player_id:
            cursor = database_connection.cursor()
            cursor.execute(self.select_sql, (player_id,))
            row = cursor.fetchone()
            if not row:
                data['error'] = 'Player ' + player_id + ' not found.'
                return data
            data['id'] = row[0]
            data['first_name'] = row[1]
            data['last_name'] = row[2] 
            data['player_position'] = row[3] 
            data['action_title'] = 'Edit'
        return data

    def save(self, database_connection, arguments, cookies, data):
        if data['first_name'] == '' or data['last_name'] == '' or data['player_position'] == '':
            data['error'] = 'All fields are required'
            return data
        cursor = database_connection.cursor()
        if data['id'] == '':
            cursor.execute(self.insert_sql, (data['first_name'], data['last_name'], data['player_position']))
        else:
            cursor.execute(self.update_sql, (data['first_name'], data['last_name'], data['player_position'], data['id']))
        database_connection.commit()
        data['location'] = sportslib.Link('admin_players').url()
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
