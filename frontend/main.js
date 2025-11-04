const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let backendProc;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      webSecurity: false  // For local mic/voice
    }
  });

  // Load Vite build
  mainWindow.loadFile('dist/index.html');

  // Start bundled Python backend
  backendProc = spawn(path.join(__dirname, 'uniforge-backend'), [], { stdio: 'pipe' });
  backendProc.stdout.on('data', (data) => console.log(`Backend: ${data}`));
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (backendProc) backendProc.kill();
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});