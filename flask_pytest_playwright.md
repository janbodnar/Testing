# Flask & Pytest & Playwright



Below is an example that integrates Playwright with pytest to test the  
Flask application’s theme switcher functionality in a browser environment.  
Playwright allows us to simulate user interactions (like clicking the toggle)  
and verify the resulting CSS changes (e.g., theme switching). I'll keep the  
Flask app and CSS largely the same, adding Playwright-specific tests alongside  
the basic pytest checks.  

---

### Prerequisites

Install required packages:

```bash
pip install flask pytest pytest-playwright playwright
playwright install  # Installs browser binaries (Chromium, Firefox, WebKit)
```

---

### Directory Structure

```
theme_app/
├── app.py              # Flask app
├── static/
│   └── style.css       # CSS for themes and toggle
└── templates/
    └── home.html       # Home page with toggle
└── test/
    ├── __init__.py     # Makes test/ a package
    └── test_app.py     # Test file with Playwright
```

---

### Flask App (`app.py`)
Unchanged from the previous example:

```python
# theme_app/app.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
```

---

### HTML Template (`templates/home.html`)
Unchanged, with the toggle switch and theme-switching logic:

```html
<!-- theme_app/templates/home.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Theme Switcher App</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <h1>Welcome to Theme Switcher</h1>
        <p>Toggle the switch below to change themes.</p>
        
        <!-- Toggle Switch -->
        <label class="switch">
            <input type="checkbox" id="theme-toggle">
            <span class="slider round"></span>
        </label>
        <span class="label-text">Light/Dark Mode</span>
    </div>

    <script>
        const toggle = document.getElementById('theme-toggle');
        const body = document.body;

        // Load saved theme from localStorage
        if (localStorage.getItem('theme') === 'dark') {
            body.classList.add('dark-theme');
            toggle.checked = true;
        }

        // Toggle theme on click
        toggle.addEventListener('change', () => {
            body.classList.toggle('dark-theme');
            const theme = body.classList.contains('dark-theme') ? 'dark' : 'light';
            localStorage.setItem('theme', theme);
        });
    </script>
</body>
</html>
```

---

### CSS (`static/style.css`)
Unchanged, defining the toggle and themes:

```css
/* theme_app/static/style.css */
body {
    font-family: Arial, sans-serif;
    transition: background-color 0.3s, color 0.3s;
    margin: 0;
    padding: 0;
}

/* Light theme (default) */
body {
    background-color: #f0f0f0;
    color: #333;
}

/* Dark theme */
body.dark-theme {
    background-color: #333;
    color: #f0f0f0;
}

.container {
    max-width: 800px;
    margin: 50px auto;
    text-align: center;
}

/* Toggle Switch Styles */
.switch {
    position: relative;
    display: inline-block;
    width: 60px;
    height: 34px;
    vertical-align: middle;
}

.switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    transition: 0.4s;
    border-radius: 34px;
}

.slider:before {
    position: absolute;
    content: "";
    height: 26px;
    width: 26px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    transition: 0.4s;
    border-radius: 50%;
}

input:checked + .slider {
    background-color: #2196F3;
}

input:checked + .slider:before {
    transform: translateX(26px);
}

.label-text {
    margin-left: 10px;
    font-size: 16px;
}
```

---

### Pytest Test File with Playwright (`test/test_app.py`)

This includes both basic Flask client tests and Playwright tests to verify theme
switching:

