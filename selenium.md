# Selenium

Selenium is an open-source tool used for automating web browsers. It provides a suite of tools and libraries  
that allow developers to interact with web elements, perform browser-based tests, and automate repetitive  
web tasks. Selenium supports multiple programming languages such as Python, Java, and C#, and works with various  
browsers like Chrome, Firefox, and Edge. Its primary components include WebDriver,  
IDE (Integrated Development Environment), and Grid, which facilitate browser automation, recording,  
and parallel test execution.

## Get the driver 

Choose the driver that matches the version of your chrome.  

`https://googlechromelabs.github.io/chrome-for-testing/#stable`

Download the driver and place it into a directory that is located in the system environment `PATH`.


## Headless mode

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")  # Use new Headless mode
driver = webdriver.Chrome(options=options)

try:
    driver.get("https://www.example.com")
    print(driver.title)
finally:
    driver.quit()
```

## Search & screenshot

```python
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

try: 

    opts = Options()
    opts.add_argument("--headless")

    driver = Chrome(options=opts)
    driver.implicitly_wait(5)
    driver.get("https://www.python.org")

    driver.maximize_window()


    search_bar = driver.find_element(By.NAME, "q")
    print(search_bar)
    search_bar.clear()
    search_bar.send_keys("pycharm")
    # search_bar.send_keys(Keys.RETURN)
    search_bar.submit()

    # If we don't sleep, we don't get the correct window
    time.sleep(2)

    print(driver.current_url)
    driver.get_screenshot_as_file('screenshot.png')

finally:
    driver.quit()
```

## Page source

```python
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

try:

    opts = Options()
    opts.add_argument("--headless")


    driver = Chrome(options=opts)

    driver.get('https://webcode.me')
    title = driver.title
    content = driver.page_source

    print(content)

    assert title == 'My html page', 'title check failed'
    print('passed title check')

    assert 'Today is a beautiful day' in content, 'paragraph content check failed'
    print('passed paragraph content check')

finally:

    driver.quit()
```


## Unittest example

```python
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class WebCodeTest(unittest.TestCase):

    def setUp(self):
        opts = Options()
        opts.add_argument("--headless")

        self.driver = webdriver.Chrome(options=opts)

    def test_title(self):

        self.driver.get("https://webcode.me")
        print(self.driver.title)
        self.assertIn("My html page", self.driver.title)

    def test_paragraphs(self):

        self.driver.get("https://webcode.me")

        els = self.driver.find_elements(By.TAG_NAME, "p")

        self.assertIn('Today is a beautiful day', els[0].text)
        self.assertIn('Hello there', els[1].text)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
```

## Pytest example

```python
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    opts = Options()
    opts.add_argument("--headless")
    driver = webdriver.Chrome(options=opts)
    yield driver
    driver.quit()

class TestWebCode:
    def test_title(self, driver):
        driver.get("https://webcode.me")
        print(driver.title)
        assert "My html page" in driver.title

    def test_paragraphs(self, driver):
        driver.get("https://webcode.me")
        els = driver.find_elements(By.TAG_NAME, "p")
        assert 'Today is a beautiful day' in els[0].text
        assert 'Hello there' in els[1].text

if __name__ == "__main__":

    import sys
    sys.exit(pytest.main())
```


## Flask/Selenium example

An example with a button that when clicked redirects to another page.  

---

### Directory Structure

Here’s the complete structure:

```
flask_project/
├── app.py
├── templates/
│   ├── index.html
│   └── newpage.html
└── tests/
    └── test_app.py
```

- `flask_project/`: Root directory.
- `app.py`: Flask application file in the root.
- `templates/`: Folder for HTML templates, relative to `app.py`.
- `tests/`: Subdirectory for test files, containing `test_app.py`.

---

### Flask App Files

#### `app.py`
This remains unchanged from the previous example, defining the Flask app with two routes:  

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/newpage')
def newpage():
    return render_template('newpage.html')

if __name__ == '__main__':
    app.run(debug=True)
```

#### `templates/index.html`
The home page with a button to navigate:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Home Page</title>
</head>
<body>
    <h1>Welcome to the Home Page</h1>
    <button id="navigateButton" onclick="window.location.href='/newpage'">Go to New Page</button>
