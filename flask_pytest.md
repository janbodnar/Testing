# Pytest with Flask



## Simple tests

Below is a very simple Flask application with a home page, along with a corresponding `pytest` test  
file that checks only the status code, title, and a paragraph. This example strips down the complexity  
to focus on these three elements, making it easy to understand and adapt.

---

### Directory Structure

```
simple_app/
├── app.py           # Flask app
├── templates/
│   └── home.html    # Home page template
└── test/
    ├── __init__.py  # Makes test/ a package (can be empty)
    └── test_app.py  # Test file
```

---

### Flask App (`app.py`)

Here’s a minimal Flask app with a single route for the home page:

```python
# simple_app/app.py
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

A simple HTML page with a title and a paragraph:

```html
<!-- simple_app/templates/home.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Welcome to My App</title>
</head>
<body>
    <h1>Home Page</h1>
    <p>This is a simple paragraph on the home page.</p>
</body>
</html>
```

---

### Pytest Test File (`test/test_app.py`)

This test file uses pytest to check:

1. The HTTP status code (200 OK).
2. The page title (`<title>Welcome to My App</title>`).
3. A paragraph (`<p>This is a simple paragraph on the home page.</p>`).

```python
# simple_app/test/test_app.py
import pytest
from app import app as flask_app  # Absolute import from app.py

@pytest.fixture
def client():
    """Set up a test client for the Flask app."""
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_home_page(client):
    """Test the home page for status code, title, and paragraph."""
    response = client.get('/')
    
    # Check status code
    assert response.status_code == 200
    
    # Check title
    assert b"<title>Welcome to My App</title>" in response.data
    
    # Check paragraph
    assert b"<p>This is a simple paragraph on the home page.</p>" in response.data
```

---

### Running the Tests

1. **Navigate to the project root**:
   ```bash
   cd simple_app
   ```

2. **Run pytest**:
   ```bash
   pytest test/test_app.py -v
   ```

---

### Expected Output
If everything is set up correctly, you’ll see:

```
collected 1 item

test/test_app.py::test_home_page PASSED           [100%]

=========== 1 passed in X.XXs ===========
```

---

### Explanation
- **Flask App**: Defines a single route (`/`) that renders `home.html`.
- **HTML Template**: Contains a basic title and paragraph for testing.
- **Test File**:
  - **`client` Fixture**: Sets up a Flask test client in testing mode.
  - **`test_home_page`**: Makes a GET request to `/`, then asserts:
    - `status_code == 200`: The page loads successfully.
    - Title presence: Checks for the exact `<title>` tag in the response bytes.
    - Paragraph presence: Checks for the exact `<p>` tag in the response bytes.
- **Imports**: Uses an absolute import (`from app import app`) since `app.py` is in the root directory,
   and pytest adds `simple_app/` to `sys.path` when run from there.

---

### Notes
- **No `__init__.py` Needed**: Since we’re using an absolute import and there’s only one test file, `test/__init__.py`  
  isn’t required. Pytest will still discover `test_app.py` due to its naming convention.  
- **Simplicity**: This avoids database, forms, or external dependencies, focusing purely on the HTTP response.  
- **Byte Strings**: `response.data` is bytes, so assertions use `b"..."` to match the encoded HTML.  

---

### Running the App (Optional)
To see the page in a browser, run:

```bash
python app.py
```

Visit `http://127.0.0.1:5000/` to confirm the title and paragraph appear as expected.


## Testing JSON

Below is a simple Flask application that serves JSON data on its home page, along with a `pytest`  
test file to verify the status code, content type, and specific JSON data. This example focuses  
on testing a JSON response instead of HTML.

---

### Directory Structure
```
json_app/
├── app.py           # Flask app
└── test/
    ├── __init__.py  # Makes test/ a package (optional but included for consistency)
    └── test_app.py  # Test file
```

Note: No `templates/` directory is needed since we’re returning JSON, not rendering HTML.

---

### Flask App (`app.py`)

A minimal Flask app that returns JSON data:

```python
# json_app/app.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    data = {
        "message": "Hello, World!",
        "status": "success",
        "value": 42
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
```

- **Route `/`**: Returns a JSON object with `message`, `status`, and `value` fields.

---

### Pytest Test File (`test/test_app.py`)

This test file checks:

1. The HTTP status code (200 OK).
2. The `Content-Type` header (`application/json`).
3. Specific values in the JSON response (`message`, `status`, `value`).

```python
# json_app/test/test_app.py
import pytest
import json
from app import app as flask_app  # Absolute import from app.py

@pytest.fixture
def client():
    """Set up a test client for the Flask app."""
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_home_page_json(client):
    """Test the home page for status code, content type, and JSON data."""
    response = client.get('/')
    
    # Check status code
    assert response.status_code == 200
    
    # Check content type
    assert response.content_type == 'application/json'
    
    # Parse JSON and check data
    data = json.loads(response.data)
    assert data["message"] == "Hello, World!"
    assert data["status"] == "success"
    assert data["value"] == 42
```

