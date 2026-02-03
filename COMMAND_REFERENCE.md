# Aura Programming Language - Complete Command Reference

## Overview
Aura is a natural language programming language that transpiles English commands into professional HTML, CSS, and JavaScript.

---

## Command Types

### 1. Variables (Data Storage)

Store data in JavaScript variables.

**Syntax:**
```aura
The [object]'s [property] is '[value]'
```

**Examples:**
```aura
The user's name is 'John Doe'
The app's title is 'My Application'
The product's price is '99.99'
```

**Generated Code:**
```javascript
const user_name = 'John Doe';
const app_title = 'My Application';
const product_price = '99.99';
```

---

### 2. Themes

Apply visual themes to your application.

**Syntax:**
```aura
Use the [theme] theme
```

**Available Themes:**
- `dark` - Modern dark theme with glassmorphism
- `light` - Clean light theme with professional styling
- `default` - Simple, minimal theme

**Examples:**
```aura
Use the dark theme
Use the light theme
Use the default theme
```

---

### 3. UI Elements

#### 3.1 Buttons

**Syntax:**
```aura
Create a button with the text '[text]'
```

**Example:**
```aura
Create a button with the text 'Click Me'
Create a button with the text 'Submit Form'
```

**Generated HTML:**
```html
<button id="aura_elem_0">Click Me</button>
```

---

#### 3.2 Headings

**Syntax:**
```aura
Create a heading with the text '[text]'
```

**Example:**
```aura
Create a heading with the text 'Welcome to My App'
```

**Generated HTML:**
```html
<h1 id="aura_elem_0">Welcome to My App</h1>
```

---

#### 3.3 Paragraphs

**Syntax:**
```aura
Create a paragraph with the text '[text]'
```

**Example:**
```aura
Create a paragraph with the text 'This is a description of my application.'
```

**Generated HTML:**
```html
<p id="aura_elem_0">This is a description of my application.</p>
```

---

#### 3.4 Input Fields

**Syntax:**
```aura
Create an input with the text '[placeholder]'
```

**Example:**
```aura
Create an input with the text 'Enter your name'
Create an input with the text 'Email address'
```

**Generated HTML:**
```html
<input id="aura_elem_0" type="text" placeholder="Enter your name">
```

---

#### 3.5 Cards

Cards are styled containers for content.

**Syntax:**
```aura
Create a card with the title '[title]'
Create a card with the title '[title]' and description '[description]'
```

**Examples:**
```aura
Create a card with the title 'Feature 1'
Create a card with the title 'About Us' and description 'Learn more about our company'
```

**Generated HTML:**
```html
<div class="card" id="aura_elem_0">
    <h3>About Us</h3>
    <p>Learn more about our company</p>
</div>
```

---

#### 3.6 Images

**Syntax Option 1 (Simple):**
```aura
Create an image from '[url]'
```

**Syntax Option 2 (With Alt Text):**
```aura
Create an image with the url '[url]' and alt '[alt text]'
```

**Examples:**
```aura
Create an image from 'https://example.com/photo.jpg'
Create an image with the url 'https://example.com/logo.png' and alt 'Company Logo'
```

**Generated HTML:**
```html
<img id="aura_elem_0" src="https://example.com/logo.png" alt="Company Logo">
```

---

### 4. Actions (Event Handling)

Actions must follow a UI element to attach event handlers.

#### 4.1 Display Message

Shows an alert dialog.

**Syntax:**
```aura
When [event], display '[message]'
```

**Example:**
```aura
Create a button with the text 'Click Me'
When clicked, display 'Hello, World!'
```

**Generated JavaScript:**
```javascript
document.getElementById('aura_elem_0').addEventListener('click', function() {
    alert('Hello, World!');
});
```

---

#### 4.2 Alert

Shows an alert dialog (same as display).

**Syntax:**
```aura
When [event], alert '[message]'
```

**Example:**
```aura
Create a button with the text 'Submit'
When clicked, alert 'Form submitted successfully!'
```

---

#### 4.3 Refresh Page

Reloads the current page.

**Syntax:**
```aura
When [event], refresh the page
```

**Example:**
```aura
Create a button with the text 'Reload'
When clicked, refresh the page
```

