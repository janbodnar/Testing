# Web components

This is the home page, `index.html`.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Cards</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="app">
        <h1>Contact Cards</h1>
        <div class="controls">
            <button id="loadBtn" class="btn">Load Contacts</button>
            <div id="status" class="status"></div>
        </div>
        <cards-container id="cardsContainer" class="cards-container" loading>
            <!-- Contact cards will be inserted here -->
        </cards-container>
    </div>
    <script type="module" src="contact-card.mjs"></script>
    <script type="module" src="app.mjs"></script>
</body>
</html>
```

The overall `styles.css` file. 

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    background-color: #f5f5f5;
    color: #333;
    line-height: 1.6;
    padding: 20px;
    min-height: 100vh;
}

.app {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

h1 {
    text-align: center;
    margin-bottom: 30px;
    color: #2c3e50;
}

.controls {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    margin-bottom: 20px;
}

.btn {
    padding: 0.75rem 1.5rem;
    background-color: #4a6bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.2s;
}

.btn:hover {
    background-color: #3a5bef;
}

.status {
    padding: 0.5rem 1rem;
    border-radius: 4px;
    font-size: 0.9rem;
}

.cards-container {
    display: block;
    min-height: 200px;
    position: relative;
}

.cards-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    padding: 20px;
    max-width: 1400px;
    margin: 0 auto;
}

.error {
    color: #d32f2f;
    text-align: center;
    padding: 1rem;
    background-color: #ffebee;
    border-radius: 4px;
    margin: 1rem 0;
}

/* Responsive adjustments */
@media (max-width: 1024px) {
    .cards-container {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 768px) {
    .cards-container {
        grid-template-columns: 1fr;
    }
    
    .app {
        padding: 10px;
    }
}

/* Ensure web components are block elements by default */
:not(:defined) {
    display: block;
    opacity: 0;
    transition: opacity 0.3s ease-in-out;
}
```
