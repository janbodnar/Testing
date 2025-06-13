# Bruno

Bruno is an open-source API testing tool designed to be fast, Git-friendly, and  
offline-first. Unlike traditional API clients like Postman, Bruno stores  
collections as plain text files, making them easy to version-control with Git.  
This approach allows developers to collaborate seamlessly without relying on  
cloud-based storage. Bruno also supports scripting, assertions, and automated  
testing, enabling users to validate API responses efficiently.   

Bruno prioritizes privacy and performance, ensuring that API requests and  
responses remain local to the user's machine. It features a modern UI, powerful  
testing capabilities, and support for multiple environments, making it a  
versatile tool for API development. With its lightweight design and focus on  
developer experience, Bruno is an excellent choice for teams looking for a  
secure, efficient, and Git-integrated API client.  

## Simple example


```python
from flask import Flask, make_response, jsonify
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def index():
    return "<p>Home page</p>"


@app.route("/hello/<name>")
def hello(name):
    msg = f'Hello {escape(name)}!'
    return make_response(msg, 200)


@app.route("/current-time")
def current_time():
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"current-time": now}) # Return current time as JSON
```

## Bruno scripts

`environments/simple.bru`

```
vars {
    NAME: Robert
}
```

`home.bru`:

```
meta {
  name: home
  type: http
  seq: 1
}

get {
  url: http://localhost:5000/
}

assert {
  res.status: eq 200
  res.body: contains Home page
}
```

`hello.bru`:

```
meta {
  name: hello
  type: http
  seq: 2
}

get {
  url: http://localhost:5000/hello/{{NAME}}
}

assert {
  res.status: eq 200
  res.body: contains Hello {{NAME}}
  res.headers['content-type']: eq text/html; charset=utf-8
}
```

`current-time.bru`:

```
meta {
  name: current-time
  type: http
  seq: 3
}

get {
  url: http://localhost:5000/current-time
}

assert {
  res.status: eq 200
  res.body['current-time']: matches ^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$
  res.headers['content-type']: eq application/json
}
```


## Authentication example

```
meta {
  name: Create Task - No Title
  type: http
  seq: 6
}

post {
  url: http://127.0.0.1:5000/tasks
  body: json
  auth: none
}

headers {
  Content-Type: application/json
  Authorization: Bearer {{AUTH_TOKEN}}
}

body:json {
  {"description": "This task has no title"}
}

tests {
  const response = res.getBody();
  test("Status code is 400", function () {
      expect(res.getStatus()).to.equal(400);
  });
  test("Title is required", function () {
      expect(response.error).to.equal("Title is required");
  });
}
```

```
meta {
  name: Create Task
  type: http
  seq: 5
}

post {
  url: http://127.0.0.1:5000/tasks
  body: json
  auth: bearer
}

headers {
  Content-Type: application/json
}

auth:bearer {
  token: {{AUTH_TOKEN}}
}

body:json {
  {"title": "Test Task", "description": "This is a test task"}
}

vars:pre-request {
  : 
}

script:pre-request {
  console.log("pre request");
  console.log(bru.getEnvVar('AUTH_TOKEN'));
}

script:post-response {
  console.log("post response");
  console.log(bru.getEnvVar('AUTH_TOKEN'));
  console.log(bru.getVar('word'));
}

tests {
  const response = res.getBody();
  test("Status code is 201", function () {
      expect(res.getStatus()).to.equal(201);
  });
  test("Task created with correct data", function () {
      expect(response.title).to.equal("Test Task");
      expect(response.description).to.equal("This is a test task");
      expect(response.completed).to.equal(false);
  });
  bru.setEnvVar("TASK_ID", response.id);
  
  console.log("tests");
  
  console.log(bru.getEnvVar('AUTH_TOKEN'));
}
```

```
meta {
  name: Delete Task - Not Found
  type: http
  seq: 12
}

delete {
  url: http://127.0.0.1:5000/tasks/999
  body: none
  auth: none
}

headers {
  Authorization: Bearer {{AUTH_TOKEN}}
}

tests {
  const response = res.getBody();
  test("Status code is 404", function () {
      expect(res.getStatus()).to.equal(404);
  });
  test("Task not found", function () {
      expect(response.error).to.equal("Task not found");
  });
}
```

```
meta {
  name: Delete Task
  type: http
  seq: 11
}

delete {
  url: http://127.0.0.1:5000/tasks/{{TASK_ID}}
  body: none
  auth: none
}

headers {
  Authorization: Bearer {{AUTH_TOKEN}}
}

tests {
  const response = res.getBody();
  test("Status code is 200", function () {
      expect(res.getStatus()).to.equal(200);
  });
  test("Task deleted message", function () {
      expect(response.message).to.equal("Task deleted");
  });
}
```

