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
