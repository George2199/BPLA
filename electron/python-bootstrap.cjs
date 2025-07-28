// electron/python-bootstrap.cjs
const { app }       = require('electron');
const path          = require('path');
const os            = require('os');
const fs            = require('fs');
const crypto        = require('crypto');
const { spawnSync } = require('child_process');

/* ──────────────────────────────────────────────
   1. Путь к встроенному CPython
   ──────────────────────────────────────────── */
function bundledPython () {
  const base = path.join(process.resourcesPath, 'python');
  return process.platform === 'win32'
    ? path.join(base, 'python.exe')
    : path.join(base, 'bin', 'python3');
}

/* надёжное app.getPath */
function safePath (name, fallback) {
  try { return app.getPath(name); }
  catch { return fallback; }
}

/* ──────────────────────────────────────────────
   2. Хэш requirements.txt + версия CPython
   ──────────────────────────────────────────── */
function reqHash () {
  try {
    const req = fs.readFileSync(
      path.join(process.resourcesPath, 'pyapp', 'requirements.txt'),
      'utf8'
    );
    return crypto.createHash('sha1').update(req).digest('hex').slice(0, 8);
  } catch {
    return 'no-req';                       // если файла нет
  }
}

/* каталог виртуального окружения:
   pyenv-<312>-<b7a1c9e2>                        */
function venvDirForPlatform () {
  const base = safePath(
    'userData',
    process.platform === 'win32'
      ? path.join(os.tmpdir(), app.getName())
      : path.join(os.homedir(), '.config', app.getName())
  );
  const pyVer = (process.versions.python || '').replace('.', '') || 'py';
  return path.join(base, `pyenv-${pyVer}-${reqHash()}`);
}

function venvPython (venvDir) {
  return process.platform === 'win32'
    ? path.join(venvDir, 'Scripts', 'python.exe')
    : path.join(venvDir, 'bin', 'python3');
}

/* удобный spawnSync-wrapper */
function run (cmd, args) {
  const r = spawnSync(cmd, args, { encoding: 'utf8', stdio: 'pipe' });
  if (r.status !== 0) {
    console.error('[run:err]', cmd, args.join(' '));
    if (r.stdout) console.error('stdout:\n', r.stdout);
    if (r.stderr) console.error('stderr:\n', r.stderr);
  } else {
    console.log('[run:ok]', cmd, args.join(' '));
  }
  return r;
}

/* чистим старые pyenv-* каталоги, кроме текущего */
function cleanupOldVenvs (currentDir) {
  const base = path.dirname(currentDir);
  fs.readdirSync(base, { withFileTypes: true })
    .filter(d =>
      d.isDirectory() &&
      d.name.startsWith('pyenv-') &&
      path.join(base, d.name) !== currentDir
    )
    .forEach(d => {
      try { fs.rmSync(path.join(base, d.name), { recursive: true, force: true }); }
      catch (e) { console.warn('[venv:gc]', e); }
    });
}

/* ──────────────────────────────────────────────
   3. Главная функция
   ──────────────────────────────────────────── */
function ensureVenv () {
  const venvDir = venvDirForPlatform();
  const vpy     = venvPython(venvDir);

  /* venv уже существует  → выходим */
  if (fs.existsSync(vpy)) {
    cleanupOldVenvs(venvDir);
    return vpy;
  }

  /* каталог есть, но битый venv → удаляем */
  if (fs.existsSync(venvDir)) {
    try { fs.rmSync(venvDir, { recursive: true, force: true }); } catch {}
  }

  const py = bundledPython();
  console.log('[bootstrap] creating venv:', venvDir);

  /* создаём виртуальное окружение */
  const createArgs = ['-m', 'venv'];
  if (process.platform === 'win32') createArgs.push('--copies'); // без symlink
  createArgs.push(venvDir);

  let r = run(py, createArgs);
  if (r.status !== 0) {
    /* fallback: без pip */
    const alt = ['-m', 'venv', '--without-pip'];
    if (process.platform === 'win32') alt.push('--copies');
    alt.push(venvDir);
    r = run(py, alt);
    if (r.status !== 0) throw new Error('venv create failed');
  }

  /* пытаемся прокачать pip */
  run(vpy, ['-m', 'ensurepip', '--upgrade']);

  /* офлайн-установка из wheelhouse → при неудаче онлайн */
  const wheelhouse = path.join(process.resourcesPath, 'wheelhouse');
  const req        = path.join(process.resourcesPath, 'pyapp', 'requirements.txt');
  const baseArgs   = ['-m', 'pip', 'install', '--upgrade'];

  if (fs.existsSync(req)) {
    const offline = baseArgs.slice();
    if (fs.existsSync(wheelhouse)) offline.push('--no-index', '--find-links', wheelhouse);
    offline.push('-r', req);

    r = run(vpy, offline);
    if (r.status !== 0) {
      console.warn('[bootstrap] offline install failed → trying online');
      r = run(vpy, baseArgs.concat(['-r', req]));
      if (r.status !== 0) throw new Error('pip install failed');
    }
  }

  cleanupOldVenvs(venvDir);        // убираем старые окружения
  return vpy;
}

module.exports = { ensureVenv };