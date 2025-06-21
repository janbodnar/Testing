# Express & Insomnia


Simple Task API in Express 5.

```js
// app.js
const express = require('express');
const app = express();

// Middleware
app.use(express.json());

// In-memory database (array of tasks)
let tasks = [
  { id: 1, title: 'Morning Frog', description: 'Eat that frog', completed: false },
  { id: 2, title: 'Write CV doc', description: 'Write a new CV', completed: true },
  { id: 3, title: 'Dishes', description: 'Do the dishes', completed: false }
];
let nextId = 4;

// Helper function to find task by ID
const findTaskById = (id) => tasks.find(task => task.id === parseInt(id));

// Helper function to validate task data
const validateTask = (task) => {
  if (!task.title || typeof task.title !== 'string' || task.title.trim() === '') {
    return 'Title is required and must be a non-empty string';
  }
  if (task.description && typeof task.description !== 'string') {
    return 'Description must be a string';
  }
  if (task.completed !== undefined && typeof task.completed !== 'boolean') {
    return 'Completed must be a boolean';
  }
  return null;
};

// Routes

// POST /reset - Reset tasks to initial state
app.post('/reset', (req, res) => {
  tasks = [
    { id: 1, title: 'Morning Frog', description: 'Eat that frog', completed: false },
    { id: 2, title: 'Write CV doc', description: 'Write a new CV', completed: true },
    { id: 3, title: 'Dishes', description: 'Do the dishes', completed: false }
  ];
  nextId = 4;
  
  res.json({
    success: true,
    message: 'Tasks reset to initial state'
  });
});

// GET /tasks - Get all tasks
app.get('/tasks', (req, res) => {
  res.json({
    success: true,
    data: tasks,
    count: tasks.length
  });
});

// GET /tasks/:id - Get a specific task
app.get('/tasks/:id', (req, res) => {
  const task = findTaskById(req.params.id);
  
  if (!task) {
    return res.status(404).json({
      success: false,
      message: 'Task not found'
    });
  }
  
  res.json({
    success: true,
    data: task
  });
});

// POST /tasks - Create a new task
app.post('/tasks', (req, res) => {
  const { title, description, completed } = req.body;
  
  const validationError = validateTask(req.body);
  if (validationError) {
    return res.status(400).json({
      success: false,
      message: validationError
    });
  }
  
  const newTask = {
    id: nextId++,
    title: title.trim(),
    description: description ? description.trim() : '',
    completed: completed || false
  };
  
  tasks.push(newTask);
  
  res.status(201).json({
    success: true,
    data: newTask,
    message: 'Task created successfully'
  });
});

// PUT /tasks/:id - Update a task
app.put('/tasks/:id', (req, res) => {
  const task = findTaskById(req.params.id);
  
  if (!task) {
    return res.status(404).json({
      success: false,
      message: 'Task not found'
    });
  }
  
  const validationError = validateTask(req.body);
  if (validationError) {
    return res.status(400).json({
      success: false,
      message: validationError
    });
  }
  
  const { title, description, completed } = req.body;
  
  task.title = title.trim();
  task.description = description ? description.trim() : '';
  task.completed = completed !== undefined ? completed : task.completed;
  
  res.json({
    success: true,
    data: task,
    message: 'Task updated successfully'
  });
});

// DELETE /tasks/:id - Delete a task
app.delete('/tasks/:id', (req, res) => {
  const taskIndex = tasks.findIndex(task => task.id === parseInt(req.params.id));
  
  if (taskIndex === -1) {
    return res.status(404).json({
      success: false,
      message: 'Task not found'
    });
  }
  
  const deletedTask = tasks.splice(taskIndex, 1)[0];
  
  res.json({
    success: true,
    data: deletedTask,
    message: 'Task deleted successfully'
  });
});

// JSON parsing error handler
app.use((err, req, res, next) => {
  if (err instanceof SyntaxError && err.status === 400 && 'body' in err) {
    return res.status(400).json({
      success: false,
      message: 'Invalid JSON format'
    });
  }
  next(err);
});

// General error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    success: false,
    message: 'Something went wrong!'
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    success: false,
    message: 'Route not found'
  });
});

// Start server (only if not in test environment)
const PORT = process.env.PORT || 3000;
if (process.env.NODE_ENV !== 'test') {
  app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
  });
}

module.exports = app;
```

Insomnia tests

