# Pytest with Flask



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