</body>
</html>
```

#### `templates/newpage.html`
The target page after button click:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>New Page</title>
</head>
<body>
    <h1>This is the New Page</h1>
    <p>You have successfully navigated here!</p>
</body>
</html>
```

---

### Test File

#### `tests/test_app.py`

This is the updated test file, adjusted for the `tests` directory and compatible 
with `python -m unittest discover -s tests`:

```python
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import threading
import time
import sys
import os

# Adjust sys.path to import app from the root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

class FlaskSeleniumTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up headless Chrome
        opts = Options()
        opts.add_argument("--headless")
        cls.driver = webdriver.Chrome(options=opts)
        
        # Start Flask app in a separate thread
        cls.server_thread = threading.Thread(target=app.run, kwargs={'debug': False})
        cls.server_thread.daemon = True  # Stops when main thread exits
        cls.server_thread.start()
        
        # Give the server time to start
        time.sleep(2)

    def setUp(self):
        # Navigate to the home page before each test
        self.driver.get("http://127.0.0.1:5000/")

    def test_button_navigation(self):
        # Find and click the button
        button = self.driver.find_element(By.ID, "navigateButton")
        button.click()
        
        # Wait for navigation to complete
        time.sleep(1)
        
        # Verify the new page
        self.assertEqual(self.driver.current_url, "http://127.0.0.1:5000/newpage")
        self.assertIn("This is the New Page", self.driver.page_source)

    @classmethod
    def tearDownClass(cls):
        # Clean up
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
```

---

### Running the Example

#### Prerequisites
- Install dependencies: `pip install flask selenium`.
- Ensure ChromeDriver is installed and in your PATH (or specify its path in `webdriver.Chrome()`).

#### Steps
1. **Set Up the Directory**:
   - Create `flask_project/` with the structure above.
   - Place `app.py` in the root.
   - Create `templates/` with `index.html` and `newpage.html`.
   - Create `tests/` with `test_app.py`.

2. **Run the Tests**:
   - From the `flask_project/` directory:
     ```bash
     python -m unittest discover -s tests
     ```
   - Output should look like:
     ```
     ....
     ----------------------------------------------------------------------
     Ran 1 test in 3.123s

     OK
     ```

3. **Run the App Separately (Optional)**:
   - To test manually: `python app.py`, then visit `http://127.0.0.1:5000/`.




# Flask Application with Pagination and Selenium Tests

This tutorial demonstrates how to build a Flask application with pagination using SQLite,  
populate it with 100 rows of sample data, and test the pagination functionality with Selenium.  
The application follows Flask's recommended structure using the application factory pattern.

---

### Project Structure

```
flask_pagination/
├── instance/
│   └── example.db  (SQLite database, created at runtime)
├── flask_pagination/
│   ├── __init__.py  (Application factory)
│   ├── db.py        (Database initialization and utilities)
│   ├── routes.py    (Route definitions)
│   └── templates/
│       └── index.html  (HTML template)
├── tests/
│   └── test_app.py  (Selenium tests)
├── run.py           (Entry point to run the app)
└── requirements.txt
```

---

### Step 1: Set Up the Flask Application

#### `run.py` (Entry Point)
This file runs the Flask application using the application factory.

```python
# run.py
from flask_pagination import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
```

#### `flask_pagination/__init__.py` (Application Factory)

This defines the Flask app factory, configuring the instance folder and registering blueprints and database commands.

```python
# flask_pagination/__init__.py
from flask import Flask
import click
import os

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Load configuration
    if test_config is None:
        app.config.from_mapping(
            DATABASE=os.path.join(app.instance_path, 'example.db'),
        )
    else:
        app.config.from_mapping(test_config)

    # Register database commands
    from . import db
    db.init_app(app)

    # Register routes
    from . import routes
    app.register_blueprint(routes.bp)

    return app
```

#### `flask_pagination/db.py` (Database Handling)

This module manages the SQLite database connection, initialization, and population.

