'use strict';

const assert = require('node:assert/strict');
const { spawnSync } = require('node:child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');
const test = require('node:test');

const { createPrivateTempDir, writePrivateJson } = require('./secure_temp');

test('为每次运行创建唯一的私有临时目录和结果文件', (t) => {
  const first = createPrivateTempDir('claude-skills-test-');
  const second = createPrivateTempDir('claude-skills-test-');
  t.after(() => {
    fs.rmSync(first, { recursive: true, force: true });
    fs.rmSync(second, { recursive: true, force: true });
  });

  assert.notEqual(first, second);
  assert.equal(path.dirname(first), fs.realpathSync(os.tmpdir()));
  assert.equal(path.dirname(second), fs.realpathSync(os.tmpdir()));

  const resultPath = path.join(first, 'result.json');
  writePrivateJson(resultPath, { success: true });
  assert.deepEqual(JSON.parse(fs.readFileSync(resultPath, 'utf8')), { success: true });

  if (process.platform !== 'win32') {
    assert.equal(fs.statSync(first).mode & 0o777, 0o700);
    assert.equal(fs.statSync(resultPath).mode & 0o777, 0o600);
  }
});

test('拒绝可能逃逸临时目录根路径的前缀', () => {
  assert.throws(() => createPrivateTempDir('../escape-'), /非法字符/);
});

test('普通预检和未授权 live smoke 不创建调试目录', (t) => {
  const isolatedTempRoot = fs.mkdtempSync(path.join(fs.realpathSync(os.tmpdir()), 'claude-skills-gate-test-'));
  t.after(() => fs.rmSync(isolatedTempRoot, { recursive: true, force: true }));

  const env = {
    ...process.env,
    TEMP: isolatedTempRoot,
    TMP: isolatedTempRoot,
    TMPDIR: isolatedTempRoot,
    JUEJIN_COOKIE: '',
  };
  const preview = spawnSync(
    process.execPath,
    [path.join(__dirname, 'post_to_juejin.js'), '离线预检', __filename],
    { encoding: 'utf8', env },
  );
  assert.equal(preview.status, 0, preview.stderr);
  assert.match(preview.stdout, /预检完成，未创建草稿、未发布文章/);

  const liveSmoke = spawnSync(
    process.execPath,
    [path.join(__dirname, 'test_juejin_post.js')],
    { encoding: 'utf8', env },
  );
  assert.equal(liveSmoke.status, 1);
  assert.match(liveSmoke.stderr, /只有显式传入 --publish 才会运行/);
  assert.deepEqual(fs.readdirSync(isolatedTempRoot), []);
});
