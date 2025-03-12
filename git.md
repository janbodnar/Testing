# Git

Git is a distributed version control system that tracks changes in computer  
files and coordinates work among multiple people. It's designed to handle  
everything from small to very large projects.  

## Set username and email

```
$ git config --global user.name "John Doe"
$ git config --global user.email johndoe@example.com
```

```
$ git config --list
```

## Most common commands


| Command                          | Description                                                                                  |
|----------------------------------|----------------------------------------------------------------------------------------------|
| `git init`                       | Initializes a new Git repository in the current directory.                                   |
| `git clone <repo>`               | Clones an existing repository from a remote source to your local machine.                    |
| `git status`                     | Displays the status of the working directory and staging area, showing changes and untracked files. |
| `git add <file>`                 | Adds changes in the specified file to the staging area.                                      |
| `git add .`                      | Adds all changes in the current directory to the staging area.                               |
| `git commit -m "message"`        | Commits the staged changes with a descriptive message.                                       |
| `git branch`                     | Lists all branches in the repository and highlights the current branch.                      |
| `git branch <branch-name>`       | Creates a new branch with the specified name.                                                |
| `git checkout <branch-name>`     | Switches to the specified branch.                                                            |
| `git merge <branch-name>`        | Merges the specified branch into the current branch.                                         |
| `git remote add origin <url>`    | Adds a remote repository with the name "origin" and the specified URL.                       |
| `git push -u origin main`        | Pushes the current branch to the remote repository and sets it as the upstream branch.       |
| `git pull origin main`           | Fetches and merges changes from the remote repository into the current branch.               |
| `git fetch`                      | Fetches changes from the remote repository without merging them.                             |
| `git log`                        | Displays the commit history for the repository.                                              |
| `git diff`                       | Shows changes between the working directory and the staging area, or between commits.        |
| `git remote -v`                  | Displays the names and URLs of all remote repositories associated with your local repository.|
| `git config --global user.name "John Doe"` | Sets the global Git configuration for the user's name, which applies to all repositories. |
| `git config --global user.email johndoe@example.com` | Sets the global Git configuration for the user's email, which applies to all repositories. |
| `git branch -M main`             | Renames the current branch to `main`.                                                        |