```yaml
type: collection.insomnia.rest/5.0
name: first
meta:
  id: wrk_eca6f6cd08a74e5eaf8fc092da03810d
  created: 1750422872872
  modified: 1750422872872
  description: ""
collection:
  - url: localhost:3000/tasks
    name: Get All Initial Tasks
    meta:
      id: req_8e6cbeaa706b4995a75c2b6dd19fbe7a
      created: 1750422903345
      modified: 1750505991561
      isPrivate: false
      description: ""
      sortKey: -1750422903345
    method: GET
    headers:
      - name: User-Agent
        value: insomnia/11.2.0
    scripts:
      afterResponse: >-
        const response = insomnia.response.json();


        console.log('GET /tasks Response:');

        console.log(JSON.stringify(response, null, 2));


        // Test for status code

        insomnia.test('Status code is 200', function () {
            insomnia.response.to.have.status(200);
        });


        // Test for response structure

        insomnia.test('Response has expected structure', function () {
            insomnia.expect(response).to.have.property('success').that.is.a('boolean');
            insomnia.expect(response.success).to.equal(true);
            insomnia.expect(response).to.have.property('data').that.is.an('array');
            insomnia.expect(response).to.have.property('count').that.is.a('number');
        });


        // Test for initial task count

        insomnia.test('There are initially 3 tasks', function () {
            insomnia.expect(response.data).to.have.lengthOf(3);
            insomnia.expect(response.count).to.equal(3);
            insomnia.expect(response.count).to.equal(response.data.length);
        });


        // Test for task object structure

        insomnia.test('Each task has correct properties', function () {
            response.data.forEach((task, index) => {
                insomnia.expect(task).to.have.property('id').that.is.a('number');
                insomnia.expect(task).to.have.property('title').that.is.a('string');
                insomnia.expect(task).to.have.property('description').that.is.a('string');
                insomnia.expect(task).to.have.property('completed').that.is.a('boolean');
            });
        });
    settings:
      renderRequestBody: true
      encodeUrl: true
      followRedirects: global
      cookies:
        send: true
        store: true
      rebuildPath: true
  - url: localhost:3000/tasks/1
    name: Get First Taks
    meta:
      id: req_a481820643154ee291ad72da9bd20619
      created: 1750426408356
      modified: 1750508289896
      isPrivate: false
      description: ""
      sortKey: -1750077582716
    method: GET
    headers:
      - name: User-Agent
        value: insomnia/11.2.0
    scripts:
      afterResponse: |+
        const response = insomnia.response.json();

        console.log("data");
        console.log(JSON.stringify(response, null, 2));
        console.log(response.token)

        insomnia.test("Status code is 200", function () {
            insomnia.response.to.have.status(200);
        });

        insomnia.test("Response has a valid title", function () {
            insomnia.expect(response.data).to.have.property("title");
            insomnia.expect(response.data.title).to.be.a("string");
            insomnia.expect(response.data.title).to.contain("Frog");
        });

    settings:
      renderRequestBody: true
      encodeUrl: true
      followRedirects: global
      cookies:
        send: true
        store: true
      rebuildPath: true
  - url: http://localhost:3000/tasks
    name: Create New Task
    meta:
      id: req_0446228ac612402c89b0adcf1dfe6dcf
      created: 1750427485298
      modified: 1750505979945
      isPrivate: false
      description: ""
      sortKey: -1750077582616
    method: POST
    body:
      mimeType: application/json
      text: |-
        {
        	"title": "{{taskTitle}}",
        	"description": "{{ taskDescription }}",
        	"completed": {{taskCompleted}}
        }
    headers:
      - name: Content-Type
        value: application/json
      - name: User-Agent
        value: insomnia/11.2.0
    scripts:
      afterResponse: >-
        const response = insomnia.response.json();



        // Test for successful task creation

        insomnia.test('Status code is 201', function () {
            insomnia.response.to.have.status(201);
        });


        insomnia.test('Response has success true', function () {
            insomnia.expect(response).to.have.property('success');
            insomnia.expect(response.success).to.equal(true);
        });


        insomnia.test('Response has data with expected structure', function () {
            insomnia.expect(response).to.have.property('data');
            insomnia.expect(response.data).to.have.property('id').that.is.a('number');
            insomnia.expect(response.data).to.have.property('title').that.is.a('string');
            insomnia.expect(response.data).to.have.property('description').that.is.a('string');
            insomnia.expect(response.data).to.have.property('completed').that.is.a('boolean');
        });


        insomnia.test('Response title contains expected text', function () {
            insomnia.expect(response.data).to.have.property('title');
            insomnia.expect(response.data.title).to.be.a('string');
            insomnia.expect(response.data.title).to.include('shopping');
        });


        insomnia.test('Response has success message', function () {
            insomnia.expect(response).to.have.property('message');
            insomnia.expect(response.message).to.equal('Task created successfully');
        });


        // store ID

        console.log(JSON.stringify(response, null, 2));

        insomnia.environment.set('createdTaskId', response.data.id);
    settings:
      renderRequestBody: true
      encodeUrl: true
      followRedirects: global
      cookies:
        send: true
        store: true
      rebuildPath: true
  - url: http://localhost:3000/reset
    name: Reset Tasks
    meta:
      id: req_a62b3903b82e49e6b1d1d1e9ee9e2fa6
      created: 1750428360443
      modified: 1750505994878
      isPrivate: false
      description: ""
      sortKey: -1750428360443
    method: POST
    headers:
      - name: User-Agent
        value: insomnia/11.2.0
    settings:
      renderRequestBody: true
      encodeUrl: true
      followRedirects: global
      cookies:
        send: true
        store: true
      rebuildPath: true
  - url: http://localhost:3000/tasks/{{createdTaskId}}
    name: Get New Task By Id
    meta:
      id: req_608a769461094f638737ce5bbf10e367
      created: 1750496986199
      modified: 1750502203411
      isPrivate: false
      description: ""
      sortKey: -1750077582516
    method: GET
    headers:
      - name: User-Agent
        value: insomnia/11.2.0
    scripts:
      afterResponse: >
        const response = insomnia.response.json();


        // Test for status code,

        insomnia.test('Status code is 200', function () {
            insomnia.response.to.have.status(200);
        });


        // Test for response structure,

        insomnia.test('Response has expected structure', function () {
            insomnia.expect(response).to.have.property('success').that.is.a('boolean');
            insomnia.expect(response.success).to.equal(true);
            insomnia.expect(response).to.have.property('data').that.is.an('object');
        });


        // Test for task data,

        insomnia.test('Retrieved task matches created task', function () {
            insomnia.expect(response.data).to.have.property('id').that.is.a('number');
            insomnia.expect(response.data.id).to.equal(insomnia.environment.get('createdTaskId'));
            insomnia.expect(response.data).to.have.property('title').that.is.a('string');
            insomnia.expect(response.data.title).to.equal(insomnia.environment.get('taskTitle'));
            insomnia.expect(response.data).to.have.property('description').that.is.a('string');
            insomnia.expect(response.data.description).to.equal(insomnia.environment.get('taskDescription'));
            insomnia.expect(response.data).to.have.property('completed').that.is.a('boolean');
            insomnia.expect(response.data.completed).to.equal(false);
        });
    settings:
      renderRequestBody: true
      encodeUrl: true
      followRedirects: global
      cookies:
        send: true
        store: true
      rebuildPath: true
  - url: localhost:3000/tasks/333
    name: Get Non Existing Task
    meta:
      id: req_b20b8352a44f45e2a1a8a80b75e3fec1
      created: 1750502259982
      modified: 1750505983130
      isPrivate: false
      description: ""
      sortKey: -1750077582666
    method: GET
    headers:
      - name: User-Agent
        value: insomnia/11.2.0
    scripts:
      afterResponse: >+
        const response = insomnia.response.json();


        insomnia.test("Status code is 404", function () {
            insomnia.response.to.have.status(404);
        });


        // Test for response structure

        insomnia.test('Response has expected error structure', function () {
            insomnia.expect(response).to.have.property('success').that.is.a('boolean');
            insomnia.expect(response.success).to.equal(false);
            insomnia.expect(response).to.have.property('message').that.is.a('string');
            insomnia.expect(response).not.to.have.property('data');
        });


        insomnia.test('Response has correct error message', function () {
        		insomnia.expect(response.message).to.equal('Task not found');
        });

    settings:
      renderRequestBody: true
      encodeUrl: true
      followRedirects: global
      cookies:
        send: true
        store: true
      rebuildPath: true
  - url: http://localhost:3000/tasks
    name: Create Task Missing Title
    meta:
      id: req_18bbc031cc7d4f9e87f773e6b1f6172c
      created: 1750503267046
      modified: 1750503842089
      isPrivate: false
      description: ""
      sortKey: -1750077582416
    method: POST
    body:
      mimeType: application/json
      text: |-
        {
        	"description": "Go to the store",
        	"completed": false
        }
    headers:
      - name: Content-Type
        value: application/json
      - name: User-Agent
        value: insomnia/11.2.0
    scripts:
      preRequest: ""
      afterResponse: >-
        console.log('Response Content-Type:', insomnia.response.contentType);

        console.log('Response Status:', insomnia.response.status);



        const response = insomnia.response.json();


        // Test for status code

        insomnia.test('Status code is 400', function () {
            insomnia.response.to.have.status(400);
        });


        // Test for response structure

        insomnia.test('Response has expected error structure', function () {
            insomnia.expect(response).to.have.property('success').that.is.a('boolean');
            insomnia.expect(response.success).to.equal(false);
            insomnia.expect(response).to.have.property('message').that.is.a('string');
            insomnia.expect(response).not.to.have.property('data');
        });


        // Test for error message

        insomnia.test('Response has correct error message', function () {
            insomnia.expect(response.message).to.equal('Title is required and must be a non-empty string');
        });
    settings:
      renderRequestBody: true
      encodeUrl: true
      followRedirects: global
      cookies:
        send: true
        store: true
      rebuildPath: true
  - url: http://localhost:3000/tasks
    name: Create Task Empty Title
    meta:
      id: req_f02e069aebeb47cba302ab056021695e
      created: 1750503942482
      modified: 1750504078671
      isPrivate: false
      description: ""
      sortKey: -1749904922251.5
    method: POST
    body:
      mimeType: application/json
      text: |-
        {
        	"title": "",
        	"description": "Go to the store",
        	"completed": false
        }
    headers:
      - name: Content-Type
        value: application/json
      - name: User-Agent
        value: insomnia/11.2.0
    scripts:
      preRequest: ""
      afterResponse: >-
        const response = insomnia.response.json();


        console.log('POST Response (Empty Title):');

        console.log(JSON.stringify(response, null, 2));


        // Test for status code

        insomnia.test('Status code is 400', function () {
            insomnia.response.to.have.status(400);
        });


        // Test for response structure

        insomnia.test('Response has expected error structure', function () {
            insomnia.expect(response).to.have.property('success').that.is.a('boolean');
            insomnia.expect(response.success).to.equal(false);
            insomnia.expect(response).to.have.property('message').that.is.a('string');
            insomnia.expect(response).not.to.have.property('data');
        });


        // Test for error message

        insomnia.test('Response has correct error message', function () {
            insomnia.expect(response.message).to.equal('Title is required and must be a non-empty string');
        });
    settings:
      renderRequestBody: true
      encodeUrl: true
      followRedirects: global
      cookies:
        send: true
        store: true
      rebuildPath: true
  - url: http://localhost:3000/tasks
    name: Create Task Non Bool Completion
    meta:
      id: req_7907eae2c746441e9d48f9242bff3817
      created: 1750504059475
      modified: 1750504176641
      isPrivate: false
      description: ""
      sortKey: -1749818592169.25
    method: POST
    body:
      mimeType: application/json
      text: |-
        {
        	"title": "Visit cinema",
        	"description": "Go to the cinema to watch the Amateur film",
        	"completed": "false"
        }
    headers:
      - name: Content-Type
        value: application/json
      - name: User-Agent
        value: insomnia/11.2.0
    scripts:
      preRequest: ""
      afterResponse: >-
        const response = insomnia.response.json();


        console.log('POST Response (Non-Boolean Completed):');

        console.log(JSON.stringify(response, null, 2));


        // Test for status code

        insomnia.test('Status code is 400', function () {
            insomnia.response.to.have.status(400);
        });


        // Test for response structure

        insomnia.test('Response has expected error structure', function () {
            insomnia.expect(response).to.have.property('success').that.is.a('boolean');
            insomnia.expect(response.success).to.equal(false);
            insomnia.expect(response).to.have.property('message').that.is.a('string');
            insomnia.expect(response).not.to.have.property('data');
        });


        // Test for error message

        insomnia.test('Response has correct error message', function () {
            insomnia.expect(response.message).to.equal('Completed must be a boolean');
        });
    settings:
      renderRequestBody: true
      encodeUrl: true
      followRedirects: global
      cookies:
        send: true
        store: true
      rebuildPath: true
  - url: http://localhost:3000/tasks/1
    name: Update Task Valid Data
    meta:
      id: req_db9508e694b84c9586b77805409e06db
      created: 1750505975427
      modified: 1750508162426
      isPrivate: false
      description: ""
      sortKey: -1749775427128.125
    method: PUT
    body:
      mimeType: application/json
      text: |-
        {
        	"title": "{{updatedTaskTitle}}",
        	"description": "{{updatedTaskDescription}}",
        	"completed": true
        }
    headers:
      - name: Content-Type
        value: application/json
      - name: User-Agent
        value: insomnia/11.2.0
    scripts:
      preRequest: ""
      afterResponse: >-
        const response = insomnia.response.json();


        console.log('PUT Response (Valid Data):');

        console.log(JSON.stringify(response, null, 2));


        // Test for status code

        insomnia.test('Status code is 200', function () {
            insomnia.response.to.have.status(200);
        });


        // Test for response structure

        insomnia.test('Response has expected structure', function () {
            insomnia.expect(response).to.have.property('success').that.is.a('boolean');
            insomnia.expect(response.success).to.equal(true);
            insomnia.expect(response).to.have.property('data').that.is.an('object');
            insomnia.expect(response).to.have.property('message').that.is.a('string');
        });


        // Test for updated task data

        insomnia.test('Task updated correctly', function () {
            insomnia.expect(response.data).to.have.property('id').that.is.a('number');
            insomnia.expect(response.data.id).to.equal(1);
            insomnia.expect(response.data).to.have.property('title').that.is.a('string');
            insomnia.expect(response.data.title).to.equal(insomnia.environment.get('updatedTaskTitle'));
            insomnia.expect(response.data).to.have.property('description').that.is.a('string');
            insomnia.expect(response.data.description).to.equal(insomnia.environment.get('updatedTaskDescription'));
            insomnia.expect(response.data).to.have.property('completed').that.is.a('boolean');
            insomnia.expect(response.data.completed).to.equal(true);
        });


        // Test for success message

        insomnia.test('Response has correct success message', function () {
            insomnia.expect(response.message).to.equal('Task updated successfully');
        });


        // Store task ID for reference

        insomnia.environment.set('updatedTaskId', response.data.id);
    settings:
      renderRequestBody: true
      encodeUrl: true
      followRedirects: global
      cookies:
        send: true
        store: true
      rebuildPath: true
  - url: http://localhost:3000/tasks/{{updatedTaskId}}
    name: Get Updated Task
    meta:
      id: req_c0d4975515534120b0de490268cacf0e
      created: 1750506195220
      modified: 1750508254510
      isPrivate: false
      description: ""
      sortKey: -1749753844607.5625
    method: GET
    body:
      mimeType: application/json
      text: ""
    headers:
      - name: Content-Type
        value: application/json
      - name: User-Agent
        value: insomnia/11.2.0
    scripts:
      preRequest: ""
      afterResponse: >+
        const response = insomnia.response.json();


        // Test for status code

        insomnia.test('Status code is 200', function () {
            insomnia.response.to.have.status(200);
        });



        insomnia.test('Retrieved task matches updated task', function () {
            insomnia.expect(response.data).to.have.property('id').that.is.a('number');
            insomnia.expect(response.data.id).to.equal(insomnia.environment.get('updatedTaskId'));
            insomnia.expect(response.data).to.have.property('title').that.is.a('string');
            insomnia.expect(response.data.title).to.equal(insomnia.environment.get('updatedTaskTitle'));
            insomnia.expect(response.data).to.have.property('description').that.is.a('string');
            insomnia.expect(response.data.description).to.equal(insomnia.environment.get('updatedTaskDescription'));
            insomnia.expect(response.data).to.have.property('completed').that.is.a('boolean');
            insomnia.expect(response.data.completed).to.equal(true);
        });


        // Test for success message

        insomnia.test('Response success attribute is true', function () {
            insomnia.expect(response.success).to.equal(true);
        });

    settings:
      renderRequestBody: true
      encodeUrl: true
      followRedirects: global
      cookies:
        send: true
        store: true
      rebuildPath: true
  - url: http://localhost:3000/tasks/{{updatedTaskId}}
    name: Delete First Task
    meta:
      id: req_64e4a754f5d944c190a205aae6441b24
      created: 1750508546956
      modified: 1750508589566
      isPrivate: false
      description: ""
      sortKey: -1749743053347.2812
    method: DELETE
    body:
      mimeType: application/json
      text: ""
    headers:
      - name: Content-Type
        value: application/json
      - name: User-Agent
        value: insomnia/11.2.0
    scripts:
      preRequest: ""
      afterResponse: >-
        const response = insomnia.response.json();


        // Test for status code

        insomnia.test('Status code is 200', function () {
            insomnia.response.to.have.status(200);
        });


        // Test for response structure

        insomnia.test('Response has expected structure', function () {
            insomnia.expect(response).to.have.property('success').that.is.a('boolean');
            insomnia.expect(response.success).to.equal(true);
            insomnia.expect(response).to.have.property('data').that.is.an('object');
            insomnia.expect(response).to.have.property('message').that.is.a('string');
        });


        // Test for deleted task data

        insomnia.test('Task deleted correctly', function () {
            insomnia.expect(response.data).to.have.property('id').that.is.a('number');
            insomnia.expect(response.data.id).to.equal(1);
            insomnia.expect(response.data).to.have.property('title').that.is.a('string');
            insomnia.expect(response.data).to.have.property('description').that.is.a('string');
            insomnia.expect(response.data).to.have.property('completed').that.is.a('boolean');
        });


        // Test for success message

        insomnia.test('Response has correct success message', function () {
            insomnia.expect(response.message).to.equal('Task deleted successfully');
        });


        // Store task ID for next request

        insomnia.environment.set('deletedTaskId', response.data.id);
    settings:
      renderRequestBody: true
      encodeUrl: true
      followRedirects: global
      cookies:
        send: true
        store: true
      rebuildPath: true
  - url: http://localhost:3000/tasks/{{deletedTaskId}}
    name: Get Deleted Task
    meta:
      id: req_b4d348fa9dca479ea39042776d257c3f
      created: 1750508681175
      modified: 1750508712987
      isPrivate: false
      description: ""
      sortKey: -1749743053247.2812
    method: GET
    body:
      mimeType: application/json
      text: ""
    headers:
      - name: Content-Type
        value: application/json
      - name: User-Agent
        value: insomnia/11.2.0
    scripts:
      preRequest: ""
      afterResponse: >-
        const response = insomnia.response.json();


        // Test for status code

        insomnia.test('Status code is 404', function () {
            insomnia.response.to.have.status(404);
        });


        // Test for response structure

        insomnia.test('Response has expected error structure', function () {
            insomnia.expect(response).to.have.property('success').that.is.a('boolean');
            insomnia.expect(response.success).to.equal(false);
            insomnia.expect(response).to.have.property('message').that.is.a('string');
            insomnia.expect(response).not.to.have.property('data');
        });


        // Test for error message

        insomnia.test('Response has correct error message', function () {
            insomnia.expect(response.message).to.equal('Task not found');
        });
    settings:
      renderRequestBody: true
      encodeUrl: true
      followRedirects: global
      cookies:
        send: true
        store: true
      rebuildPath: true
  - url: http://localhost:3000/tasks/{{deletedTaskId}}
    name: Delete Already Deleted Task
    meta:
      id: req_461768c5ca0744f5aecdcd0a6763439b
      created: 1750508901531
      modified: 1750508937857
      isPrivate: false
      description: ""
      sortKey: -1749743053147.2812
    method: DELETE
    body:
      mimeType: application/json
      text: ""
    headers:
      - name: Content-Type
        value: application/json
      - name: User-Agent
        value: insomnia/11.2.0
    scripts:
      preRequest: ""
      afterResponse: >-
        const response = insomnia.response.json();


        console.log('DELETE Response (Already Deleted):');

        console.log(JSON.stringify(response, null, 2));


        // Test for status code

        insomnia.test('Status code is 404', function () {
            insomnia.response.to.have.status(404);
        });


        // Test for response structure

        insomnia.test('Response has expected error structure', function () {
            insomnia.expect(response).to.have.property('success').that.is.a('boolean');
            insomnia.expect(response.success).to.equal(false);
            insomnia.expect(response).to.have.property('message').that.is.a('string');
            insomnia.expect(response).not.to.have.property('data');
        });


        // Test for error message

        insomnia.test('Response has correct error message', function () {
            insomnia.expect(response.message).to.equal('Task not found');
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
    id: jar_2f37214aa8dfea02996db8823e930a8d24b6b3c6
    created: 1750422872887
    modified: 1750508959118
environments:
  name: Base Environment
  meta:
    id: env_2f37214aa8dfea02996db8823e930a8d24b6b3c6
    created: 1750422872882
    modified: 1750508959124
    isPrivate: false
  data:
    createdTaskId: 4
    taskTitle: Do shopping
    taskDescription: Go to the store to buy groceries
    taskCompleted: "false"
    updatedTaskId: 1
    updatedTaskDescription: Buy groceries and household items
    updatedTaskTitle: Updated shopping
    deletedTaskId: 1
```

