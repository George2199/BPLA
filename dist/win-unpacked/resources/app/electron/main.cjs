const { app, BrowserWindow } = require('electron');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

let backendProcess = null;

const logDir = path.join(process.resourcesPath || __dirname, 'logs');
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

function launchBackend(isDev) {
  if (isDev) {
    const backendScript = path.join(__dirname, 'backend', 'app.py');
    console.log('Launching backend in dev mode from:', backendScript);
    backendProcess = spawn('python', [backendScript], {
      cwd: path.dirname(backendScript),
      stdio: 'ignore',
      detached: true,
    });
  } else {
    const backendScript = path.join(process.resourcesPath, 'backend', 'app.py');
    const python = path.join(process.resourcesPath, 'venv', 'Scripts', 'python.exe'); // Windows
    console.log('Launching backend in prod mode from:', backendScript);
    backendProcess = spawn(python, [backendScript], {
      cwd: path.dirname(backendScript),
      stdio: 'ignore',
      detached: true,
      windowsHide: true,
    });
  }

  if (backendProcess) {
    backendProcess.unref();
    console.log('Backend launched.');
  } else {
    console.error('Failed to launch backend process.');
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

  const isDev = !app.isPackaged;
  console.log('isDev =', isDev);
  launchBackend(isDev);

  if (isDev) {
    const devUrl = 'http://localhost:5173';
    console.log('Loading dev server at:', devUrl);
    win.loadURL(devUrl).catch(err => {
      console.error('Failed to load dev URL:', err);
    });
    win.webContents.openDevTools();
  } else {
    const indexPath = path.join(app.getAppPath(), 'dist', 'index.html');
    win.loadFile(indexPath).then(() => {
      console.log('index.html loaded successfully.');
    }).catch(err => {
      console.error('Failed to load index.html:', err);
    });
  }

  win.on('ready-to-show', () => console.log('Window ready to show'));
  win.webContents.on('did-finish-load', () => console.log('Finished loading web content'));
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
      process.kill(-backendProcess.pid); // kill group
      console.log('Backend process killed');
    } catch (e) {
      console.error('Failed to kill backend process:', e);
    }
  }
  if (process.platform !== 'darwin') app.quit();
});
