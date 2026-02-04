# Natural Language Commands in Aura

Aura now supports a wide range of natural language commands to make coding even more intuitive. You can use these commands on their own or chain them together with the `then` keyword.

## 🎨 Styling
- **Color:** `Make the button red` or `Change the background to blue`
- **Size:** `Make the heading larger` or `Make the button smaller`
- **Themes:** `Use the dark theme`

## 👁️ Visibility
- **Hide:** `Hide the button`
- **Show:** `Show the input`
- **Toggle:** `Toggle the card` (switches between hidden/shown)

## 📝 Text Manipulation
- **Change Text:** `Change the heading to 'Welcome!'` or `Update the paragraph with 'New text'`
- **Case:** `Make the text uppercase` or `Make the text lowercase`

## 🖱️ Interaction
- **Focus:** `Focus on the input` (puts cursor in the box)
- **Disable/Enable:** `Disable the button` or `Enable the input`
- **Clear:** `Clear the input`

## ⏱️ Timing & Flow
- **Wait:** `Wait 2 seconds` (great for sequences!)
- **Navigation:** `Go to 'https://google.com'` or `Open 'link' in new tab`
- **Scroll:** `Scroll to the bottom` or `Scroll to the top`

## 📋 Clipboard
- **Copy:** `Copy 'Hello' to clipboard`
- **Copy Element:** `Copy the input to clipboard`

## ✨ Animations
- **Fade:** `Fade out the card` or `Fade in the image`
- **Slide:** `Slide in from left` (coming soon)

## 🔔 Notifications
- **Toast:** `Show a notification saying 'Success!'`

---

## Example Usage

```aura
Create a button with the text 'Magic Button'
When clicked, display 'Processing...', then wait 2 seconds, then fade out the button, then show a notification saying 'Done!'
```

```aura
Create an input with the text 'Search...'
Create a button with the text 'Go'
When clicked, focus on the input, then make the input bigger
```