```python
# flask_pagination/db.py
import sqlite3
import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.execute('DROP TABLE IF EXISTS items')
    db.execute('CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT)')
    db.commit()

def populate_db():
    db = get_db()
    for i in range(1, 101):
        db.execute('INSERT OR IGNORE INTO items (id, name) VALUES (?, ?)', (i, f'Item {i}'))
    db.commit()

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(populate_db_command)

@click.command('init-db')
def init_db_command():
    """Initialize the database."""
    init_db()
    click.echo('Initialized the database.')

@click.command('populate-db')
def populate_db_command():
    """Populate the database with 100 sample items."""
    populate_db()
    click.echo('Database populated with 100 items.')
```

#### `flask_pagination/routes.py` (Routes)

This module defines the pagination logic and route using a Blueprint.

```python
# flask_pagination/routes.py
from flask import Blueprint, render_template, request
from .db import get_db
import math

bp = Blueprint('main', __name__)

def get_items(page, per_page=10):
    offset = (page - 1) * per_page
    db = get_db()
    items = db.execute('SELECT * FROM items LIMIT ? OFFSET ?', (per_page, offset)).fetchall()
    total_items = db.execute('SELECT COUNT(*) FROM items').fetchone()[0]
    return items, total_items

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    items, total_items = get_items(page, per_page)
    total_pages = math.ceil(total_items / per_page)
    
    return render_template('index.html', 
                         items=items,
                         page=page,
                         total_pages=total_pages,
                         per_page=per_page)
```

#### `flask_pagination/templates/index.html` (Template)
This HTML template displays the paginated table.

```html
<!-- flask_pagination/templates/index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Pagination Example</title>
    <style>
        .pagination {
            margin: 20px 0;
        }
        .pagination a {
            padding: 8px 16px;
            text-decoration: none;
            color: black;
        }
        .pagination a.active {
            background-color: #4CAF50;
            color: white;
        }
    </style>
</head>
<body>
    <h1>Items List</h1>
    <table>
        <tr>
            <th>ID</th>
            <th>Name</th>
        </tr>
        {% for item in items %}
        <tr>
            <td>{{ item['id'] }}</td>
            <td>{{ item['name'] }}</td>
        </tr>
        {% endfor %}
    </table>

    <div class="pagination">
        {% if page > 1 %}
            <a href="?page={{ page - 1 }}">« Previous</a>
        {% endif %}

        {% for p in range(1, total_pages + 1) %}
            <a href="?page={{ p }}" class="{% if p == page %}active{% endif %}">{{ p }}</a>
        {% endfor %}

        {% if page < total_pages %}
            <a href="?page={{ page + 1 }}">Next »</a>
        {% endif %}
    </div>
</body>
</html>
```

---

### Step 2: Selenium Unit Tests

#### `tests/test_app.py`

This file contains Selenium tests to verify pagination functionality.

