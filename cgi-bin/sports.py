import appconfig, cgi, mysql.connector

# User actions
import action_about
import action_home

# Admin
import action_admin_login
import action_admin_logout
import action_admin_sports
import action_admin_sport_edit

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
            'home': action_home.Action(),
            'about': action_about.Action(),
            # Admin
            'admin_login': action_admin_login.Action(),
            'admin_logout': action_admin_logout.Action(),
            'admin_sports': action_admin_sports.Action(),
            'admin_sport_edit': action_admin_sport_edit.Action()
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
        result = {}
        try:
            self.database_connection = mysql.connector.connect(
                user=appconfig.database_user,
                password=appconfig.database_password,
                database=appconfig.database_name,
                host=appconfig.database_host)
            result = self.actionInstance.execute(
                self.database_connection, 
                self.arguments, 
                self.cookies)
        except mysql.connector.Error as err:
            result['error'] = str(err)
        finally:
            if self.database_connection:
                self.database_connection.close()
                self.database_connection = None
        return result