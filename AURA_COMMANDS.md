# Aura Programming Language - Command Reference v4.0

## 1. Project Configuration
| Command | Description |
| :--- | :--- |
| `Use the dark theme` | Switch to dark mode (default) |
| `Use the light theme` | Switch to light mode |
| `The app's title is 'My App'` | Set the browser tab title |
| `The user's name is 'John'` | Define a variable |

## 2. Page & Navigation
**Multi-Page Support**: Simply create new `.aura` files (e.g., `About.aura`).
| Command | Description |
| :--- | :--- |
| `Create a global navbar with links [Home, About]` | Adds a responsive navbar to ALL pages |
| `Create a global navbar with logo 'App' and links [Home, Page]` | Navbar with logo and links |
| `Create a link to page 'About' with the text 'Read More'` | Creates a clickable text link to an internal page |
| `When clicked, go to page 'About'` | Action: Navigate to an internal page instantly |
| `When clicked, go to 'https://google.com'` | Action: Navigate to an external URL |
| `When clicked, go to 'https://xyz.com' in a new tab` | Action: Open URL in a new tab |

## 3. UI Components
| Command | Description |
| :--- | :--- |
| `Create a heading with the text 'Hello'` | Main Page Heading (H1) |
| `Create a paragraph with the text 'Content...'` | Regular text block |
| `Create a button with the text 'Click Me'` | Action Button |
| `Create an input with the text 'Enter Name'` | Text Input Field |
| `Create a card with the title 'Title' and description 'Desc'` | Beautiful Card Component |
| `Create an image from 'https://example.com/img.jpg'` | Image Component |

## 4. Styling & Formatting
| Command | Description |
| :--- | :--- |
| `Align the heading to the center` | Center align the last element |
| `Align the text to the right` | Right align the last element |
| `Make the text bold` | Bold formatting |
| `Make the text italic` | Italic formatting |
| `Underline the title` | Underline formatting |
| `Make the text uppercase` | Uppercase formatting |

## 5. Interactivity (Actions)
Use `When clicked, ...` to add actions to the last element. You can chain actions using `then`.
| Command | Description |
| :--- | :--- |
| `display 'Hello World'` | Shows a browser alert |
| `refresh the page` | Reloads the current page |
| `wait 2 seconds` | Pauses execution (useful for mock loading) |
| `clear the input` | Clears the value of the last input |
| `show the element` | Makes a hidden element visible |
| `hide the element` | Hides an element |

**Example Chaining:**
```aura
When clicked, wait 2 seconds, then display 'Done!', then refresh the page
```

