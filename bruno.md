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

### Flask app

```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a secure key in production
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tasks', lazy=True))

# Initialize database
with app.app_context():
    db.create_all()

# Helper function to verify JWT token
def token_required(f):
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        try:
            token = token.split(" ")[1]  # Expecting 'Bearer <token>'
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['user_id']).first()
            if not current_user:
                return jsonify({'error': 'User not found'}), 401
        except:
            return jsonify({'error': 'Invalid token'}), 401
        return f(current_user, *args, **kwargs)
    decorator.__name__ = f.__name__
    return decorator

# Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(username=data['username'], password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({'token': token}), 200

@app.route('/tasks', methods=['POST'])
@token_required
def create_task(current_user):
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    new_task = Task(
        title=data['title'],
        description=data.get('description', ''),
        user_id=current_user.id
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({
        'id': new_task.id,
        'title': new_task.title,
        'description': new_task.description,
        'completed': new_task.completed
    }), 201

@app.route('/tasks', methods=['GET'])
@token_required
def get_tasks(current_user):
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'completed': task.completed
    } for task in tasks]), 200

@app.route('/tasks/<int:task_id>', methods=['GET'])
@token_required
def get_task(current_user, task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'completed': task.completed
    }), 200

@app.route('/tasks/<int:task_id>', methods=['PUT'])
@token_required
def update_task(current_user, task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    db.session.commit()
    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'completed': task.completed
    }), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(current_user, task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)
```

### Bruno scripts

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

### Jest tests

```js
import request from 'supertest';
const app = 'http://127.0.0.1:5000';
let AUTH_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3NDk4MTA1NDN9.dkLrVG3ax_HrW9ADx3D0Wxm9MWjQqNXwUn8JP3R-pNs';
let TASK_ID;

describe('Task API Tests', () => {
  let timestamp = Date.now(); // Get current timestamp
  let password; // Store the timestamped password
  let username; // Store the timestamped username

  beforeAll(async () => {
    // Create timestamped username and password
    username = `testuser_${timestamp}`;
    password = `testpass123_${timestamp}`;

    // Register User with timestamped username and password
    await request(app)
      .post('/register')
      .set('Content-Type', 'application/json')
      .send({ username: username, password: password })
      .expect(201)
      .expect((res) => {
        expect(res.body.message).toEqual('User registered successfully');
      });

    // Login User to get AUTH_TOKEN using the same credentials
    const loginResponse = await request(app)
      .post('/login')
      .set('Content-Type', 'application/json')
      .send({ username: username, password: password })
      .expect(200)
      .expect((res) => {
        expect(res.body.token).toBeDefined();
      });
    AUTH_TOKEN = loginResponse.body.token;
  });

  test('Login User - Invalid Credentials', async () => {
    const response = await request(app)
      .post('/login')
      .set('Content-Type', 'application/json')
      .send({ username: username, password: 'wrongpass' })
      .expect(401);
    expect(response.body.error).toEqual('Invalid credentials');
  });

  test('Register User - Duplicate Username', async () => {
    const response = await request(app)
      .post('/register')
      .set('Content-Type', 'application/json')
      .send({ username: 'testuser', password: 'testpass123' })
      .expect(400);
    expect(response.body.error).toEqual('Username already exists');
  });

  test('Create Task - No Title', async () => {
    const response = await request(app)
      .post('/tasks')
      .set('Content-Type', 'application/json')
      .set('Authorization', `Bearer ${AUTH_TOKEN}`)
      .send({ description: 'This task has no title' })
      .expect(400);
    expect(response.body.error).toEqual('Title is required');
  });

  test('Create Task', async () => {
    const response = await request(app)
      .post('/tasks')
      .set('Content-Type', 'application/json')
      .set('Authorization', `Bearer ${AUTH_TOKEN}`)
      .send({ title: 'Test Task', description: 'This is a test task' })
      .expect(201);
    expect(response.body.title).toEqual('Test Task');
    expect(response.body.description).toEqual('This is a test task');
    expect(response.body.completed).toEqual(false);
    TASK_ID = response.body.id;
  });

  test('Get All Tasks', async () => {
    const response = await request(app)
      .get('/tasks')
      .set('Authorization', `Bearer ${AUTH_TOKEN}`)
      .expect(200);
    expect(Array.isArray(response.body)).toBe(true);
  });

  test('Get Task by ID', async () => {
    const response = await request(app)
      .get('/tasks/1')
      .set('Authorization', `Bearer ${AUTH_TOKEN}`)
      .expect(200);
    expect(response.body.title).toEqual('Test Task');
  });

  test('Get Task by ID - Not Found', async () => {
    const response = await request(app)
      .get('/tasks/999')
      .set('Authorization', `Bearer ${AUTH_TOKEN}`)
      .expect(404);
    expect(response.body.error).toEqual('Task not found');
  });

  test('Update Task', async () => {
    const response = await request(app)
      .put(`/tasks/${TASK_ID}`)
      .set('Content-Type', 'application/json')
      .set('Authorization', `Bearer ${AUTH_TOKEN}`)
      .send({ title: 'Updated Task', description: 'Updated description', completed: true })
      .expect(200);
    expect(response.body.title).toEqual('Updated Task');
    expect(response.body.completed).toEqual(true);
  });

  test('Delete Task', async () => {
    const response = await request(app)
      .delete(`/tasks/${TASK_ID}`)
      .set('Authorization', `Bearer ${AUTH_TOKEN}`)
      .expect(200);
    expect(response.body.message).toEqual('Task deleted');
  });

  test('Delete Task - Not Found', async () => {
    const response = await request(app)
      .delete('/tasks/999')
      .set('Authorization', `Bearer ${AUTH_TOKEN}`)
      .expect(404);
    expect(response.body.error).toEqual('Task not found');
  });
});
```


