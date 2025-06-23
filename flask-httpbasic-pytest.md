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

The `requirements.txt` file:


```python
Flask==3.1.1
Flask-HTTPAuth==4.8.0
pytest==8.4.1
pytest-flask==1.3.0
python-dotenv==1.0.0
pytest-cov==6.2.1
requests==2.32.3
```

The credentials are in the `.env` file:  

```.env
# Basic Auth credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=password123
USER_USERNAME=user
USER_PASSWORD=userpass
```

The flask application hides endpoints behind HTTP basic auth. 
The following is `app.py` file: 

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


## Pytest

The following are Pytest test in `tests\test_app.py`: 

```python
import pytest
import base64
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, auth

# Test credentials from environment variables
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
USER_USERNAME = os.getenv('USER_USERNAME')
USER_PASSWORD = os.getenv('USER_PASSWORD')

# Create test client
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_public_endpoint(client):
    """Test that public endpoint is accessible without authentication"""
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"message": "Welcome to the public endpoint!"}

def test_private_endpoint_unauthorized(client):
    """Test that private endpoint requires authentication"""
    response = client.get('/private')
    assert response.status_code == 401
    assert response.json == {"error": "Authentication required"}

def test_private_endpoint_authorized(client):
    """Test that private endpoint works with valid credentials"""
    # Create basic auth header
    auth_header = {
        'Authorization': 'Basic ' + base64.b64encode(
            f"{USER_USERNAME}:{USER_PASSWORD}".encode()
        ).decode()
    }
    response = client.get('/private', headers=auth_header)
    assert response.status_code == 200
    data = response.json
    assert data["message"] == "Welcome to the private endpoint!"
    assert data["user"] == USER_USERNAME
    assert data["role"] == "user"

def test_admin_endpoint_unauthorized(client):
    """Test that admin endpoint requires admin credentials"""
    # Test with regular user credentials
    auth_header = {
        'Authorization': 'Basic ' + base64.b64encode(
            f"{USER_USERNAME}:{USER_PASSWORD}".encode()
        ).decode()
    }
    response = client.get('/admin', headers=auth_header)
    assert response.status_code == 403
    assert response.json == {"error": "Admin access required"}

def test_admin_endpoint_authorized(client):
    """Test that admin endpoint works with admin credentials"""
    auth_header = {
        'Authorization': 'Basic ' + base64.b64encode(
            f"{ADMIN_USERNAME}:{ADMIN_PASSWORD}".encode()
        ).decode()
    }
    response = client.get('/admin', headers=auth_header)
    assert response.status_code == 200
    data = response.json
    assert data["message"] == "Welcome to the admin endpoint!"
    assert data["user"] == ADMIN_USERNAME
    assert data["role"] == "admin"
```

To run tests, we launch `pytest tests` from the project directory.  

```
pytest tests
================================================== test session starts ==================================================
platform win32 -- Python 3.12.7, pytest-8.4.1, pluggy-1.5.0
rootdir: C:\Users\Jano\Documents\prog\testing\basicauth
plugins: anyio-4.8.0, Faker-25.2.0, asyncio-0.25.3, base-url-2.1.0, cov-6.2.1, flask-1.3.0, playwright-0.7.0, socket-0.7.0, syrupy-4.8.1, time-machine-2.16.0
asyncio: mode=Mode.STRICT, asyncio_default_fixture_loop_scope=None
collected 5 items

tests\test_app.py .....                                                                                            [100%]

=================================================== 5 passed in 0.36s ===================================================
```

## Using requests

The following is additional `client.py` script that uses requests to connect to  
the endpoints.  

```python
import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Server configuration
BASE_URL = 'http://localhost:5000'

# Get credentials from environment variables
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
USER_USERNAME = os.getenv('USER_USERNAME')
USER_PASSWORD = os.getenv('USER_PASSWORD')

def test_public_endpoint():
    """Test the public endpoint that doesn't require authentication"""
    print("\nTesting public endpoint...")
    url = f"{BASE_URL}/"
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_private_endpoint(username, password):
    """Test the private endpoint with the given credentials"""
    print(f"\nTesting private endpoint with user: {username}")
    url = f"{BASE_URL}/private"
    try:
        response = requests.get(
            url,
            auth=HTTPBasicAuth(username, password)
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_admin_endpoint(username, password):
    """Test the admin endpoint with the given credentials"""
    print(f"\nTesting admin endpoint with user: {username}")
    url = f"{BASE_URL}/admin"
    try:
        response = requests.get(
            url,
            auth=HTTPBasicAuth(username, password)
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    # First, make sure the server is running at http://localhost:5000
    print("Make sure the Flask server is running at http://localhost:5000\n")
    
    # Test public endpoint (no auth required)
    test_public_endpoint()
    
    # Test private endpoint with regular user
    test_private_endpoint(USER_USERNAME, USER_PASSWORD)
    
    # Test admin endpoint with regular user (should fail)
    test_admin_endpoint(USER_USERNAME, USER_PASSWORD)
    
    # Test admin endpoint with admin user
    test_admin_endpoint(ADMIN_USERNAME, ADMIN_PASSWORD)
    
    # Test private endpoint with invalid credentials
    print("\nTesting private endpoint with invalid credentials...")
    test_private_endpoint("invalid_user", "wrong_password")
    
    print("\nAll tests completed!")
```


