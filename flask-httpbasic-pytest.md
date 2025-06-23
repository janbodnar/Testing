# Flask & HTTP Basic auth with Pytest

```.env
# Basic Auth credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=password123
USER_USERNAME=user
USER_PASSWORD=userpass
```

The flask application hides endpoints behind HTTP basic auth. 

```python
from flask import Flask, jsonify, g
from flask_httpauth import HTTPBasicAuth
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
auth = HTTPBasicAuth()

# User data with roles
USERS = {
    os.getenv('ADMIN_USERNAME'): {
        'password': os.getenv('ADMIN_PASSWORD'),
        'role': 'admin'
    },
    os.getenv('USER_USERNAME'): {
        'password': os.getenv('USER_PASSWORD'),
        'role': 'user'
    }
}

@auth.verify_password
def verify_password(username, password):
    """Verify the username/password combination"""
    if username in USERS and USERS[username]['password'] == password:
        g.current_user = username
        g.user_role = USERS[username]['role']
        return username
    return None

@auth.error_handler
def auth_error(status):
    """Handle authentication errors"""
    return jsonify({"error": "Authentication required"}), status

@app.route('/')
def public_endpoint():
    """Public endpoint that doesn't require authentication"""
    return jsonify({"message": "Welcome to the public endpoint!"})

@app.route('/private')
@auth.login_required
def private_endpoint():
    """Private endpoint that requires authentication"""
    return jsonify({
        "message": "Welcome to the private endpoint!",
        "user": g.current_user,
        "role": g.user_role
    })

@app.route('/admin')
@auth.login_required
def admin_endpoint():
    """Admin endpoint that requires admin role"""
    if g.user_role != 'admin':
        return jsonify({"error": "Admin access required"}), 403
    return jsonify({
        "message": "Welcome to the admin endpoint!",
        "user": g.current_user,
        "role": g.user_role
    })

if __name__ == '__main__':
    app.run(debug=True)
```

The `requirements.txt` file:

```
Flask==3.1.1
Flask-HTTPAuth==4.8.0
pytest==8.4.1
pytest-flask==1.3.0
python-dotenv==1.0.0
pytest-cov==6.2.1
```


Run http from CMD terminal: 

```
set HTTP_USER=user
set HTTP_PASS=userpass
http --auth-type=basic --auth=%HTTP_USER%:%HTTP_PASS% http://localhost:5000/private
```
