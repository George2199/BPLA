const { app } = require('electron')
const path = require('path')
const fs = require('fs')
const crypto = require('crypto')
const { spawnSync } = require('child_process')

function bundledPython() {
  const base = path.join(process.resourcesPath, 'python')
  return process.platform === 'win32'
    ? path.join(base, 'python.exe')
    : path.join(base, 'bin', 'python3')
}
function venvPython(venvDir) {
  return process.platform === 'win32'
    ? path.join(venvDir, 'Scripts', 'python.exe')
    : path.join(venvDir, 'bin', 'python3')
}
function hashFile(p) {
  try { return crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex').slice(0,12) }
  catch { return 'no-req' }
}

function ensureVenv() {
  const venvDir = path.join(app.getPath('userData'), 'pyenv')
  const vpy = venvPython(venvDir)
  const req = path.join(process.resourcesPath, 'pyapp', 'requirements.txt')
  const reqHash = hashFile(req)
  const stamp = path.join(venvDir, `.installed-${reqHash}`)

  const needInstall =
    !fs.existsSync(vpy) || !fs.existsSync(stamp)

  if (!needInstall) return vpy

  // (пере)создаём venv
  const py = bundledPython()
  if (!fs.existsSync(vpy)) {
    console.log('[bootstrap] creating venv:', venvDir)
    let r = spawnSync(py, ['-m', 'venv', venvDir], { stdio: 'inherit' })
    if (r.status !== 0) throw new Error('venv create failed')
  }

  console.log('[bootstrap] ensurepip')
  spawnSync(vpy, ['-m', 'ensurepip', '--upgrade'], { stdio: 'inherit' })

  // офлайн → при неудаче онлайн
  const wheelhouse = path.join(process.resourcesPath, 'wheelhouse')
  const baseArgs = ['-m','pip','install','--upgrade']
  const offlineArgs = baseArgs.slice()
  if (fs.existsSync(wheelhouse)) offlineArgs.push('--no-index','--find-links', wheelhouse)
  if (fs.existsSync(req))        offlineArgs.push('-r', req)

  console.log('[bootstrap] pip install (offline if wheelhouse exists)')
  let r = spawnSync(vpy, offlineArgs, {
    stdio: 'inherit',
    env: { ...process.env, PYTHONNOUSERSITE: '1', PIP_DISABLE_PIP_VERSION_CHECK: '1' }
  })
  if (r.status !== 0 && fs.existsSync(req)) {
    console.warn('[bootstrap] offline failed — trying online')
    r = spawnSync(vpy, baseArgs.concat(['-r', req]), {
      stdio: 'inherit',
      env: { ...process.env, PYTHONNOUSERSITE: '1', PIP_DISABLE_PIP_VERSION_CHECK: '1' }
    })
    if (r.status !== 0) throw new Error('pip install failed')
  }

  // ставим маркер и чистим старые
  for (const f of fs.readdirSync(venvDir)) {
    if (f.startsWith('.installed-') && f !== path.basename(stamp)) {
      try { fs.unlinkSync(path.join(venvDir, f)) } catch {}
    }
  }
  fs.writeFileSync(stamp, new Date().toISOString())
  return vpy
}

module.exports = { ensureVenv }