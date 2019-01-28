import sportslib

class Action:

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
