# Github Pages 

Publis a project Github page.  


## Simple static page

It consists of an HTML page, CSS file, and a README file. 

The `README.me` file:

```md
# My Project Website

This is a simple static project website deployed using GitHub Pages.

## How to deploy

1. Push to the `main` branch.
2. Enable GitHub Pages in the repository settings (set source to `main` branch, `/root`).
3. Visit your site at `https://<your-username>.github.io/<repo-name>/`.
```

The `index.html` file:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Project Website</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>Welcome to My Project</h1>
        <nav>
            <a href="#about">About</a>
            <a href="#features">Features</a>
            <a href="#contact">Contact</a>
        </nav>
    </header>
    <main>
        <section id="about">
            <h2>About</h2>
            <p>This is a simple project website deployed with GitHub Pages.</p>
        </section>
        <section id="features">
            <h2>Features</h2>
            <ul>
                <li>Fast and simple</li>
                <li>Deployed with GitHub Pages</li>
                <li>Easy to maintain</li>
            </ul>
        </section>
        <section id="contact">
            <h2>Contact</h2>
            <p>Email: your@email.com</p>
        </section>
    </main>
    <footer>
        <p>&copy; 2025 My Project</p>
    </footer>
</body>
</html>
```

The `style.css` file:

```css
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background: #f9f9f9;
    color: #222;
}
header {
    background: #222;
    color: #fff;
    padding: 1.5rem 1rem 1rem 1rem;
    text-align: center;
}
nav a {
    color: #fff;
    margin: 0 1rem;
    text-decoration: none;
    font-weight: bold;
}
nav a:hover {
    text-decoration: underline;
}
main {
    max-width: 700px;
    margin: 2rem auto;
    background: #fff;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}
section {
    margin-bottom: 2rem;
}
footer {
    text-align: center;
    padding: 1rem;
    background: #eee;
    color: #555;
    position: fixed;
    width: 100%;
    bottom: 0;
    left: 0;
}
```

Create a local git repository:

```
git init && git add . && git commit -m "Initial commit"
```

Create a repo:

```
gh repo create serve-page --public --source . --remote=origin --push
```

Finally, enable GitHub Pages in the repository settings (set source to the `main` branch, `/root`).


