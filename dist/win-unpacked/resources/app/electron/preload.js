const fs = require('fs');
const path = require('path');
const logPath = path.join(__dirname, '..', 'logs', 'electron.log');
const logStream = fs.createWriteStream(logPath, { flags: 'a' });

function logToFile(type, ...args) {
  const time = new Date().toISOString();
  logStream.write(`[${type}] ${time} ${args.join(' ')}\n`);
}

window.addEventListener('DOMContentLoaded', () => {
  ['log', 'warn', 'error'].forEach(type => {
    const original = console[type];
    console[type] = (...args) => {
      original(...args);
      logToFile(type.toUpperCase(), ...args.map(String));
    };
  });
});
