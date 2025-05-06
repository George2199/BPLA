const { app, BrowserWindow } = require('electron');
const path = require('path');

const fs = require('fs');
const logFile = path.join(app.getPath('userData'), 'electron-log.txt');
const logStream = fs.createWriteStream(logFile, { flags: 'a' });

console.log = (...args) => {
  logStream.write(args.map(String).join(' ') + '\n');
};
console.error = console.log;

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  const isDev = process.env.VITE_DEV_SERVER_URL || process.env.NODE_ENV === 'development';

  if (isDev) {
    win.loadURL('http://localhost:5173');
    win.webContents.openDevTools();
  } else {
    win.loadFile(path.join(__dirname, '/dist/index.html'));
  }
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
