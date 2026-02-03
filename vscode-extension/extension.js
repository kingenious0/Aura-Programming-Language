const vscode = require('vscode');

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    console.log('Aura Language Support extension is now active');

    // Register command to run Aura transpiler
    let transpileCommand = vscode.commands.registerCommand('aura.transpile', async function () {
        const editor = vscode.window.activeTextEditor;
        
        if (!editor) {
            vscode.window.showErrorMessage('No active editor found');
            return;
        }

        const document = editor.document;
        
        if (document.languageId !== 'aura') {
            vscode.window.showErrorMessage('Current file is not an Aura file');
            return;
        }

        // Save the file first
        await document.save();

        const terminal = vscode.window.createTerminal('Aura Transpiler');
        const filePath = document.fileName;
        
        terminal.show();
        terminal.sendText(`python transpiler/transpiler.py "${filePath}"`);
        
        vscode.window.showInformationMessage('Transpiling Aura file...');
    });

    // Register command to start watch mode
    let watchCommand = vscode.commands.registerCommand('aura.watch', async function () {
        const editor = vscode.window.activeTextEditor;
        
        if (!editor) {
            vscode.window.showErrorMessage('No active editor found');
            return;
        }

        const document = editor.document;
        
        if (document.languageId !== 'aura') {
            vscode.window.showErrorMessage('Current file is not an Aura file');
            return;
        }

        // Save the file first
        await document.save();

        const terminal = vscode.window.createTerminal('Aura Watch Mode');
        const filePath = document.fileName;
        
        terminal.show();
        terminal.sendText(`python watch.py "${filePath}"`);
        
        vscode.window.showInformationMessage('Aura Watch Mode started');
    });

    context.subscriptions.push(transpileCommand);
    context.subscriptions.push(watchCommand);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
}
