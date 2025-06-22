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

The main `app.mjs` file that starts the application. 

```mjs
const API_URL = 'https://webcode.me/students.json';

// Import the CardsContainer to ensure it's registered
import './cards-container.mjs';

class ContactCardsApp {
    constructor() {
        this.container = document.getElementById('cardsContainer');
        this.loadBtn = document.getElementById('loadBtn');
        this.statusEl = document.getElementById('status');
        
        this.init();
    }
    
    init() {
        // Add event listener to the load button
        this.loadBtn.addEventListener('click', () => this.loadContacts());
        
        // Load contacts automatically when the page loads
        this.loadContacts();
    }
    
    async loadContacts() {
        try {
            // Show loading state
            this.setLoading(true);
            this.setStatus('Loading contacts...', 'info');
            
            // Fetch data from the API
            const response = await fetch(API_URL);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const contacts = await response.json();
            this.displayContacts(contacts);
            this.setStatus(`Loaded ${contacts.length} contacts`, 'success');
        } catch (error) {
            console.error('Error loading contacts:', error);
            this.setStatus(`Error: ${error.message}`, 'error');
            this.showError('Failed to load contacts. Please try again.');
        } finally {
            this.setLoading(false);
        }
    }
    
    displayContacts(contacts) {
        // Clear existing cards
        this.container.innerHTML = '';
        
        if (!contacts || !contacts.length) {
            this.showMessage('No contacts found');
            return;
        }
        
        // Sort contacts alphabetically by name
        const sortedContacts = [...contacts].sort((a, b) => a.name.localeCompare(b.name));
        
        // Create and append contact cards
        sortedContacts.forEach(contact => {
            const card = document.createElement('contact-card');
            card.setAttribute('name', contact.name);
            card.setAttribute('avatar', contact.avatar);
            card.setAttribute('hobbies', JSON.stringify(contact.hobbies));
            card.setAttribute('theme', contact.theme);
            
            this.container.appendChild(card);
        });
    }
    
    setLoading(isLoading) {
        if (isLoading) {
            this.loadBtn.disabled = true;
            this.container.loading = true;
        } else {
            this.loadBtn.disabled = false;
            this.container.loading = false;
        }
    }
    
    setStatus(message, type = 'info') {
        this.statusEl.textContent = message;
        this.statusEl.className = 'status';
        if (type === 'error') {
            this.statusEl.style.color = '#d32f2f';
        } else if (type === 'success') {
            this.statusEl.style.color = '#2e7d32';
        }
    }
    
    showError(message) {
        const errorEl = document.createElement('div');
        errorEl.className = 'error';
        errorEl.textContent = message;
        this.container.appendChild(errorEl);
    }
    
    showMessage(message) {
        const messageEl = document.createElement('div');
        messageEl.className = 'message';
        messageEl.textContent = message;
        this.container.appendChild(messageEl);
    }
}

// Initialize the app when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ContactCardsApp();
});
```

The `cards-container.mjs` custom tag:

```mjs
// Import the CSS module
import containerStyles from './cards-container.css' with { type: 'css' };

class CardsContainer extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.render();
    }

    static get observedAttributes() {
        return ['loading'];
    }

    connectedCallback() {
        this.render();
    }

    attributeChangedCallback(name, oldValue, newValue) {
        if (name === 'loading' && this.shadowRoot) {
            const loadingEl = this.shadowRoot.querySelector('.loading');
            if (loadingEl) {
                loadingEl.style.display = newValue !== null ? 'flex' : 'none';
            }
        }
    }

    get loading() {
        return this.hasAttribute('loading');
    }

    set loading(value) {
        if (value) {
            this.setAttribute('loading', '');
        } else {
            this.removeAttribute('loading');
        }
    }

    render() {
        // Adopt the stylesheet
        if (!this.shadowRoot.adoptedStyleSheets.includes(containerStyles)) {
            this.shadowRoot.adoptedStyleSheets = [...this.shadowRoot.adoptedStyleSheets, containerStyles];
        }

        this.shadowRoot.innerHTML = `
            <div class="loading">
                <div class="spinner"></div>
                <p>Loading contacts...</p>
            </div>
            <slot></slot>
        `;
    }
}

// Define the custom element
if (!customElements.get('cards-container')) {
    customElements.define('cards-container', CardsContainer);
}

export default CardsContainer;
```

