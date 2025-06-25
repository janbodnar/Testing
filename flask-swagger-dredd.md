# Flask & Swagger

Swagger is a set of open-source tools that helps developers **design, build, document, and test RESTful APIs**.  
It’s built around the **OpenAPI Specification** (formerly known as the Swagger Specification), which is a standardized  
way to describe what an API does, what endpoints it offers, what parameters it expects, and what responses it returns. 

Swagger features:

- **Swagger Editor**: A browser-based tool where you can write and preview your API spec in YAML or JSON.
- **Swagger UI**: Generates interactive documentation from your API spec, letting users try out endpoints directly in the browser.
- **Swagger Codegen**: Automatically generates client libraries, server stubs, and API documentation in various programming languages.

In essence, Swagger bridges the gap between API developers and consumers by making APIs easier to understand, test, and integrate.   
It’s especially handy in API-first development, where the contract (API spec) is defined before any code is written. 

## Flask example

The `app.py` file has three endpoints. 

```python
from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

# Sample in-memory user data
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
]

@app.route('/hello', methods=['GET'])
def hello():
    """
    A simple hello world endpoint.
    ---
    responses:
      200:
        description: Returns a greeting
        examples:
          application/json: {"message": "Hello, world!"}
    """
    return jsonify(message="Hello, world!")

@app.route('/users', methods=['GET'])
def get_users():
    """
    Retrieve a list of all users.
    ---
    responses:
      200:
        description: A list of users
        examples:
          application/json: [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"}
          ]
    """
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Retrieve a specific user by ID.
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: The ID of the user to retrieve
    responses:
      200:
        description: User found
        examples:
          application/json: {"id": 1, "name": "Alice", "email": "alice@example.com"}
      404:
        description: User not found
        examples:
          application/json: {"message": "User not found"}
    """
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"message": "User not found"}), 404

@app.route('/users', methods=['POST'])
def add_user():
    """
    Add a new user.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: The name of the user
            email:
              type: string
              description: The email of the user
          required:
            - name
            - email
    responses:
      201:
        description: User created successfully
        examples:
          application/json: {"id": 3, "name": "New User", "email": "newuser@example.com"}
      400:
        description: Invalid input
        examples:
          application/json: {"message": "Name and email are required"}
    """
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"message": "Name and email are required"}), 400
    
    new_id = max(user['id'] for user in users) + 1 if users else 1
    new_user = {
        "id": new_id,
        "name": data['name'],
        "email": data['email']
    }
    users.append(new_user)
    return jsonify(new_user), 201

if __name__ == '__main__':
    app.run(debug=True)
```

From the `/apidocs` endpoint we download the JSON file and transform it into YAML with `yq` tool.  

```
yq -oy api_spec.json > api_spec.yaml
```

We get the spec in YAML. 

```yaml
definitions: {}
info:
  description: powered by Flasgger
  termsOfService: /tos
  title: A swagger API
  version: 0.0.1
paths:
  /hello:
    get:
      responses:
        "200":
          description: Returns a greeting
          examples:
            application/json:
              message: Hello, world!
      summary: A simple hello world endpoint.
  /users:
    get:
      responses:
        "200":
          description: A list of users
          examples:
            application/json:
              - email: alice@example.com
                id: 1
                name: Alice
              - email: bob@example.com
                id: 2
                name: Bob
      summary: Retrieve a list of all users.
    post:
      consumes:
        - application/json
      parameters:
        - in: body
          name: body
          required: true
          schema:
            properties:
              email:
                description: The email of the user
                type: string
                example: "newuser@example.com"
              name:
                description: The name of the user
                type: string
                example: "New User"
            required:
              - name
              - email
            type: object
            example:
              name: "New User"
              email: "newuser@example.com"
      responses:
        "201":
          description: User created successfully
          examples:
            application/json:
              email: newuser@example.com
              id: 3
              name: New User
        "400":
          description: Invalid input
          examples:
            application/json:
              message: Name and email are required
      summary: Add a new user.
  /users/{user_id}:
    get:
      parameters:
        - description: The ID of the user to retrieve
          in: path
          name: user_id
          required: true
          type: integer
          x-example: 1
      responses:
        "200":
          description: User found
          examples:
            application/json:
              email: alice@example.com
              id: 1
              name: Alice
        "404":
          description: User not found
          examples:
            application/json:
              message: User not found
      summary: Retrieve a specific user by ID.
swagger: "2.0"
```

We use the YAML spec with the Dredd tool to automatically create tests for our endpoints. However, some data  
might be missing that Dredd is expecting. Using AI model, we fix this based on error messages we get.  

For instance:

1. **Adding `x-example: 1`** to the `user_id` path parameter - this provided Dredd with a concrete value to use   
   when testing the `/users/{user_id}` endpoint. 
3. **Adding example values** to the POST request body schema - this gave Dredd the actual data  
    to send in the request body.

The combination of the `consumes: application/json` field (which was already present) and the example values   
ensured that Dredd sends properly formatted JSON requests with the correct Content-Type header. 


Finally, we run the tests.  

```
dredd api_spec.yaml http://localhost:5000
```





