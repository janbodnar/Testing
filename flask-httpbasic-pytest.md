# Flask & HTTP Basic auth with Pytest

**Basic authentication** is a simple method for enforcing access control over HTTP.  
When a client (like a browser or an API tool) makes a request to a server that requires  
authentication, it includes an `Authorization` header that looks like this:

```
Authorization: Basic <credentials>
```

Here, `<credentials>` is a Base64-encoded string of the format `username:password`.

## Key characteristics:

- **Simplicity**: No cookies, sessions, or tokens—just a header with credentials.
- **No encryption**: Base64 is *not* secure—it's just encoding. Anyone intercepting the request can decode it easily.
- **Best used with HTTPS**: To protect credentials from being exposed in transit.
- **Stateless**: Each request must include the credentials again—there’s no session tracking.

It’s defined in [RFC 7617](https://datatracker.ietf.org/doc/html/rfc7617) and was one of  
the earliest authentication schemes used on the web.


## Pytest example

The example demonstrates the usage of HTTP Basic authentication with Pytest  
tests.  

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
