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












