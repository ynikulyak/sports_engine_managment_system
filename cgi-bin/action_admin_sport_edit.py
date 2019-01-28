import sportslib

class Action:

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



        
