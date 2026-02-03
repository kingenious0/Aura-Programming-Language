# Publishing Aura VS Code Extension

This guide walks you through publishing the Aura Language Support extension to the VS Code Marketplace.

## Prerequisites

1. **Node.js and npm** installed
2. **Microsoft Account** (free)
3. **Azure DevOps Account** (free)
4. **Visual Studio Code** installed

## Step 1: Install Required Tools

```bash
# Install vsce (Visual Studio Code Extension Manager)
npm install -g vsce

# Install dependencies
cd vscode-extension
npm install
```

## Step 2: Create a Publisher Account

1. Go to https://marketplace.visualstudio.com/manage
2. Sign in with your Microsoft account
3. Click "Create publisher"
4. Fill in the details:
   - **Publisher ID**: Choose a unique ID (e.g., `aura-lang`, `yourname-aura`)
   - **Display Name**: Your name or organization
   - **Email**: Your email address

## Step 3: Generate a Personal Access Token (PAT)

1. Go to https://dev.azure.com
2. Sign in with the same Microsoft account
3. Click on your profile icon → "Personal access tokens"
4. Click "New Token"
5. Configure the token:
   - **Name**: "VS Code Extension Publishing"
   - **Organization**: All accessible organizations
   - **Expiration**: 90 days (or custom)
   - **Scopes**: Select "Marketplace" → Check "Manage"
6. Click "Create"
7. **IMPORTANT**: Copy the token immediately (you won't see it again!)

## Step 4: Update package.json

Update the `publisher` field in `package.json` with your publisher ID:

```json
{
  "publisher": "your-publisher-id",
  ...
}
```

## Step 5: Package the Extension

```bash
cd vscode-extension

# Package the extension
vsce package

# This creates a .vsix file (e.g., aura-language-1.0.0.vsix)
```

## Step 6: Test Locally (Optional but Recommended)

```bash
# Install the extension locally to test
code --install-extension aura-language-1.0.0.vsix

# Test it with your .aura files
# Uninstall when done testing
```

## Step 7: Publish to Marketplace

### Option A: Using Command Line (Recommended)

```bash
# Login with your PAT
vsce login your-publisher-id
# Paste your Personal Access Token when prompted

# Publish the extension
vsce publish

# Or publish with a specific version bump
vsce publish patch  # 1.0.0 -> 1.0.1
vsce publish minor  # 1.0.0 -> 1.1.0
vsce publish major  # 1.0.0 -> 2.0.0
```

### Option B: Manual Upload

1. Go to https://marketplace.visualstudio.com/manage
2. Click on your publisher
3. Click "New extension" → "Visual Studio Code"
4. Upload the `.vsix` file
5. Fill in any additional details
6. Click "Upload"

## Step 8: Verify Publication

1. Wait 5-10 minutes for the extension to be processed
2. Search for your extension in VS Code marketplace
3. Check the extension page at: `https://marketplace.visualstudio.com/items?itemName=your-publisher-id.aura-language`

## Publishing Timeline

- **Automated Validation**: 1-5 minutes
- **Marketplace Listing**: Immediate after validation
- **Search Indexing**: Up to 24 hours
- **Verified Publisher Badge**: Up to 5 business days (optional)

## Updating the Extension

When you make changes:

```bash
# Update version in package.json
# Then publish
vsce publish patch  # or minor/major
```

## Important Notes

1. **Free to Publish**: No fees required
2. **No Manual Review**: Automated validation only
3. **Public by Default**: Extensions are public unless you specify otherwise
4. **Icon**: Add an icon to `vscode-extension/icons/aura-icon.png` for better visibility
5. **README**: The README.md will be displayed on the marketplace page

## Troubleshooting

### "Publisher not found"
- Make sure you created a publisher account
- Verify the publisher ID in package.json matches your account

### "Authentication failed"
- Your PAT may have expired
- Generate a new PAT and login again

### "Extension validation failed"
- Check the error message
- Common issues: missing required fields in package.json, invalid grammar file

## Best Practices

1. **Version Control**: Tag releases in Git
   ```bash
   git tag v1.0.0
   git push --tags
   ```

2. **Changelog**: Keep a CHANGELOG.md file updated

3. **Testing**: Always test locally before publishing

4. **Icon**: Add a professional icon (128x128 PNG)

5. **Screenshots**: Add screenshots to the README for the marketplace

## Resources

- [VS Code Extension Publishing Guide](https://code.visualstudio.com/api/working-with-extensions/publishing-extension)
- [Extension Manifest Reference](https://code.visualstudio.com/api/references/extension-manifest)
- [Marketplace Publisher Portal](https://marketplace.visualstudio.com/manage)

## Cost

**Publishing is 100% FREE!** There are no fees for:
- Creating a publisher account
- Publishing extensions
- Hosting on the marketplace
- Updates and maintenance

---

**Ready to publish? Follow the steps above and share Aura with the world!**
