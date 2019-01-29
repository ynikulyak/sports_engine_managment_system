import appconfig, cgi, mysql.connector, controllers

"""
Main application class that opens MySQL connection and execute
desired action.
"""
class Application:
    """
    Class constructor.

    Parameters:
    action (string) - action name to execute
    arguments (cgi.arguments) - GCI form arguments
    """
    def __init__(self, action, arguments, cookies):
        # Build a map of actions that application knows about.
        self.actions = {
            # User actions
            'home': controllers.Home(),
            'about': controllers.About(),
            # Admin
            'admin_login': controllers.AdminLogin(),
            'admin_logout': controllers.AdminLogout(),
            'admin_sports': controllers.AdminSports(),
            'admin_sport_edit': controllers.AdminSportEdit(),
            'admin_players': controllers.AdminPlayers(),
            'admin_player_edit': controllers.AdminPlayerEdit()
        }
        if action not in self.actions.keys():
            raise ValueError('Action ' + action + ' is not implemented.')
        self.action = action
        self.actionInstance = self.actions[action]
        self.arguments = arguments
        self.cookies = cookies

    """
    Starts application by connecting to MySQL and executing desired
    action.
    Returns:
    dictionary (dict) - Dictionary of parameters to render in template.
      If dictionary contains key "cookies" then key processes as dictionary
      of cookie names and values and all the cookies are set before sending contents headers.
      If dictionary contains key "location" then its value treated as HTML redirect.
    """
    def start(self):
        result = {'error': ''}
        try:
            self.database_connection = mysql.connector.connect(
                user=appconfig.database_user,
                password=appconfig.database_password,
                database=appconfig.database_name,
                host=appconfig.database_host)
            if not self.database_connection:
                result['error'] = 'No MySQL connection'
            else: 
                result = self.actionInstance.execute(
                    self.database_connection, 
                    self.arguments, 
                    self.cookies)
                if 'error' not in result.keys():
                    result['error'] = ''
        except mysql.connector.Error as err:
            result['error'] = str(err)
        finally:
            if self.database_connection:
                self.database_connection.close()
                self.database_connection = None
        return result