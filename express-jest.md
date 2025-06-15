# Express & Jest


Express CRUD app. 

The `package.json` file:

```json
{
  "name": "express-crud-app",
  "version": "1.0.0",
  "description": "A simple CRUD application built with Express.js 5.1",
  "main": "app.js",
  "scripts": {
    "start": "node app.js",
    "dev": "nodemon app.js",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  },
  "keywords": [
    "express",
    "crud",
    "nodejs",
    "api",
    "rest"
  ],
  "author": "",
  "license": "MIT",
  "dependencies": {
    "express": "^5.1.0"
  },
  "devDependencies": {
    "jest": "^29.7.0",
    "supertest": "^6.3.3",
    "nodemon": "^3.0.2"
  },
  "jest": {
    "testEnvironment": "node",
    "collectCoverageFrom": [
      "*.js",
      "!node_modules/**",
      "!coverage/**"
    ],
    "coverageReporters": [
      "text",
      "lcov",
      "html"
    ]
  }
}
```

The `app.js` file:

```js
// app.js
const express = require('express');
const app = express();

// Middleware
app.use(express.json());

// In-memory database (array of tasks)
let tasks = [
  { id: 1, title: 'Sample Task', description: 'This is a sample task', completed: false },
  { id: 2, title: 'Another Task', description: 'This is another task', completed: true }
];
let nextId = 3;

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

the `app.test.js` file:

```js
// app.test.js
const request = require('supertest');
const app = require('./app');

