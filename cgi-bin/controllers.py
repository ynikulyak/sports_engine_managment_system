import sportslib, hashlib

# Regular user controllers

class About:

    """
    About controller

    Parameters:
    database_connection (mysql.connector.connection) - MySQL database connection
    arguments (cgi.arguments - HTML form fields and GET arguments
    cookies (dict) - cookies as a dictionary
    """
    def execute(self, database_connection, arguments, cookies):
        return {}

class Home:

    """
    Home contoller

    Parameters:
    database_connection (mysql.connector.connection) - MySQL database connection
    arguments (cgi.arguments - HTML form fields and GET arguments
    cookies (dict) - cookies as a dictionary
    """
    def execute(self, database_connection, arguments, cookies):
        # search.py is responsible for searching on site
        return {'TABLE_OF_SPORT_DATA': '', 'error': '', 'QUERY': ''}

import sportslib

# Admin related controllers

class AdminDivisions:

    sql = "SELECT d.division_id, d.division_name, s.sport_name FROM division d LEFT JOIN sports s ON d.sport_id = s.sport_id ORDER BY d.division_id"

    """
    Admin divisions controller

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
        table = sportslib.HTMLTable("ID", "Name", "Sport", "Edit", "Delete")
        row = cursor.fetchone()
        while row is not None:
            link = sportslib.Link("admin_division_edit", row[0], str(row[0]))
            edit_link = sportslib.Link("admin_division_edit", row[0], "edit")
            table.add_row(link, row[1], row[2], edit_link, 'X')
            row = cursor.fetchone()
        return {'TABLE_OF_DIVISIONS': table}


class AdminDivisionEdit:

    select_sql = "SELECT * FROM division WHERE division_id = %s LIMIT 1"
    insert_sql = "INSERT INTO division (division_name, sport_id) VALUES (%s, %s)"
    update_sql = "UPDATE division SET division_name = %s, sport_id = %s WHERE division_id = %s LIMIT 1"

    list_of_sports_sql = "SELECT sport_id, sport_name FROM sports ORDER BY sport_name"


    """
    Admin add/edit division controller

    Parameters:
    database_connection (mysql.connector.connection) - MySQL database connection
    arguments (cgi.arguments - HTML form fields and GET arguments
    cookies (dict) - cookies as a dictionary
    """
    def execute(self, database_connection, arguments, cookies):
        select_of_sports = self.build_select_of_sports(database_connection)
        division_id = arguments.getvalue("id", "")
        data = {
            'id': division_id, 
            'division_name': arguments.getvalue("division_name", "").strip(),
            'sport_id': arguments.getvalue("sport_id", "").strip(),
            'action_title': 'Add',
            'error': '',
            'SELECT_OF_SPORTS': select_of_sports
        }
        if "save" == arguments.getvalue("submit", ""):
            return self.save(database_connection, arguments, cookies, data)
        row = None
        if division_id:
            cursor = database_connection.cursor()
            cursor.execute(self.select_sql, (division_id,))
            row = cursor.fetchone()
            if not row:
                data['error'] = 'Division ' + division_id + ' not found.'
                data['id'] = ''
                return data
            data['id'] = row[0]
            data['division_name'] = row[1]
            data['sport_id'] = row[2] 
            data['action_title'] = 'Edit'
            select_of_sports.set_selected(data['sport_id'])
        return data

    def save(self, database_connection, arguments, cookies, data):
        if data['division_name'] == '' or data['sport_id'] == '':
            data['error'] = 'All fields are required'
            return data
        cursor = database_connection.cursor()
        if data['id'] == '':
            cursor.execute(self.insert_sql, (data['division_name'], data['sport_id']))
        else:
            cursor.execute(self.update_sql, (data['division_name'], data['sport_id'], data['id']))
        database_connection.commit()
        data['location'] = sportslib.Link('admin_divisions').url()
        return data

    def build_select_of_sports(self, database_connection):
        cursor = database_connection.cursor()
        cursor.execute(self.list_of_sports_sql)
        select = sportslib.HTMLSelect('sports', 'sport_id')
        row = cursor.fetchone()
        while row is not None:
            select_id = str(row[0])
            select_title = row[1]
            select.add_option(select_id, select_title)
            row = cursor.fetchone()
        return select




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
                data['id'] = ''
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

class AdminTeams:

    sql = "SELECT * FROM team ORDER BY team_id"

    """
    Admin team controller

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
        table = sportslib.HTMLTable("ID", "Team Name", "Sport_ID", "Division_ID", "Edit", "Delete")
        row = cursor.fetchone()
        while row is not None:
            link = sportslib.Link("admin_team_edit", row[0], str(row[0]))
            edit_link = sportslib.Link("admin_team_edit", row[0], "edit")
            table.add_row(link, row[1], row[2], row[3], edit_link, 'X')
            row = cursor.fetchone()

        return {'TABLE_OF_TEAMS': table}


class AdminTeamEdit:

    select_sql = "SELECT * FROM team WHERE team_id = %s LIMIT 1"
    insert_sql = "INSERT INTO team (team_name, sport_id, division-id) VALUES (%s, %s, %s)"
    update_sql = "UPDATE team SET team_name = %s, sport_id = %s, division_id = %s WHERE team_id = %s LIMIT 1"


    """
    Admin add/edit team controller

    Parameters:
    database_connection (mysql.connector.connection) - MySQL database connection
    arguments (cgi.arguments - HTML form fields and GET arguments
    cookies (dict) - cookies as a dictionary
    """
    def execute(self, database_connection, arguments, cookies):
        team_id = arguments.getvalue("id", "")
        data = {
            'id': team_id, 
            'team_name': arguments.getvalue("team_name", "").strip(),
            'sport_id': arguments.getvalue("sport_id", "").strip(),
	    'division_id': arguments.getvalue("division_id", "").strip(),
            'action_title': 'Add',
            'error': ''
        }
        if "save" == arguments.getvalue("submit", ""):
            return self.save(database_connection, arguments, cookies, data)
        row = None
        if team_id:
            cursor = database_connection.cursor()
            cursor.execute(self.select_sql, (team_id,))
            row = cursor.fetchone()
            if not row:
                data['error'] = 'Team ' + team_id + ' not found.'
                data['id'] = ''
                return data
            data['id'] = row[0]
            data['team_name'] = row[1]
            data['sport_id'] = row[2] 
            data['division_id'] = row[3] 
            data['action_title'] = 'Edit'
        return data

    def save(self, database_connection, arguments, cookies, data):
        if data['id'] == '' or data['team_name'] == '' or data['sport_id'] == '' or data['division_id'] == '':
            data['error'] = 'All fields are required'
            return data
        cursor = database_connection.cursor()
        if data['id'] == '':
            cursor.execute(self.insert_sql, (data['team_name'], data['sport_id'], data['division_id']))
        else:
            cursor.execute(self.update_sql, (data['team_name'], data['sport_id'], data['division_id'], data['id']))
        database_connection.commit()
        data['location'] = sportslib.Link('admin_teams').url()
        return data





class AdminPlayers:

    sql = "SELECT * FROM player ORDER BY player_id"

    """
    Admin players controller

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
    Admin add/edit player controller

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
                data['id'] = ''
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
    Admin login controller

    Parameters:
    database_connection (mysql.connector.connection) - MySQL database connection
    arguments (cgi.arguments - HTML form fields and GET arguments
    cookies (dict) - cookies as a dictionary
    """
    def execute(self, database_connection, arguments, cookies):
        data = {'error': ''}
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
    Admin logout controller

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