**Generated JavaScript:**
```javascript
document.getElementById('aura_elem_0').addEventListener('click', function() {
    location.reload();
});
```

---

### 5. Action Modifiers

Modifiers add additional actions to the previous event handler.

#### 5.1 And Refresh

Adds a page refresh after the previous action.

**Syntax:**
```aura
And refresh the page
```

**Example:**
```aura
Create a button with the text 'Submit'
When clicked, display 'Form submitted!'
And refresh the page
```

**Generated JavaScript:**
```javascript
document.getElementById('aura_elem_0').addEventListener('click', function() {
    alert('Form submitted!');
    location.reload();
});
```

---

### 6. Layout Commands

#### 6.1 Center Element

Centers the previous element.

**Syntax:**
```aura
Put the [element] in the middle
Put the [element] in the center
```

**Example:**
```aura
Create a button with the text 'Centered Button'
Put the button in the middle
```

**Generated HTML:**
```html
<button id="aura_elem_0" class="center">Centered Button</button>
```

---

### 7. Networking (Advanced)

Make API requests (generates fetch code).

**Syntax:**
```aura
Ask "[url]" for [data type]
```

**Example:**
```aura
Ask "api.weather.com/current" for weather
```

**Generated JavaScript:**
```javascript
fetch('https://api.weather.com/current')
    .then(response => response.json())
    .then(data => {
        console.log('weather:', data);
    })
    .catch(error => console.error('Error fetching weather:', error));
```

---

### 8. Deployment

Adds deployment-ready comments.

**Syntax:**
```aura
Go live
```

**Example:**
```aura
Go live
```

**Generated JavaScript:**
```javascript
// Deployment: This application is ready to go live!
console.log('Aura app ready for deployment!');
```

---

## Complete Example

```aura
# My First Aura Application
Use the dark theme

# Variables
The app's name is 'Todo App'
The user's role is 'admin'

# Header
Create a heading with the text 'Welcome to Aura'
Create a paragraph with the text 'Build apps with natural language!'

# Interactive Buttons
Create a button with the text 'Say Hello'
When clicked, display 'Hello from Aura!'

Create a button with the text 'Refresh'
When clicked, refresh the page

# Input Form
Create an input with the text 'Enter your name'
Create an input with the text 'Enter your email'
Create a button with the text 'Submit'
When clicked, alert 'Form submitted!'
And refresh the page

# Feature Cards
Create a card with the title 'Easy Syntax' and description 'Write code in plain English'
Create a card with the title 'Beautiful Output' and description 'Professional HTML and CSS'
Create a card with the title 'Fast Development' and description 'Build apps in minutes'

# Images
Create an image with the url 'https://example.com/banner.jpg' and alt 'App Banner'

# Deployment
Go live
```

---

## Event Types

Currently supported events:
- `clicked` / `click` - Mouse click event
- `submit` - Form submission
- `hover` - Mouse hover (mouseenter)

---

## Best Practices

1. **Theme First**: Set your theme at the beginning of the file
2. **Variables Early**: Define variables before using them
3. **UI Then Actions**: Create UI elements before attaching actions
4. **Comments**: Use `#` for comments to document your code
5. **Modifiers**: Use `And` to chain multiple actions

---

## File Structure

```
my_app.aura          # Your Aura source file
index.html           # Generated output (default)
```

---

## Command Line Usage

```bash
# Basic transpilation
python transpiler/transpiler.py app.aura

# Custom output file
python transpiler/transpiler.py app.aura output.html

# Watch mode (auto-transpile on save)
python watch.py app.aura
```

---

## Supported Scopes (Syntax Highlighting)

- `keyword.control.aura` - Create, Use, When, And, Put, Ask, Go
- `entity.name.tag.ui.aura` - button, heading, paragraph, input, card, image
- `keyword.control.action.aura` - clicked, display, alert, refresh
- `string.quoted.aura` - String literals
- `comment.line.aura` - Comments
- `support.constant.aura` - Themes
- `variable.other.property.aura` - Variables

---

## Future Enhancements

- Loops and conditionals
- More UI components (tables, forms, modals)
- CSS customization commands
- Multi-page support
- Component reusability
- Data binding
- More event types
- Animation commands

---

**Happy coding with Aura!**