describe('Task CRUD API', () => {
  let createdTaskId;

  describe('GET /tasks', () => {
    it('should return all tasks', async () => {
      const response = await request(app)
        .get('/tasks')
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(Array.isArray(response.body.data)).toBe(true);
      expect(response.body.count).toBe(response.body.data.length);
      expect(response.body.data.length).toBeGreaterThanOrEqual(0);
    });

    it('should return tasks with correct structure', async () => {
      const response = await request(app)
        .get('/tasks')
        .expect(200);

      if (response.body.data.length > 0) {
        const task = response.body.data[0];
        expect(task).toHaveProperty('id');
        expect(task).toHaveProperty('title');
        expect(task).toHaveProperty('description');
        expect(task).toHaveProperty('completed');
        expect(typeof task.id).toBe('number');
        expect(typeof task.title).toBe('string');
        expect(typeof task.completed).toBe('boolean');
      }
    });
  });

  describe('POST /tasks', () => {
    it('should create a new task with valid data', async () => {
      const newTask = {
        title: 'Test Task',
        description: 'This is a test task',
        completed: false
      };

      const response = await request(app)
        .post('/tasks')
        .send(newTask)
        .expect(201);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toHaveProperty('id');
      expect(response.body.data.title).toBe(newTask.title);
      expect(response.body.data.description).toBe(newTask.description);
      expect(response.body.data.completed).toBe(newTask.completed);
      expect(response.body.message).toBe('Task created successfully');

      createdTaskId = response.body.data.id;
    });

    it('should create a task with minimal data (title only)', async () => {
      const newTask = {
        title: 'Minimal Task'
      };

      const response = await request(app)
        .post('/tasks')
        .send(newTask)
        .expect(201);

      expect(response.body.success).toBe(true);
      expect(response.body.data.title).toBe(newTask.title);
      expect(response.body.data.description).toBe('');
      expect(response.body.data.completed).toBe(false);
    });

    it('should return 400 for missing title', async () => {
      const invalidTask = {
        description: 'Task without title'
      };

      const response = await request(app)
        .post('/tasks')
        .send(invalidTask)
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.message).toContain('Title is required');
    });

    it('should return 400 for empty title', async () => {
      const invalidTask = {
        title: '   ',
        description: 'Task with empty title'
      };

      const response = await request(app)
        .post('/tasks')
        .send(invalidTask)
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.message).toContain('Title is required');
    });

    it('should return 400 for invalid completed value', async () => {
      const invalidTask = {
        title: 'Valid Title',
        completed: 'not a boolean'
      };

      const response = await request(app)
        .post('/tasks')
        .send(invalidTask)
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.message).toContain('Completed must be a boolean');
    });
  });

  describe('GET /tasks/:id', () => {
    it('should return a specific task by ID', async () => {
      if (!createdTaskId) {
        // Create a task first if none exists
        const newTask = { title: 'Task for GET test' };
        const createResponse = await request(app)
          .post('/tasks')
          .send(newTask);
        createdTaskId = createResponse.body.data.id;
      }

      const response = await request(app)
        .get(`/tasks/${createdTaskId}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.id).toBe(createdTaskId);
      expect(response.body.data).toHaveProperty('title');
      expect(response.body.data).toHaveProperty('description');
      expect(response.body.data).toHaveProperty('completed');
    });

    it('should return 404 for non-existent task', async () => {
      const nonExistentId = 99999;

      const response = await request(app)
        .get(`/tasks/${nonExistentId}`)
        .expect(404);

      expect(response.body.success).toBe(false);
      expect(response.body.message).toBe('Task not found');
    });
  });

  describe('PUT /tasks/:id', () => {
    it('should update an existing task', async () => {
      if (!createdTaskId) {
        // Create a task first if none exists
        const newTask = { title: 'Task for PUT test' };
        const createResponse = await request(app)
          .post('/tasks')
          .send(newTask);
        createdTaskId = createResponse.body.data.id;
      }

      const updatedData = {
        title: 'Updated Task Title',
        description: 'Updated description',
        completed: true
      };

      const response = await request(app)
        .put(`/tasks/${createdTaskId}`)
        .send(updatedData)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.id).toBe(createdTaskId);
      expect(response.body.data.title).toBe(updatedData.title);
      expect(response.body.data.description).toBe(updatedData.description);
      expect(response.body.data.completed).toBe(updatedData.completed);
      expect(response.body.message).toBe('Task updated successfully');
    });

    it('should return 404 for updating non-existent task', async () => {
      const nonExistentId = 99999;
      const updatedData = {
        title: 'Updated Title'
      };

      const response = await request(app)
        .put(`/tasks/${nonExistentId}`)
        .send(updatedData)
        .expect(404);

      expect(response.body.success).toBe(false);
      expect(response.body.message).toBe('Task not found');
    });

    it('should return 400 for invalid update data', async () => {
      if (!createdTaskId) {
        const newTask = { title: 'Task for validation test' };
        const createResponse = await request(app)
          .post('/tasks')
          .send(newTask);
        createdTaskId = createResponse.body.data.id;
      }

      const invalidData = {
        title: '',
        description: 'Valid description'
      };

      const response = await request(app)
        .put(`/tasks/${createdTaskId}`)
        .send(invalidData)
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.message).toContain('Title is required');
    });
  });

  describe('DELETE /tasks/:id', () => {
    it('should delete an existing task', async () => {
      // Create a task specifically for deletion
      const taskToDelete = { title: 'Task to be deleted' };
      const createResponse = await request(app)
        .post('/tasks')
        .send(taskToDelete);
      
      const taskId = createResponse.body.data.id;

      const response = await request(app)
        .delete(`/tasks/${taskId}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.id).toBe(taskId);
      expect(response.body.message).toBe('Task deleted successfully');

      // Verify task is actually deleted
      await request(app)
        .get(`/tasks/${taskId}`)
        .expect(404);
    });

    it('should return 404 for deleting non-existent task', async () => {
      const nonExistentId = 99999;

      const response = await request(app)
        .delete(`/tasks/${nonExistentId}`)
        .expect(404);

      expect(response.body.success).toBe(false);
      expect(response.body.message).toBe('Task not found');
    });
  });

  describe('Error Handling', () => {
    it('should return 404 for non-existent route', async () => {
      const response = await request(app)
        .get('/non-existent-route')
        .expect(404);

      expect(response.body.success).toBe(false);
      expect(response.body.message).toBe('Route not found');
    });

    it('should handle malformed JSON', async () => {
      const response = await request(app)
        .post('/tasks')
        .set('Content-Type', 'application/json')
        .send('{ invalid json }')
        .expect(400);
    });
  });

  describe('Integration Tests', () => {
    it('should perform complete CRUD cycle', async () => {
      // Create
      const newTask = {
        title: 'Integration Test Task',
        description: 'Testing full CRUD cycle',
        completed: false
      };

      const createResponse = await request(app)
        .post('/tasks')
        .send(newTask)
        .expect(201);

      const taskId = createResponse.body.data.id;
      expect(createResponse.body.data.title).toBe(newTask.title);

      // Read
      const readResponse = await request(app)
        .get(`/tasks/${taskId}`)
        .expect(200);

      expect(readResponse.body.data.title).toBe(newTask.title);

      // Update
      const updatedTask = {
        title: 'Updated Integration Test Task',
        description: 'Updated description',
        completed: true
      };

      const updateResponse = await request(app)
        .put(`/tasks/${taskId}`)
        .send(updatedTask)
        .expect(200);

      expect(updateResponse.body.data.title).toBe(updatedTask.title);
      expect(updateResponse.body.data.completed).toBe(true);

      // Delete
      await request(app)
        .delete(`/tasks/${taskId}`)
        .expect(200);

      // Verify deletion
      await request(app)
        .get(`/tasks/${taskId}`)
        .expect(404);
    });
  });
});
```


