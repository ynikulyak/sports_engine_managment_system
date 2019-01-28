import sportslib

class Action:

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
