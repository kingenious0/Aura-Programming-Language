const vscode = require('vscode');
const { spawn } = require('child_process');
const path = require('path');

let brainDaemon = null;
let requestId = 0;

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    console.log('Aura Language Support extension is now active');

    // Start the Brain Daemon for real-time corrections
    startBrainDaemon(context);

    // Register inline completion provider for ghost text
    const completionProvider = vscode.languages.registerInlineCompletionItemProvider(
        { language: 'aura' },
        {
            async provideInlineCompletionItems(document, position, context, token) {
                const line = document.lineAt(position.line);
                const lineText = line.text;
                
                // Only suggest if line is not empty and cursor is at end
                if (!lineText.trim() || position.character !== lineText.length) {
                    return [];
                }

                // Request correction from daemon
                const correction = await requestCorrection(lineText);
                
                if (correction && correction.changed) {
                    const item = new vscode.InlineCompletionItem(
                        correction.corrected,
                        new vscode.Range(position.line, 0, position.line, lineText.length)
                    );
                    
                    return [item];
                }
                
                return [];
            }
        }
    );

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
        terminal.sendText(`python -m transpiler.transpiler build "${filePath}"`);
        
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

        const terminal = vscode.window.createTerminal('Aura Watch Mode');
        const workspaceFolder = vscode.workspace.workspaceFolders[0].uri.fsPath;
        
        terminal.show();
        terminal.sendText(`cd "${workspaceFolder}" && python watch.py .`);
        
        vscode.window.showInformationMessage('Aura Watch Mode started');
    });

    // Register command to manually trigger correction on current line
    let correctLineCommand = vscode.commands.registerCommand('aura.correctLine', async function () {
        const editor = vscode.window.activeTextEditor;
        if (!editor) return;

        const position = editor.selection.active;
        const line = editor.document.lineAt(position.line);
        const lineText = line.text;

        const correction = await requestCorrection(lineText);
        
        if (correction && correction.changed) {
            await editor.edit(editBuilder => {
                editBuilder.replace(line.range, correction.corrected);
            });
            
            // Show purple flash effect (via status bar)
            vscode.window.setStatusBarMessage('✨ Aura Brain: Corrected!', 1000);
        }
    });

    context.subscriptions.push(completionProvider);
    context.subscriptions.push(transpileCommand);
    context.subscriptions.push(watchCommand);
    context.subscriptions.push(correctLineCommand);
}

/**
 * Start the Brain Daemon process
 */
function startBrainDaemon(context) {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!workspaceFolder) return;

    try {
        brainDaemon = spawn('python', ['-m', 'transpiler.brain_daemon'], {
            cwd: workspaceFolder,
            stdio: ['pipe', 'pipe', 'pipe']
        });

        brainDaemon.stderr.on('data', (data) => {
            console.log(`[Aura Brain Daemon] ${data.toString()}`);
        });

        brainDaemon.on('close', (code) => {
            console.log(`[Aura Brain Daemon] Process exited with code ${code}`);
            brainDaemon = null;
        });

        console.log('[Aura Brain Daemon] Started successfully');
    } catch (error) {
        console.error('[Aura Brain Daemon] Failed to start:', error);
    }
}

/**
 * Request correction from the daemon
 * @param {string} line - Line of code to correct
 * @returns {Promise<{original: string, corrected: string, changed: boolean}>}
 */
function requestCorrection(line) {
    return new Promise((resolve, reject) => {
        if (!brainDaemon) {
            resolve(null);
            return;
        }

        const id = ++requestId;
        const request = {
            jsonrpc: '2.0',
            id: id,
            method: 'correct',
            params: { line: line }
        };

        let responseData = '';
        
        const onData = (data) => {
            responseData += data.toString();
            
            // Check if we have a complete JSON response
            try {
                const response = JSON.parse(responseData);
                if (response.id === id) {
                    brainDaemon.stdout.removeListener('data', onData);
                    resolve(response.result);
                }
            } catch (e) {
                // Not complete yet, keep accumulating
            }
        };

        brainDaemon.stdout.on('data', onData);
        
        // Send request
        brainDaemon.stdin.write(JSON.stringify(request) + '\n');

        // Timeout after 500ms
        setTimeout(() => {
            brainDaemon.stdout.removeListener('data', onData);
            resolve(null);
        }, 500);
    });
}

function deactivate() {
    if (brainDaemon) {
        brainDaemon.kill();
    }
}

module.exports = {
    activate,
    deactivate
}
