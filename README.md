# Sports Web site and Administration

## Class information
CST363: Database Systems - Project 1.1  at CSUMB: Web app using CGI scripts, MySQL, HTML, CSS

## Starting the web server
Make sure you use Python of version 3.
```shell
cd [DIRECTORY_OF_WEB_PROJECT]
python httpserver.py
```

After running this command you will see `server started 8000` in your command line/terminal which means that application is running and processing HTTP traffic on port **8000**.
You can then open a browser and load main page of the application with the following link: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Dynamic HTML rendering
Application uses Python basic HTTP server and its ability to execute Python scripts stored in **cgi-bin** directory. 
In order to be able to render HTML pages dynamically, application uses Python scripts **index.py** (user visible application part) and
**admin.py** (administration application part) to dynamically render HTML header, HTML body and HTML footer of the application.

Since HTML header and footer are the same for each application page, it makes sense to move them into their own files: **_header.html** and **_footer.html**.

Scripts **index.py** and **admin.py** act as main point in [Front Controller Pattern](https://en.wikipedia.org/wiki/Front_controller) and process all HTTP requests to the web application.

HTTP parameter **action** sets web application page name and this page rendered to browser.

When the user opens web application with default HTTP URL [http://127.0.0.1:8000](http://127.0.0.1:8000), the Python's web server loads static HTML file **index.html** which contains a redirect to web application's Front Controller in **index.py**.

Below you may find the list of links that web application processes.

## List of URLs in the web application

### Regular links (note action parameter is in bold):

* [http://127.0.0.1:8000/cgi-bin/index.py](http://127.0.0.1:8000/cgi-bin/index.py) - Home page
* [http://127.0.0.1:8000/cgi-bin/index.py?**action=home**](http://127.0.0.1:8000/cgi-bin/index.py?action=home) - Home page
* [http://127.0.0.1:8000/cgi-bin/index.py?**action=about**](http://127.0.0.1:8000/cgi-bin/index.py?action=about) - About page

### Admin links (note action parameter is in bold):

* [http://127.0.0.1:8000/cgi-bin/admin.py](http://127.0.0.1:8000/cgi-bin/admin.py) - Login page
* [http://127.0.0.1:8000/cgi-bin/admin.py?**action=login**](http://127.0.0.1:8000/cgi-bin/admin.py?action=login) - Login page



### TODO:
* add dynamic variables to web engine
* add actions for different web pages
* add HTML redirect helper function
* add SQL functions and database configuration