The `cards-container.css` file:

```css
:host {
    display: block;
    position: relative;
    min-height: 200px;
}

:host([loading]) ::slotted(*) {
    opacity: 0.5;
    pointer-events: none;
}

.loading {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: none;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    color: #666;
}

:host([loading]) .loading {
    display: flex;
}

.spinner {
    width: 40px;
    height: 40px;
    border: 4px solid rgba(0, 0, 0, 0.1);
    border-radius: 50%;
    border-top-color: #4a6bff;
    animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

::slotted(*) {
    transition: opacity 0.3s ease-in-out;
}
```

The `contact-card.mjs` component:

```mjs
// Import the CSS module and template
import cardStyles from './contact-card.css' with { type: 'css' };
import { cardTemplate } from './contact-card.template.mjs';

class ContactCard extends HTMLElement {
    static get observedAttributes() {
        return ['name', 'avatar', 'hobbies', 'theme'];
    }

    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }

    connectedCallback() {
        this.render();
    }

    attributeChangedCallback(name, oldValue, newValue) {
        if (oldValue !== newValue) {
            this.render();
        }
    }

    get name() {
        return this.getAttribute('name') || 'Unknown';
    }

    get avatar() {
        return this.getAttribute('avatar') || 'https://api.dicebear.com/6.x/lorelei/svg?seed=0';
    }

    get theme() {
        return this.getAttribute('theme') || '#f5f5f5';
    }

    get hobbies() {
        try {
            const hobbies = this.getAttribute('hobbies');
            if (!hobbies) return [];
            // Handle both JSON strings and comma-separated values
            if (hobbies.startsWith('[')) {
                return JSON.parse(hobbies);
            }
            return hobbies.split(',').map(h => h.trim());
        } catch (e) {
            console.error('Error parsing hobbies:', e);
            return [];
        }
    }

    render() {
        // Adopt the stylesheet
        if (!this.shadowRoot.adoptedStyleSheets.includes(cardStyles)) {
            this.shadowRoot.adoptedStyleSheets = [...this.shadowRoot.adoptedStyleSheets, cardStyles];
        }

        // Set the theme CSS variable
        this.style.setProperty('--card-theme', this.theme);

        // Generate the HTML
        const hobbiesHTML = this.hobbies
            .map(hobby => `<span class="hobby">${hobby}</span>`)
            .join('');

        // Set the inner HTML using the imported template
        this.shadowRoot.innerHTML = cardTemplate(this.name, this.avatar, hobbiesHTML);
    }
}

// Define the custom element
if (!customElements.get('contact-card')) {
    customElements.define('contact-card', ContactCard);
}
```

The `contact-card.template.mjs` file:

```mjs
export const cardTemplate = (name, avatar, hobbiesHTML) => `
    <div class="card" part="card">
        <div class="card-header" part="header">
            <img 
                src="${avatar}" 
                alt="${name}'s avatar" 
                class="avatar" 
                part="avatar"
                loading="lazy"
                width="100"
                height="100">
        </div>
        <div class="card-body" part="body">
            <h3 class="card-title" part="title">${name}</h3>
            ${hobbiesHTML ? `
                <div class="hobbies" part="hobbies">
                    ${hobbiesHTML}
                </div>
            ` : ''}
        </div>
    </div>
`;
```

The `contact-card.css` file:

```css
:host {
    display: block;
    margin-bottom: 20px;
    --card-theme: var(--card-theme, #f5f5f5);
}

.card {
    background: white;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    height: 100%;
    display: flex;
    flex-direction: column;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.card-header {
    height: 150px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    background-color: var(--card-theme);
}

.avatar {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    border: 4px solid white;
    object-fit: cover;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card-body {
    padding: 20px;
    text-align: center;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
}

.card-title {
    margin: 0 0 10px 0;
    color: #2c3e50;
    font-size: 1.5rem;
}

.hobbies {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 8px;
    margin-top: auto;
    padding-top: 15px;
}

.hobby {
    background-color: #e8f4f8;
    color: #2980b9;
    padding: 4px 10px;
    border-radius: 15px;
    font-size: 0.8rem;
    white-space: nowrap;
}

@media (max-width: 768px) {
    .card {
        max-width: 100%;
    }
}
```