```
meta {
  name: Get All Tasks
  type: http
  seq: 7
}

get {
  url: http://127.0.0.1:5000/tasks
  body: none
  auth: bearer
}

headers {
  Authorization: Bearer {{AUTH_TOKEN}}
}

auth:bearer {
  token: {{AUTH_TOKEN}}
}

tests {
  const response = res.getBody();
  console.log('Token:', response.token);
  test("Status code is 200", function () {
      expect(res.getStatus()).to.equal(200);
  });
  test("Response is an array", function () {
      expect(Array.isArray(response)).to.be.true;
  });
}
```

```
meta {
  name: Get Task by ID - Not Found
  type: http
  seq: 9
}

get {
  url: http://127.0.0.1:5000/tasks/999
  body: none
  auth: none
}

headers {
  Authorization: Bearer {{AUTH_TOKEN}}
}

tests {
  const response = res.getBody();
  test("Status code is 404", function () {
      expect(res.getStatus()).to.equal(404);
  });
  test("Task not found", function () {
      expect(response.error).to.equal("Task not found");
  });
}
```

```
meta {
  name: Get Task by ID
  type: http
  seq: 8
}

get {
  url: http://127.0.0.1:5000/tasks/1
  body: none
  auth: bearer
}

headers {
  Authorization: Bearer {{AUTH_TOKEN}}
}

auth:bearer {
  token: {{AUTH_TOKEN}}
}

tests {
  const response = res.getBody();
  test("Status code is 200", function () {
      expect(res.getStatus()).to.equal(200);
  });
  test("Task has correct title", function () {
      expect(response.title).to.equal("Test Task");
  });
}
```

```
meta {
  name: Login User - Invalid Credentials
  type: http
  seq: 4
}

post {
  url: http://127.0.0.1:5000/login
  body: json
  auth: none
}

headers {
  Content-Type: application/json
}

body:json {
  {"username": "testuser", "password": "wrongpass"}
}

tests {
  const response = res.getBody();
  test("Status code is 401", function () {
      expect(res.getStatus()).to.equal(401);
  });
  test("Invalid credentials", function () {
      expect(response.error).to.equal("Invalid credentials");
  });
}
```

```
meta {
  name: Login User
  type: http
  seq: 3
}

post {
  url: http://127.0.0.1:5000/login
  body: json
  auth: none
}

headers {
  Content-Type: application/json
}

body:json {
  {
    "username": "testuser",
    "password": "testpass123"
  }
}

script:post-response {
  const response = res.getBody();
  bru.setEnvVar("AUTH_TOKEN", response.token);
  console.log("token", response.token);
  console.log(`AUTH_TOKEN: ${bru.getEnvVar("AUTH_TOKEN")}`);
}

tests {
  const response = res.getBody();
  test("Status code is 200", function () {
      expect(res.getStatus()).to.equal(200);
  });
  test("Token exists", function () {
      expect(response.token).to.exist;
  });
  // bru.setEnvVar("AUTH_TOKEN", response.token);
  // console.log('Token:', response.token);
  // console.log('Environment AUTH_TOKEN:', bru.getEnvVar('AUTH_TOKEN'));
}
```

```
meta {
  name: Register User - Duplicate Username
  type: http
  seq: 2
}

post {
  url: http://127.0.0.1:5000/register
  body: json
  auth: none
}

headers {
  Content-Type: application/json
}

body:json {
  {"username": "testuser", "password": "testpass123"}
}

tests {
  const response = res.getBody();
  test("Status code is 400", function () {
      expect(res.getStatus()).to.equal(400);
  });
  test("Username already exists", function () {
      expect(response.error).to.equal("Username already exists");
  });
}
```


```
meta {
  name: Register User
  type: http
  seq: 1
}

post {
  url: http://127.0.0.1:5000/register
  body: json
  auth: none
}

headers {
  Content-Type: application/json
}

body:json {
  {"username": "testuser", "password": "testpass123"}
}

tests {
  const response = res.getBody();
  test("Status code is 201", function () {
      expect(res.getStatus()).to.equal(201);
  });
  test("User registered successfully", function () {
      expect(response.message).to.equal("User registered successfully");
  });
}
```

```
meta {
  name: Update Task
  type: http
  seq: 10
}

put {
  url: http://127.0.0.1:5000/tasks/{{TASK_ID}}
  body: json
  auth: none
}

headers {
  Content-Type: application/json
  Authorization: Bearer {{AUTH_TOKEN}}
}

body:json {
  {"title": "Updated Task", "description": "Updated description", "completed": true}
}

tests {
  const response = res.getBody();
  test("Status code is 200", function () {
      expect(res.getStatus()).to.equal(200);
  });
  test("Task updated correctly", function () {
      expect(response.title).to.equal("Updated Task");
      expect(response.completed).to.equal(true);
  });
}
```

```
meta {
  name: Task API Tests
  seq: 1
}

auth {
  mode: none
}

vars:pre-request {
  AUTH_TOKEN: 
  TASK_ID: 
}

vars {
  word: "falcon"
}
```
