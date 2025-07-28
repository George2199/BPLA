// electron/python-bootstrap.cjs
const { app } = require('electron');
const path = require('path');
const os   = require('os');
const fs = require('fs');
const { spawnSync } = require('child_process')

function bundledPython() {
  const base = path.join(process.resourcesPath, 'python')
  return process.platform === 'win32'
    ? path.join(base, 'python.exe')
    : path.join(base, 'bin', 'python3')
}

function safePath(name, fallback) {
  try { return app.getPath(name); }
  catch { return fallback; }            // никогда не бросаем наружу
}

function venvDirForPlatform () {
  const base = safePath(
    'userData',
    // надёжные каталоги, существующие на всех Windows
    process.platform === 'win32'
      ? path.join(os.tmpdir(), app.getName())        // C:\Users\...\AppData\Local\Temp\AeroCosmos
      : path.join(os.homedir(), '.config', app.getName())
  );
  return path.join(base, 'pyenv');
}

function venvPython(venvDir) {
  return process.platform === 'win32'
    ? path.join(venvDir, 'Scripts', 'python.exe')
    : path.join(venvDir, 'bin', 'python3')
}

function run(cmd, args) {
  const r = spawnSync(cmd, args, { encoding: 'utf8', stdio: 'pipe' })
  if (r.status !== 0) {
    console.error('[run:err]', cmd, args.join(' '))
    if (r.stdout) console.error('stdout:\n', r.stdout)
    if (r.stderr) console.error('stderr:\n', r.stderr)
  } else {
    console.log('[run:ok]', cmd, args.join(' '))
  }
  return r
}

function ensureVenv() {
  const venvDir = venvDirForPlatform()
  const vpy = venvPython(venvDir)

  // venv валиден — выходим
  if (fs.existsSync(vpy)) return vpy

  // если каталог существует, но интерпретатора нет — чистим
  if (fs.existsSync(venvDir) && !fs.existsSync(vpy)) {
    try { fs.rmSync(venvDir, { recursive: true, force: true }) } catch {}
  }

  const py = bundledPython()
  console.log('[bootstrap] creating venv:', venvDir)

  // На Windows используем --copies, чтобы не упереться в права на симлинки
  const createArgs = ['-m', 'venv']
  if (process.platform === 'win32') createArgs.push('--copies')
  createArgs.push(venvDir)

  let r = run(py, createArgs)
  if (r.status !== 0) {
    // Фолбэк: создаём без pip (на случай проблем в момент инициализации pip)
    const alt = ['-m', 'venv', '--without-pip']
    if (process.platform === 'win32') alt.push('--copies')
    alt.push(venvDir)
    r = run(py, alt)
    if (r.status !== 0) throw new Error('venv create failed')
  }

  // попробовать ensurepip (если есть)
  run(vpy, ['-m', 'ensurepip', '--upgrade'])

  const wheelhouse = path.join(process.resourcesPath, 'wheelhouse')
  const req = path.join(process.resourcesPath, 'pyapp', 'requirements.txt')
  const baseArgs = ['-m', 'pip', 'install', '--upgrade']

  if (fs.existsSync(req)) {
    // офлайн → если не вышло, онлайн
    const offline = baseArgs.slice()
    if (fs.existsSync(wheelhouse)) offline.push('--no-index', '--find-links', wheelhouse)
    offline.push('-r', req)

    r = run(vpy, offline)
    if (r.status !== 0) {
      console.warn('[bootstrap] offline failed — trying online')
      r = run(vpy, baseArgs.concat(['-r', req]))
      if (r.status !== 0) throw new Error('pip install failed')
    }
  }

  return vpy
}

module.exports = { ensureVenv }