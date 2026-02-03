# Aura 'then' Keyword - Sequential Actions

## Overview

The `then` keyword allows you to chain multiple actions together in a single event handler. This enables complex workflows without writing multiple separate action commands.

---

## Syntax

```aura
When [event], [action1], then [action2], then [action3]
```

---

## Supported Actions

### 1. Display/Alert Message
```aura
display 'Message'
alert 'Message'
```

### 2. Refresh Page
```aura
refresh the page
```

### 3. Clear Input
```aura
clear the input
```

### 4. Show/Hide Element
```aura
show the [element]
hide the [element]
```

---

## Examples

### Example 1: Display then Refresh
```aura
Create a button with the text 'Submit'
When clicked, display 'Saved!', then refresh the page
```

**Generated JavaScript:**
```javascript
document.getElementById('aura_elem_0').addEventListener('click', function() {
    alert('Saved!');
    location.reload();
});
```

---

### Example 2: Display then Clear Input
```aura
Create an input with the text 'Enter name'
Create a button with the text 'Submit'
When clicked, display 'Form submitted!', then clear the input
```

**Generated JavaScript:**
```javascript
document.getElementById('aura_elem_1').addEventListener('click', function() {
    alert('Form submitted!');
    document.getElementById('aura_elem_1').value = '';
});
```

---

### Example 3: Multiple Actions Chained
```aura
Create an input with the text 'Type something'
Create a button with the text 'Process'
When clicked, display 'Processing...', then clear the input, then refresh the page
```

**Generated JavaScript:**
```javascript
document.getElementById('aura_elem_1').addEventListener('click', function() {
    alert('Processing...');
    document.getElementById('aura_elem_1').value = '';
    location.reload();
});
```

---

### Example 4: Alert then Refresh
```aura
Create a button with the text 'Reload'
When clicked, alert 'This will reload the page', then refresh the page
```

**Generated JavaScript:**
```javascript
document.getElementById('aura_elem_0').addEventListener('click', function() {
    alert('This will reload the page');
    location.reload();
});
```

---

## How It Works

1. **Parser**: The `action_sequence` pattern captures the entire action string after `When [event],`
2. **Splitting**: The action string is split by `, then ` to get individual actions
3. **Parsing**: Each action is parsed using regex to determine its type and parameters
4. **Generation**: JavaScript code is generated for each action
5. **Combination**: All actions are combined into a single event listener

---

## Action Types Recognized

| Action String | Type | JavaScript Generated |
|---------------|------|---------------------|
| `display 'X'` | Display | `alert('X');` |
| `alert 'X'` | Alert | `alert('X');` |
| `refresh the page` | Refresh | `location.reload();` |
| `clear the input` | Clear Input | `element.value = '';` |
| `hide the element` | Hide | `element.style.display = 'none';` |
| `show the element` | Show | `element.style.display = 'block';` |

---

## Best Practices

1. **Order Matters**: Actions execute in the order specified
2. **Refresh Last**: If using `refresh the page`, it should be the last action
3. **Clear Specific**: `clear the input` clears the element that triggered the event
4. **Readable**: Use descriptive action sequences for maintainability

---

## Limitations

- `clear the input` only works on input elements
- `refresh the page` will interrupt any subsequent actions
- Maximum recommended: 3-4 chained actions for readability

---

## Comparison with 'And' Modifier

### Old Way (And modifier):
```aura
Create a button with the text 'Submit'
When clicked, display 'Saved!'
And refresh the page
```

### New Way (then keyword):
```aura
Create a button with the text 'Submit'
When clicked, display 'Saved!', then refresh the page
```

Both work, but `then` is more concise and allows unlimited chaining.

---

## Complete Example

```aura
# Form with Sequential Actions
Use the dark theme

Create a heading with the text 'Contact Form'
Create a paragraph with the text 'Fill out the form below'

Create an input with the text 'Your Name'
Create an input with the text 'Your Email'
Create an input with the text 'Your Message'

Create a button with the text 'Submit'
When clicked, display 'Thank you! Your message has been sent.', then clear the input, then refresh the page

Create a button with the text 'Reset'
When clicked, clear the input
```

---

## Syntax Highlighting

The `then` keyword is highlighted with the `keyword.control.aura` scope in VS Code.

---

## Future Enhancements

Potential future actions:
- `navigate to 'url'`
- `set value to 'X'`
- `toggle the element`
- `focus the input`
- `submit the form`
- `log 'message'`

---

**The `then` keyword makes Aura even more powerful for building interactive applications!**
