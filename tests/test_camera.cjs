// Simulated camera lifecycle only; this does not certify a physical webcam.
const test = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const source = fs.readFileSync(require('node:path').join(__dirname, '../static/script.js'), 'utf8');

function app(getUserMedia, timers = {}) {
  const elements = new Map();
  const element = id => {
    if (!elements.has(id)) elements.set(id, {
      value: id === 'mode' ? 'api' : id === 'threshold' ? '70' : '',
      classList: {toggle() {}}, getContext: () => ({}), replaceChildren() {},
      play: async () => {}, hidden: false, disabled: false,
    });
    return elements.get(id);
  };
  const context = vm.createContext({
    document: {getElementById: element}, navigator: {mediaDevices: {getUserMedia}},
    window: {addEventListener() {}}, requestAnimationFrame: () => 1,
    cancelAnimationFrame() {}, setTimeout, clearTimeout, ...timers,
  });
  vm.runInContext(source, context);
  vm.runInContext('ready = true', context);
  return {element, context};
}

test('camera permission refusal restores usable controls', async () => {
  const {element} = app(async () => { throw new Error('Permission denied'); });
  await element('camera').onclick();
  assert.match(element('message').textContent, /Permission denied/);
  assert.equal(element('upload-button').disabled, false);
  assert.equal(element('camera').disabled, false);
});

test('stop and reset release every active camera track', async () => {
  let stopped = 0;
  const stream = {getTracks: () => [{stop: () => stopped++}]};
  const {element} = app(async () => stream);
  await element('camera').onclick();
  assert.equal(element('video').srcObject, stream);
  element('stop').onclick();
  assert.equal(stopped, 1);
  assert.equal(element('video').srcObject, null);
  await element('camera').onclick();
  element('reset').onclick();
  assert.equal(stopped, 2);
  assert.equal(element('video').srcObject, null);
});

test('a camera granted after reset is immediately released', async () => {
  let grant, stopped = 0;
  const {element} = app(() => new Promise(resolve => {grant = resolve;}));
  const pending = element('camera').onclick();
  element('reset').onclick();
  grant({getTracks: () => [{stop: () => stopped++}]});
  await pending;
  assert.ok(stopped >= 1);
  assert.equal(element('video').srcObject, null);
});

test('timeout restores upload and stops a late camera stream', async () => {
  let expire, grant, stopped = 0;
  const {element} = app(() => new Promise(resolve => {grant = resolve;}), {
    setTimeout: callback => {expire = callback; return 1;}, clearTimeout() {},
  });
  const pending = element('camera').onclick();
  expire();
  await pending;
  assert.match(element('message').textContent, /15 saat/);
  assert.equal(element('upload-button').disabled, false);
  grant({getTracks: () => [{stop: () => stopped++}]});
  await Promise.resolve(); await Promise.resolve();
  assert.equal(stopped, 1);
  assert.equal(element('video').srcObject, null);
});