---

### `__init__.py` in `test/`

An empty file to mark `test/` as a package (optional with absolute imports, 
but included per your preference):

```
json_app/test/__init__.py
```

---

### Running the Tests

1. **Navigate to the project root**:
   ```bash
   cd json_app
   ```

2. **Run pytest**:
   ```bash
   pytest test/test_app.py -v
   ```

---

### Expected Output
If everything is set up correctly, you’ll see:

```
collected 1 item

test/test_app.py::test_home_page_json PASSED      [100%]

=========== 1 passed in X.XXs ===========
```

---

### Explanation

- **Flask App**:
  - Uses `jsonify` to return a JSON response with a dictionary containing `message`, `status`, and `value`.  
  - Automatically sets the `Content-Type` header to `application/json`.  

- **Test File**:
  - **`client` Fixture**: Sets up a Flask test client in testing mode.  
  - **`test_home_page_json`**:
    - `response.status_code == 200`: Verifies the request succeeds.  
    - `response.content_type == 'application/json'`: Confirms the response is JSON.  
    - `json.loads(response.data)`: Parses the JSON bytes into a Python dictionary.  
    - Assertions on `data`: Checks exact values for `message`, `status`, and `value`.  

- **Imports**: Uses absolute `from app import ...` since `app.py` is in the root,  
  and pytest adds `json_app/` to `sys.path` when run from there.

- **`test/__init__.py`**: Included for consistency with your previous setup,  
  though not required here with absolute imports and a single test file.

---

### Running the App (Optional)
To see the JSON in a browser or tool like `curl`, run:

```bash
python app.py
```

Visit `http://127.0.0.1:5000/` or use:

```bash
curl http://127.0.0.1:5000/
```

You’ll see:

```json
{
    "message": "Hello, World!",
    "status": "success",
    "value": 42
}
```






## Testing a form 

```
pip install pytest pytest-flask flask flask-wtf flask-sqlalchemy
```

The `static\style.css` file:

```css
/* Reset some basic elements */
body, html {
    margin: 0;
    padding: 0;
    height: 100%;
    font-family: Arial, sans-serif;
  }
  
  /* Center the form container */
  .form-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh; /* Full viewport height */
    background-color: #f0f0f0;
  }
  
  /* Style the form wrapper */
  .form-wrapper {
    width: 50%; /* Adjust the width as needed */
    max-width: 600px; /* Maximum width */
    padding: 20px;
    background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
  
  /* Style form elements */
  .form-wrapper label {
    font-weight: bold;
    margin-top: 10px;
  }
  
  .form-wrapper input[type="text"],
  .form-wrapper input[type="number"] {
    width: 100%;
    padding: 8px;
    margin: 8px 0;
    box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .form-wrapper .pure-button-primary {
    width: auto; /* Shrink the button width */
    padding: 8px 16px; /* Adjust padding */
    background-color: #007bff;
    color: #ffffff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
  }
  
  .form-wrapper .pure-button-primary:hover {
    background-color: #0056b3;
  }
  
  .errors {
    color: red;
    list-style-type: none;
    padding: 0;
  }
```

The `templates\index.html` file:

```html
<!doctype html>
<html lang="en">
  <head>
    <title>WTForms and SQLite Example</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/pure/2.0.6/pure-min.css" integrity="sha384-ZO8+rtGFVLEv0wBz/U7S4IYlfHpG6OLTR7VcpvxmT2F8i8FQmJOGYgATszVqv5cq" crossorigin="anonymous">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
  </head>
  <body>
    <div class="form-container">
      <div class="form-wrapper">
        <h1>User Form</h1>
        <form class="pure-form pure-form-stacked" method="POST">
          {{ form.hidden_tag() }}
          <fieldset>
            <div>
              <label>{{ form.first_name.label }}</label>
              {{ form.first_name(class_="pure-input-1-2") }}
              {% if form.first_name.errors %}
                <ul class="errors">
                  {% for error in form.first_name.errors %}
                    <li>{{ error }}</li>
                  {% endfor %}
                </ul>
              {% endif %}
            </div>
            <div>
              <label>{{ form.last_name.label }}</label>
              {{ form.last_name(class_="pure-input-1-2") }}
              {% if form.last_name.errors %}
                <ul class="errors">
                  {% for error in form.last_name.errors %}
                    <li>{{ error }}</li>
                  {% endfor %}
                </ul>
              {% endif %}
            </div>
            <div>
              <label>{{ form.occupation.label }}</label>
              {{ form.occupation(class_="pure-input-1-2") }}
              {% if form.occupation.errors %}
                <ul class="errors">
                  {% for error in form.occupation.errors %}
                    <li>{{ error }}</li>
                  {% endfor %}
                </ul>
              {% endif %}
            </div>
            <div>
              <label>{{ form.salary.label }}</label>
              {{ form.salary(class_="pure-input-1-2") }}
              {% if form.salary.errors %}
                <ul class="errors">
                  {% for error in form.salary.errors %}
                    <li>{{ error }}</li>
                  {% endfor %}
                </ul>
              {% endif %}
            </div>
            <div>
              {{ form.submit(class_="pure-button pure-button-primary") }}
            </div>
          </fieldset>
        </form>
      </div>
    </div>
  </body>
</html>
```

