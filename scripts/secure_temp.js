'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');

function createPrivateTempDir(prefix = 'claude-skills-') {
  if (!/^[A-Za-z0-9._-]+$/.test(prefix)) {
    throw new TypeError(`临时目录前缀包含非法字符: ${prefix}`);
  }

  const tempRoot = fs.realpathSync(os.tmpdir());
  const tempDir = fs.mkdtempSync(path.join(tempRoot, prefix));
  fs.chmodSync(tempDir, 0o700);
  return tempDir;
}

function writePrivateJson(filePath, value) {
  fs.writeFileSync(filePath, JSON.stringify(value), {
    encoding: 'utf8',
    flag: 'w',
    mode: 0o600,
  });
  fs.chmodSync(filePath, 0o600);
}

module.exports = { createPrivateTempDir, writePrivateJson };
