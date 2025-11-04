const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let backendProc;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      webSecurity: false
    }
  });

  mainWindow.loadFile('dist/index.html');

  // Start bundled backend
  const backendPath = path.join(__dirname, 'uniforge-backend');
  backendProc = spawn(backendPath, { stdio: 'pipe' });
  backendProc.stdout.on('data', data => console.log(`Backend: ${data}`));
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (backendProc) backendProc.kill();
  if (process.platform !== 'darwin') app.quit();
});