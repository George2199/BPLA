// electron/main.cjs
const { app, BrowserWindow, dialog } = require('electron')
const { autoUpdater } = require('electron-updater');
const log = require('electron-log');
const path = require('path')
const os    = require('os')
const fs = require('fs')
const { spawn } = require('child_process')
const { ensureVenv } = require('./python-bootstrap.cjs')

let backendProcess = null
const isDev = !app.isPackaged

/* ---------- безопасный app.getPath ------------------------------ */
function safePath (name) {
  try { return app.getPath(name) }
  catch { return path.join(os.tmpdir(), app.getName()) }   // точно доступно
}
/* --------------------------------------------------------------- */

function initAutoUpdater() {
  if (isDev) return;                // обновления нужны только в production

  autoUpdater.logger = log;
  autoUpdater.autoDownload = false; // не качаем в фон без спроса

  autoUpdater.on('update-available', info => {
    dialog.showMessageBox({
      type: 'info',
      title: 'Найдена новая версия',
      message: `Доступна ${info.version}. Скачать и установить?`,
      buttons: ['Да', 'Позже']
    }).then(({ response }) => {
      if (response === 0) autoUpdater.downloadUpdate();
    });
  });

  autoUpdater.on('download-progress', p =>
    log.info(`Скачано ${p.percent.toFixed(1)} %…`)
  );

  autoUpdater.on('update-downloaded', () => {
    dialog.showMessageBox({
      type: 'question',
      buttons: ['Перезапустить', 'Позже'],
      defaultId: 0,
      message: 'Обновление загружено. Перезапустить сейчас?'
    }).then(({ response }) => {
      if (response === 0) autoUpdater.quitAndInstall();
    });
  });

  autoUpdater.checkForUpdatesAndNotify();    // ← одна строка проверяет всё
}


const dataDir = safePath('userData')           // ← пригодится и для БД
const logDir  = path.join(dataDir, 'logs')
fs.mkdirSync(logDir, { recursive: true })
const logFile   = path.join(logDir, 'electron.log')
const logStream = fs.createWriteStream(logFile, { flags: 'a' })
console.log  = (...a) => logStream.write(`[LOG ${new Date().toISOString()}] ${a.join(' ')}\n`)
console.error = (...a) => logStream.write(`[ERROR ${new Date().toISOString()}] ${a.join(' ')}\n`)

function launchBackend () {
  let python, backendScript, cwd

  if (isDev) {
    python = process.platform === 'win32'
      ? path.resolve(__dirname, '..', 'backend', 'venv', 'Scripts', 'python.exe')
      : path.resolve(__dirname, '..', 'backend', 'venv', 'bin', 'python3')
    backendScript = path.resolve(__dirname, '..', 'backend', 'app.py')
    console.log('Launching backend in DEV mode...')
  } else {
    try {
      console.log('ENV LOCALAPPDATA =', process.env.LOCALAPPDATA);
      console.log('app.getPath("appData")', app.getPath('appData'));
      // console.log('app.getPath("localAppData")', (() => {
      //   try { return app.getPath('localAppData'); } catch (e) { return String(e); }
      // })());
      python = ensureVenv() // создаст venv в профиле пользователя и вернёт путь к интерпретатору
    } catch (e) {
      dialog.showErrorBox('Ошибка инициализации Python', e.message);
      console.error('[bootstrap] ensureVenv error:', e)
      throw e
    }
    backendScript = path.join(process.resourcesPath, 'pyapp', 'app.py')
    console.log('Launching backend in PROD mode...')
  }

  cwd = path.dirname(backendScript)
  console.log('Python path:', python)
  console.log('Backend script:', backendScript)

  const detached = process.platform !== 'win32' && !isDev

  backendProcess = spawn(python, [backendScript], {
    cwd,
    detached,
    stdio: isDev ? 'inherit' : 'pipe',
    windowsHide: true,
    env: {
      ...process.env,
      PYTHONNOUSERSITE: '1',
      APP_DATA_DIR: dataDir,        // <— передаём
      FLASK_ENV:  'production',
      FLASK_DEBUG: '0'
    }
  });

  if (!isDev) {
    backendProcess.stdout?.on('data', d => console.log('[py]', d.toString()))
    backendProcess.stderr?.on('data', d => console.error('[py]', d.toString()))
    if (detached) backendProcess.unref()
  }
}

function createWindow () {
  const win = new BrowserWindow({
    width: 1200, height: 800,
    webPreferences: { nodeIntegration: true, contextIsolation: false }
  })

  launchBackend()

  if (isDev) {
    win.loadURL('http://localhost:5173').catch(err => console.error('Dev load error:', err))
    win.webContents.openDevTools()
  } else {
    const indexPath = path.join(app.getAppPath(), 'dist', 'index.html')
    console.log('appPath=', app.getAppPath(), 'resourcesPath=', process.resourcesPath, 'index=', indexPath)
    win.loadFile(indexPath).then(() => console.log('Frontend loaded'))
      .catch(err => console.error('Failed to load index.html:', err))
  }

  win.on('ready-to-show', () => console.log('Window ready'))
  win.webContents.on('did-fail-load', (e, code, desc, url) => {
    console.error(`Load failed: ${code} - ${desc} @ ${url}`)
  })
}

app.whenReady().then(() => {
  console.log('App ready')
  createWindow();
  initAutoUpdater();
  app.on('activate', () => { if (BrowserWindow.getAllWindows().length === 0) createWindow() })
})

app.on('window-all-closed', () => {
  console.log('All windows closed')
  if (backendProcess && typeof backendProcess.pid === 'number') {
    try {
      backendProcess.kill() // Windows: без отрицательных PID
      console.log('Backend killed')
    } catch (e) { console.error('Error killing backend:', e) }
  }
  if (process.platform !== 'darwin') app.quit()
})