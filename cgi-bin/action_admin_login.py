import sportslib, hashlib, uuid 

class Action:

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
