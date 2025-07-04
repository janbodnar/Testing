# Github Actions

**GitHub Actions** is a powerful automation tool built right into GitHub that lets you 
automate, customize, and execute software development workflows directly in your repository.

## What It Does

- **CI/CD Automation**: Build, test, and deploy your code automatically when you push changes.
- **Event-Driven Workflows**: Trigger actions on events like `push`, `pull_request`, `issue`, or even on a schedule.
- **Custom Workflows**: Define your own workflows using YAML files stored in `.github/workflows/`.

##  Core Concepts

| Term       | Description |
|------------|-------------|
| **Workflow** | A YAML file that defines the automation process. |
| **Job**      | A set of steps that run in the same environment. |
| **Step**     | A single task, like running a script or using an action. |
| **Action**   | A reusable unit of code (can be custom or from the marketplace). |
| **Runner**   | The server/environment where jobs are executed (GitHub-hosted or self-hosted). |


## Example Use Cases

- Run tests automatically when code is pushed
- Deploy apps to cloud platforms like AWS, Azure, or Firebase
- Lint and format code on pull requests
- Send Slack notifications when builds fail

## Example

Authenticate.

```
gh auth login
```

Create local project. 

```
mkdir my-project
cd my-project
echo "# My Project" > README.md
git init
```

Add and commit files.

```
git add .
git commit -m "Initial commit"
```

Create a New GitHub Repo with CLI

```
gh repo create my-project --public --source=. --remote=origin --push
```

Push changes. 

```
# After making changes
git add .
git commit -m "Update something"
git push origin main
```

The `.github/workflows/ci.yaml` is a GitHub Actions workflow file that sets up a Continuous Integration (CI)  
pipeline for a project that uses Bun. 

```yaml
name: ci

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v1

      - run: bun install
      - run: bun test

  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v1

      - run: bun install
      - run: bun build ./index.js --outfile=./dist/index

      - uses: actions/upload-artifact@v4
        with:
          name: bun-binary
          path: ./dist/index
```

The workflow:

- Tests your code automatically on every push/PR
- Builds your main file
- Uploads the result for potential deployment or download
  

This is a simple Server created in Bun.  

```js
const server = Bun.serve({
  fetch(req) {
    const url = new URL(req.url);
    if (url.pathname === "/") {
      return new Response("Bun!");
    }
    if (url.pathname === "/greet") {
      return new Response("Hello, world!");
    }
    if (url.pathname === '/today') {
      return new Response(`Today is ${new Date().toLocaleDateString()}`);
    }
    return new Response("Not Found", { status: 404 });
  },
});

export default server;

console.log("Listening on http://localhost:3000 ...");
```

And this is a corresponding test file.  

```js
import { test, expect } from "bun:test";
import server from "./index.js";

test("GET /", async () => {
  const res = await server.fetch(new Request("http://localhost:3000/"));
  expect(res.status).toBe(200);
  const text = await res.text();
  expect(text).toBe("Bun!");
});

test("GET /greet", async () => {
  const res = await server.fetch(new Request("http://localhost:3000/greet"));
  expect(res.status).toBe(200);
  const text = await res.text();
  expect(text).toBe("Hello, world!");
});

test("GET /today", async () => {
  const res = await server.fetch(new Request("http://localhost:3000/today"));
  expect(res.status).toBe(200);
  const text = await res.text();
  expect(text).toContain("Today is");
});
```