## Httpie command

Run http from CMD terminal: 

```
set HTTP_USER=user
set HTTP_PASS=userpass
http --auth-type=basic --auth=%HTTP_USER%:%HTTP_PASS% http://localhost:5000/private
```

## Dev tools

Use `fetch` and `btoa` to connect in Dev tools.


```js
const username = "user";
const password = "userpass";
const credentials = btoa(`${username}:${password}`);

fetch("http://localhost:5000/private", {
  method: "GET",
  headers: {
    "Authorization": `Basic ${credentials}`
  }
})
.then(response => response.text())
.then(data => console.log("Response:", data))
.catch(error => console.error("Error:", error));
```




## Insomnia test file

```yaml
type: collection.insomnia.rest/5.0
name: My first collection
meta:
  id: wrk_5bcf42e89f7343c383301091a56f7914
  created: 1750676738227
  modified: 1750676738227
  description: ""
collection:
  - url: http://localhost:5000/
    name: Public Home page
    meta:
      id: req_9b8973c2208c442c8a961f6a3a1941af
      created: 1750676738348
      modified: 1750677194897
      isPrivate: false
      description: ""
      sortKey: -1750676738348
    method: GET
    headers:
      - name: User-Agent
        value: insomnia/11.2.0
    authentication:
      type: none
    scripts:
      afterResponse: >+
        const response = insomnia.response.json();



        // Test for status code

        insomnia.test("Status code is 200", function () {
            insomnia.response.to.have.status(200);
        });


        // test for public message

        insomnia.test('Contains correct message text', function () {
            insomnia.expect(response).to.have.property('message').that.is.a('string');
        	  insomnia.expect(response.message).to.equal('Welcome to the public endpoint!');
        });

    settings:
      renderRequestBody: true
      encodeUrl: true
      followRedirects: global
      cookies:
        send: true
        store: true
      rebuildPath: true
  - url: http://localhost:5000/private
    name: Get Private Endpoint as User
    meta:
      id: req_08623369363f4d31ab6e140c3917817e
      created: 1750677224573
      modified: 1750678168302
      isPrivate: false
      description: ""
      sortKey: -1750552549395.5
    method: GET
    headers:
      - name: User-Agent
        value: insomnia/11.2.0
    authentication:
      type: basic
      useISO88591: false
      disabled: false
      username: "{{USER_NAME}}"
      password: "{{USER_PASS}}"
    scripts:
      afterResponse: >
        const response = insomnia.response.json();



        // Test for status code

        insomnia.test("Status code is 200", function () {
            insomnia.response.to.have.status(200);
        });


        // test for private message

        insomnia.test('Contains correct message text', function () {
            insomnia.expect(response).to.have.property('message').that.is.a('string');
        	  insomnia.expect(response.message).to.equal('Welcome to the private endpoint!');
        });



        insomnia.test('Contains correct role', function () {
            insomnia.expect(response).to.have.property('role').that.is.a('string');
            insomnia.expect(response.role).to.equal('user');
        });


        insomnia.test('Contains correct user', function () {
            insomnia.expect(response).to.have.property('user').that.is.a('string');
            insomnia.expect(response.user).to.equal('user');
        });
    settings:
      renderRequestBody: true
      encodeUrl: true
      followRedirects: global
      cookies:
        send: true
        store: true
      rebuildPath: true
  - url: http://localhost:5000/admin
    name: Get Admin Endpoint
    meta:
      id: req_d042bcdeaf8b45ebb284b8e55f6ae685
      created: 1750677387557
      modified: 1750678135738
      isPrivate: false
      description: ""
      sortKey: -1750490454919.25
    method: GET
    headers:
      - name: User-Agent
        value: insomnia/11.2.0
    authentication:
      type: basic
      useISO88591: false
      disabled: false
      username: "{{ADMIN_NAME}}"
      password: "{{ADMIN_PASS}}"
    scripts:
      afterResponse: >
        const response = insomnia.response.json();



        // Test for status code

        insomnia.test("Status code is 200", function () {
            insomnia.response.to.have.status(200);
        });


        // test for admin message

        insomnia.test('Contains correct message text', function () {
            insomnia.expect(response).to.have.property('message').that.is.a('string');
        	  insomnia.expect(response.message).to.equal('Welcome to the admin endpoint!');
        });



        insomnia.test('Contains correct role', function () {
            insomnia.expect(response).to.have.property('role').that.is.a('string');
            insomnia.expect(response.role).to.equal('admin');
        });


        insomnia.test('Contains correct user', function () {
            insomnia.expect(response).to.have.property('user').that.is.a('string');
            insomnia.expect(response.user).to.equal('admin');
        });
    settings:
      renderRequestBody: true
      encodeUrl: true
      followRedirects: global
      cookies:
        send: true
        store: true
      rebuildPath: true
cookieJar:
  name: Default Jar
  meta:
    id: jar_957b686d719403627276c64c4040370036c80dbe
    created: 1750676738233
    modified: 1750678180170
environments:
  name: Base Environment
  meta:
    id: env_957b686d719403627276c64c4040370036c80dbe
    created: 1750676738230
    modified: 1750678180175
    isPrivate: false
```