```python
# theme_app/test/test_app.py
import pytest
from flask import url_for
from app import app as flask_app  # Absolute import

# Flask client fixture for basic tests
@pytest.fixture
def client():
    """Set up a test client for the Flask app."""
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

# Basic test for status code and content presence
def test_home_page_basic(client):
    """Test the home page for status code, title, and toggle presence."""
    response = client.get('/')
    
    assert response.status_code == 200
    assert b"<title>Theme Switcher App</title>" in response.data
    assert b'<input type="checkbox" id="theme-toggle">' in response.data
    assert b"body.classList.toggle('dark-theme')" in response.data

# Playwright fixture to run Flask app in a live server
@pytest.fixture
def live_server(playwright, tmp_path):
    """Run the Flask app in a live server for Playwright tests."""
    from threading import Thread
    from flask import Flask
    import time

    # Use a temporary port to avoid conflicts
    flask_app.config['SERVER_NAME'] = 'localhost:5001'
    
    def run_app():
        flask_app.run(port=5001, use_reloader=False, debug=False)
    
    server_thread = Thread(target=run_app)
    server_thread.daemon = True
    server_thread.start()
    
    # Wait for the server to start
    time.sleep(1)
    yield
    # Server stops when thread ends (daemon)

# Playwright test for theme switching
@pytest.mark.asyncio
async def test_theme_switching(playwright, live_server):
    """Test theme switching functionality with Playwright."""
    browser = await playwright.chromium.launch(headless=True)  # Headless for CI, set False to see browser
    page = await browser.new_page()
    
    # Navigate to the Flask app
    await page.goto('http://localhost:5001/')
    
    # Check initial state (light theme)
    body_bg = await page.eval_on_selector('body', 'el => window.getComputedStyle(el).backgroundColor')
    assert body_bg == 'rgb(240, 240, 240)'  # #f0f0f0 in RGB
    
    # Find and click the toggle
    toggle = page.locator('#theme-toggle')
    await toggle.click()
    
    # Wait for theme transition (CSS transition is 0.3s)
    await page.wait_for_timeout(500)  # Slightly longer than transition
    
    # Check dark theme
    body_bg_dark = await page.eval_on_selector('body', 'el => window.getComputedStyle(el).backgroundColor')
    assert body_bg_dark == 'rgb(51, 51, 51)'  # #333 in RGB
    
    # Toggle back to light
    await toggle.click()
    await page.wait_for_timeout(500)
    
    # Check light theme again
    body_bg_light = await page.eval_on_selector('body', 'el => window.getComputedStyle(el).backgroundColor')
    assert body_bg_light == 'rgb(240, 240, 240)'
    
    await browser.close()
```

---

### Running the Tests

1. **Navigate to the project root**:
   ```bash
   cd theme_app
   ```

2. **Run pytest**:
   ```bash
   pytest test/test_app.py -v
   ```

---

### Expected Output
```
collected 2 items

test/test_app.py::test_home_page_basic PASSED     [ 50%]
test/test_app.py::test_theme_switching PASSED     [100%]

=========== 2 passed in X.XXs ===========
```

---

### Explanation
- **Flask App and HTML/CSS**: Same as before, with a toggle switch and theme styles.

- **Test File**:
  - **`client` Fixture**: Standard Flask test client for static checks.
  - **`test_home_page_basic`**: Verifies status code, title, and toggle presence (server-side).
  - **`live_server` Fixture**: Runs the Flask app on `localhost:5001` in a background thread. Uses a custom port to avoid conflicts with a running dev server.
  - **`test_theme_switching`** (Playwright):
    - Launches a Chromium browser (headless by default).
    - Navigates to the live server.
    - Checks the initial light theme background (`#f0f0f0`).
    - Clicks the toggle and verifies the dark theme (`#333`).
    - Toggles back and confirms the light theme returns.
    - Uses `eval_on_selector` to get computed CSS styles, ensuring the theme switch applies.

- **Playwright Integration**:

  - `@pytest.mark.asyncio`: Required since Playwright’s API is async.
  - `playwright.chromium.launch()`: Starts a browser instance.
  - `page.locator()`: Finds elements by ID (e.g., `#theme-toggle`).
  - `wait_for_timeout()`: Ensures CSS transitions complete before checking styles.

---

### Notes

- **Headless Mode**: Set `headless=False` in `browser.launch()` to see the browser during testing (useful for debugging).
- **Port**: Uses `5001` to avoid clashing with `5000` if the app is running elsewhere. Adjust if needed.
- **RGB Values**: The test checks exact RGB values from the CSS (`#f0f0f0` → `rgb(240, 240, 240)`, `#333` → `rgb(51, 51, 51)`). These must match your `style.css`.
- **Limitations**: Doesn’t test `localStorage` persistence directly (requires more complex setup), but verifies the toggle’s immediate effect.

---

### Running the App (Optional)
```bash
python app.py
```

Visit `http://127.0.0.1:5000/` to manually test the toggle.