The `app.py` file:

```python
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    occupation = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)

# Create the database
with app.app_context():
    db.create_all()

# Define the form class
class UserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    occupation = StringField('Occupation', validators=[DataRequired(), Length(max=100)])
    salary = FloatField('Salary', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            occupation=form.occupation.data,
            salary=form.salary.data
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('success', user_id=user.id))
    return render_template('index.html', form=form)

@app.route('/success/<int:user_id>')
def success(user_id):
    user = User.query.get_or_404(user_id)
    return f'User {user.first_name} {user.last_name} added successfully!'

if __name__ == '__main__':
    app.run(debug=True)
```

The `test\test_app.py` file:

```python
import pytest
from app import app as flask_app, db, User  # Assuming the Flask app is in app.py

# Pytest fixture to set up the Flask app and database
@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_users.db'
    flask_app.config['WTF_CSRF_ENABLED'] = False
    
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def init_database(app):
    """Initialize the database with a sample user."""
    with app.app_context():
        user = User(first_name="John", last_name="Doe", occupation="Engineer", salary=50000.0)
        db.session.add(user)
        db.session.commit()
        yield
        db.session.rollback()

# Test the index route with GET request
def test_index_get(client):
    """Test that the index page loads successfully with a GET request."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"User Form" in response.data
    assert b"First Name" in response.data
    assert b"Last Name" in response.data
    assert b"Occupation" in response.data
    assert b"Salary" in response.data
    assert b"Submit" in response.data

# Test form submission with valid data
def test_index_post_valid(client, app):
    """Test submitting the form with valid data redirects to success."""
    form_data = {
        'first_name': 'Jane',
        'last_name': 'Smith',
        'occupation': 'Developer',
        'salary': 60000.0
    }
    response = client.post('/', data=form_data, follow_redirects=True)
    assert response.status_code == 200
    assert b"User Jane Smith added successfully!" in response.data
    
    with app.app_context():
        user = User.query.filter_by(first_name='Jane').first()
        assert user is not None
        assert user.last_name == 'Smith'
        assert user.occupation == 'Developer'
        assert user.salary == 60000.0

# Test form submission with invalid data (missing required fields)
def test_index_post_invalid(client):
    """Test submitting the form with missing data shows validation errors."""
    form_data = {
        'first_name': '',
        'last_name': 'Smith',
        'occupation': 'Developer',
        'salary': 60000.0
    }
    response = client.post('/', data=form_data)
    assert response.status_code == 200
    assert b"This field is required" in response.data
    assert b"User Form" in response.data

# Test form submission with invalid salary (non-numeric)
def test_index_post_invalid_salary(client):
    """Test submitting the form with a non-numeric salary shows an error."""
    form_data = {
        'first_name': 'Jane',
        'last_name': 'Smith',
        'occupation': 'Developer',
        'salary': 'invalid'  # Non-numeric
    }
    response = client.post('/', data=form_data)
    assert response.status_code == 200
    assert b"This field is required" in response.data  # Updated to match actual WTForms message
    assert b"User Form" in response.data

# Test form field length validation
def test_index_post_length_exceeded(client):
    """Test submitting a field exceeding max length shows an error."""
    long_string = 'a' * 51
    form_data = {
        'first_name': long_string,
        'last_name': 'Smith',
        'occupation': 'Developer',
        'salary': 60000.0
    }
    response = client.post('/', data=form_data)
    assert response.status_code == 200
    assert b"Field cannot be longer than 50 characters" in response.data  # Updated to match WTForms
    assert b"User Form" in response.data

# Test success route with valid user ID
def test_success_valid(client, init_database, app):
    """Test the success page with a valid user ID."""
    with app.app_context():
        user = User.query.first()
        response = client.get(f'/success/{user.id}')
        assert response.status_code == 200
        assert b"User John Doe added successfully!" in response.data

# Test success route with invalid user ID
def test_success_invalid(client):
    """Test the success page with an invalid user ID returns 404."""
    response = client.get('/success/999')
    assert response.status_code == 404

# Test database model
def test_user_model(app):
    """Test creating and querying a User object in the database."""
    with app.app_context():
        user = User(first_name="Alice", last_name="Johnson", occupation="Designer", salary=75000.0)
        db.session.add(user)
        db.session.commit()
        
        queried_user = User.query.filter_by(first_name="Alice").first()
        assert queried_user is not None
        assert queried_user.last_name == "Johnson"
        assert queried_user.occupation == "Designer"
        assert queried_user.salary == 75000.0
```