```python
# tests/test_app.py
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from flask_pagination import create_app

class TestPagination(unittest.TestCase):
    def setUp(self):
        # Set up Flask app with test configuration including DATABASE
        self.app = create_app({
            'TESTING': True,
            'DATABASE': os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'instance', 'test_example.db')
        })
        self.client = self.app.test_client()
        
        # Initialize and populate database within app context
        with self.app.app_context():
            from flask_pagination.db import init_db, populate_db
            init_db()
            populate_db()
        
        # Start Flask server in a separate thread
        import threading
        self.server_thread = threading.Thread(target=self.app.run, kwargs={'port': 5000})
        self.server_thread.daemon = True
        self.server_thread.start()
        time.sleep(1)  # Give server time to start
        
        # Set up Selenium
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get('http://localhost:5000')
        time.sleep(1)  # Wait for page to load

    def tearDown(self):
        self.driver.quit()
        # Clean up test database
        with self.app.app_context():
            db_path = self.app.config['DATABASE']
            if os.path.exists(db_path):
                os.remove(db_path)

    def test_initial_page_load(self):
        rows = self.driver.find_elements(By.XPATH, '//table//tr[td]')
        self.assertEqual(len(rows), 10)
        first_item = self.driver.find_element(By.XPATH, '//table//tr[td][1]/td[2]').text
        last_item = self.driver.find_element(By.XPATH, '//table//tr[td][10]/td[2]').text
        self.assertEqual(first_item, 'Item 1')
        self.assertEqual(last_item, 'Item 10')

    def test_pagination_next(self):
        next_button = self.driver.find_element(By.LINK_TEXT, 'Next »')
        next_button.click()
        time.sleep(1)
        rows = self.driver.find_elements(By.XPATH, '//table//tr[td]')
        self.assertEqual(len(rows), 10)
        first_item = self.driver.find_element(By.XPATH, '//table//tr[td][1]/td[2]').text
        last_item = self.driver.find_element(By.XPATH, '//table//tr[td][10]/td[2]').text
        self.assertEqual(first_item, 'Item 11')
        self.assertEqual(last_item, 'Item 20')

    def test_pagination_specific_page(self):
        page_5 = self.driver.find_element(By.LINK_TEXT, '5')
        page_5.click()
        time.sleep(1)
        rows = self.driver.find_elements(By.XPATH, '//table//tr[td]')
        self.assertEqual(len(rows), 10)
        first_item = self.driver.find_element(By.XPATH, '//table//tr[td][1]/td[2]').text
        last_item = self.driver.find_element(By.XPATH, '//table//tr[td][10]/td[2]').text
        self.assertEqual(first_item, 'Item 41')
        self.assertEqual(last_item, 'Item 50')

    def test_last_page(self):
        page_10 = self.driver.find_element(By.LINK_TEXT, '10')
        page_10.click()
        time.sleep(1)
        rows = self.driver.find_elements(By.XPATH, '//table//tr[td]')
        self.assertEqual(len(rows), 10)
        first_item = self.driver.find_element(By.XPATH, '//table//tr[td][1]/td[2]').text
        last_item = self.driver.find_element(By.XPATH, '//table//tr[td][10]/td[2]').text
        self.assertEqual(first_item, 'Item 91')
        self.assertEqual(last_item, 'Item 100')

if __name__ == '__main__':
    unittest.main()
```

---

### Step 3: Requirements

Create `requirements.txt`:

```
# requirements.txt
flask
sqlite3
selenium
webdriver-manager
click
```

Install dependencies:
```bash
pip install -r requirements.txt
```

---

### How It Works

1. **Flask Application:**
   - Uses the application factory pattern (`create_app`) for scalability.
   - Stores the SQLite database in the `instance/` folder.
   - Implements pagination with 10 items per page from a 100-row dataset.
   - Provides CLI commands (`init-db` and `populate-db`) to manage the database.

2. **Database:**
   - `init_db`: Creates a table `items` with `id` and `name` columns.
   - `populate_db`: Inserts 100 rows (`Item 1` to `Item 100`).

3. **Selenium Tests:**
   - `setUp`: Creates a test app with a temporary database, populates it, and starts the server.
   - Tests verify pagination (10 rows per page) across the initial page, next page, page 5, and the last page (10).
   - `tearDown`: Cleans up the test database.

---

### Running the Application

1. **Set the `FLASK_APP` Environment Variable:**
   - **Windows (Command Prompt):**
     ```bash
     set FLASK_APP=flask_pagination
     ```
   - **Unix/Linux/macOS:**
     ```bash
     export FLASK_APP=flask_pagination
     ```
   - **Windows (PowerShell):**
     ```powershell
     $env:FLASK_APP = "flask_pagination"
     ```

2. **Initialize the Database:**
   ```bash
   flask init-db
   ```
   Output: `Initialized the database.`

3. **Populate the Database:**
   ```bash
   flask populate-db
   ```
   Output: `Database populated with 100 items.`

4. **Run the Application:**
   ```bash
   python run.py
   ```
   - Visit `http://localhost:5000` to see the paginated table with 10 items per page.

5. **Run the Tests:**
   ```bash
   python -m tests.test_app
   ```
   - Expected output:
     ```
     ....
     ----------------------------------------------------------------------
     Ran 4 tests in X.XXXs
     OK
     ```
   - The tests create a temporary database (`instance/test_example.db`), run the checks, and clean up afterward.

---

### Notes
- The application uses Flask’s recommended structure with blueprints and an instance folder.
- The database path is configurable via `app.config['DATABASE']`, set to `instance/example.db` by default and `instance/test_example.db` for tests.
- Selenium tests use XPath (`//table//tr[td]`) to correctly count only data rows, excluding the header.
- The `FLASK_APP` variable must be set for CLI commands to work with the factory pattern.








