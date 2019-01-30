import appconfig, cgi, re, os, html, urllib.parse, hashlib

app_base_path = "/cgi-bin/index.py?"
redirect_template_path = "./redirect.html"

"""
HTML table helper to build HTML tables.
"""
class Link:

    def __init__(self, action, id = "", title = "", css_classes = ""):
        self.action = action
        self.title = title
        self.id = id
        self.css_classes = css_classes

    def url(self):
        url = app_base_path + 'action=' + url_encode(self.action)
        if self.id:
            url += "&id=" + url_encode(str(self.id))
        return url

    def __str__(self):
        link = '<a class="action-' + self.action
        if self.css_classes:
            link += ' ' + self.css_classes
        link += '" href="' + self.url() + '">'
        link += encode_html_entities(self.title)
        link += '</a>'
        return link

"""
HTML table helper to build HTML tables.
"""
class HTMLTable:
    default_css_classes = 'table table-hover table-bordered table-condensed table-striped'

    def __init__(self, *table_titles):
        self.rows = [] # rows as strings
        self.titles = []
        for title in table_titles: 
            self.titles.append(title)

    def add_row(self, *columns):
        html_row = "<tr>"
        index = 1
        for column in columns:
            html_row += '<td class="row_' + str(index) + '">' 
            if isinstance(column, str):
                html_row += encode_html_entities(str(column)) 
            else:
                html_row += str(column) 
            html_row += "</td>"
            index += 1
        html_row += "</tr>"
        self.rows.append(html_row)
        
    def __str__(self):
        result = '<table class="' + self.default_css_classes + '"><tr>'
        index = 1
        for title in self.titles:
            result += '<th class="rowheader_' + str(index) + '"">'
            result += encode_html_entities(title)
            result += "</th>\n"
            index += 1
        result += "</tr>\n"
        for row in self.rows:
            result += row + "\n"
        return result + "</table>"


class HTMLSelect:
    default_css_classes = 'form-control'

    def __init__(self, select_name, field_name):
        self.select_name = select_name
        self.field_name = field_name
        self.selected = str(-1)
        self.options = []

    def add_option(self, id, title):
        self.options.append((str(id), str(title)))

    def set_selected(self, id):
        self.selected = str(id)

    def __str__(self):
        result = '<select class="' + self.default_css_classes + '" id="' + self.field_name + '" name="' + self.field_name + '">'
        result += '<option value="">-- choose ' + self.select_name + '-- </option>'
        index = 1
        for option in self.options:
            result += '<option class="option_' + str(index) + '" '
            if option[0] == self.selected:
                result += ' selected '    
            result += 'value="' + encode_html_entities(option[0]) + '">'
            result += encode_html_entities(option[1]) + '</option>'
            index += 1
        return result + "</select>"

# Body template dynamic contents
base_path_placeholder = '[#BASE_PATH#]'
log_out_button_placeholder = '[#LOG_OUT_BUTTON#]'
def build_template(template_contents, parameters):
    """
    Builds given template by replacing variables with given values.
    """
    result = template_contents
    user_id = get_logged_in_user_id()
    logout_button = ''
    if isinstance(parameters, dict):
        for key in parameters:
            value = parameters[key]
            if isinstance(value, str):
                value = encode_html_entities(value)
            else:
                value = str(value)
            template_variable = '[#' + key + '#]' 
            result = result.replace(template_variable, value)
    result = result.replace(base_path_placeholder, app_base_path)
    if user_id:
        logout_button = Link('admin_logout', '', 'Log out', 'pull-right btn')
    result = result.replace(log_out_button_placeholder, str(logout_button))
    return result

def get_logged_in_user_id():
    """
    Returns logged in user id from cookies. Very weak and simple auth.
    Returns
    user_id (string) - user_id as string or if there is no logged in user
    """
    cookies = get_cookies()
    if 'auth' in cookies.keys():
        data = cookies['auth'].split('--')
        if len(data) < 2:
            return None
        signature = hashlib.sha1((appconfig.secret + data[1]).encode('utf-8')).hexdigest()
        # Only allow user if SHA1 signature matches
        if signature == data[0]:
            return data[1]
    # No cookie or wrong signature
    return None

def build_auth_cookie(user_id):
    """
    Builds auth cookie that contains signed auth info: (secret + user_id) + '--' + user_id
    It is used by get_logged_in_user_id() to get authenticated user.
    """
    user_id = str(user_id)
    return hashlib.sha1((appconfig.secret + user_id).encode('utf-8')).hexdigest() + '--' + user_id

# Call this method before outputting Content-Type: text/html; charset=utf-8
def get_cookies():
    result = {}
    if 'HTTP_COOKIE' in os.environ:
        cookies = os.environ['HTTP_COOKIE'].split('; ')
        for cookie in cookies:
            cookie = cookie.split('=')
            if (len(cookie) >= 2):
                result[url_decode(cookie[0])] = url_decode(cookie[1])
    return result

# Call this method before outputting Content-Type: text/html; charset=utf-8
def set_cookies(cookies):
    for key in cookies.keys():
        value = cookies[key]
        ek = url_encode(key)
        ev = url_encode(value)
        print("Set-Cookie:" + ek + " = " + ev + "; Path=/; HttpOnly")

def redirect(location):
    """
    Returns redirection HTML for the given location

    Parameters:
    location (string) - location to redirect to.
    """
    redirect_template = file_get_contents(redirect_template_path)
    return build_template(redirect_template, {'LOCATION': location})


def file_get_contents(filename):
    """
    Reads given file content and returns it as a string

    Parameters:
    filename (string) - file name (with path) to read from hard drive
    Returns:
    text (string) - file contents
    """
    with open(filename, 'r') as content_file:
        return content_file.read()

def sanitize_file_name(filename):
    """
    Sanitizes given file name by removing characters 
    other then a-zA-Z0-9 and _ from the given string.

    Parameters:
    filename (string) - file name (withouth path) to sanitize
    Returns:
    text (string) - sanitized file name
    """
    return re.sub(r'\W+', '', filename)

def encode_html_entities(text):
    """
    Encodes HTML entities to be safely inserted into the HTML

    Parameters:
    text (string) - text to work with
    Returns:
    text (string) - text with encoded html entities
    """
    return html.escape(text)

def url_encode(value):
    """
    Encodes URL entities in URL component.

    Parameters:
    value (string) - text to work with
    Returns:
    text (string) - text with encoded html entities
    """
    return urllib.parse.quote(value)

def url_decode(value):
    """
    Decodes URL entities in URL component

    Parameters:
    value (string) - text to work with
    Returns:
    text (string) - text with encoded html entities
    """
    return urllib.parse.unquote(value)

