const { app, BrowserWindow } = require('electron');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');
const { ensureVenv } = require('./bootstrap-python');

let backendProcess = null;
const isDev = !app.isPackaged;

const logDir = path.join(app.getPath('userData'), 'logs');
fs.mkdirSync(logDir, { recursive: true });
const logFile = path.join(logDir, 'electron.log');
const logStream = fs.createWriteStream(logFile, { flags: 'a' });

console.log = (...args) => {
  const line = `[LOG ${new Date().toISOString()}] ` + args.map(String).join(' ') + '\n';
  logStream.write(line);
};
console.error = (...args) => {
  const line = `[ERROR ${new Date().toISOString()}] ` + args.map(String).join(' ') + '\n';
  logStream.write(line);
};

function launchBackend() {
  let python, backendScript, cwd;

  if (isDev) {
    python = path.resolve(__dirname, '..', 'backend', 'venv', 'bin', 'python3');
    backendScript = path.resolve(__dirname, '..', 'backend', 'app.py');
    cwd = path.dirname(backendScript);
    console.log('Launching backend in DEV mode...');
  } else {
    python = ensureVenv(); // use embedded python & create venv if needed
    backendScript = path.join(process.resourcesPath, 'pyapp', 'app.py');
    cwd = path.dirname(backendScript);
    console.log('Launching backend in PROD mode...');
  }

  console.log('Python path:', python);
  console.log('Backend script:', backendScript);

  try {
    backendProcess = spawn(python, [backendScript], {
      cwd,
      detached: !isDev,
      stdio: isDev ? 'inherit' : 'ignore',
      windowsHide: true
    });

    if (!isDev) backendProcess.unref();
    console.log('Backend launched');
  } catch (e) {
    console.error('Failed to launch backend process:', e);
  }
}

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  launchBackend();

  if (isDev) {
    win.loadURL('http://localhost:5173').catch(err => {
      console.error('Dev load error:', err);
    });
    win.webContents.openDevTools();
  } else {
    const indexPath = path.join(process.resourcesPath, 'dist', 'index.html');
    win.loadFile(indexPath).then(() => {
      console.log('Frontend loaded');
    }).catch(err => {
      console.error('Failed to load index.html:', err);
    });
  }

  win.on('ready-to-show', () => console.log('Window ready'));
  win.webContents.on('did-fail-load', (e, code, desc, url) => {
    console.error(`Load failed: ${code} - ${desc} @ ${url}`);
  });
}

app.whenReady().then(() => {
  console.log('App ready');
  createWindow();
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  console.log('All windows closed');
  if (backendProcess && !backendProcess.killed) {
    try {
      process.kill(-backendProcess.pid);
      console.log('Backend killed');
    } catch (e) {
      console.error('Error killing backend:', e);
    }
  }
  if (process.platform !== 'darwin') app.quit();
});