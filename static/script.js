'use strict';
const $ = id => document.getElementById(id);
let model = null, ready = false, stream = null, running = false;
let generation = 0, result = null, sourceName = '', frameId = 0, busy = false;
let predictionPending = false;
const records = [], canvas = $('frame'), ctx = canvas.getContext('2d');
const threshold = () => Number($('threshold').value) / 100;
const say = (text, error = false) => { $('message').textContent = text; $('message').classList.toggle('error', error); };
function controls() {
  $('camera').disabled = !ready || busy || running;
  $('upload-button').disabled = !ready || busy;
  $('load').disabled = busy;
  $('stop').disabled = !running;
}
function stopCamera() {
  running = false;
  cancelAnimationFrame(frameId);
  if (stream) stream.getTracks().forEach(track => track.stop());
  stream = null; $('video').srcObject = null; controls();
}
function clearResult() {
  result = null; $('prediction').textContent = '—'; $('confidence').textContent = '—';
  $('confidence-bar').value = 0; $('scores').replaceChildren();
  $('decision').textContent = 'MENUNGGU INPUT';
  $('interpretation').textContent = 'Keputusan akan dipaparkan selepas inferens.';
  $('record').disabled = true;
}
function reset() {
  generation++; stopCamera(); busy = false; clearResult();
  $('frame').hidden = true; $('empty').hidden = false; $('upload').value = '';
  $('source').textContent = 'Tiada input'; sourceName = ''; controls();
  say(ready ? 'Sedia menerima input baharu.' : 'Muatkan model terlebih dahulu.');
}
function draw(source) {
  const w = source.videoWidth || source.naturalWidth || source.width;
  const h = source.videoHeight || source.naturalHeight || source.height;
  const side = Math.min(w, h);
  ctx.drawImage(source, (w-side)/2, (h-side)/2, side, side, 0, 0, 400, 400);
  $('frame').hidden = false; $('empty').hidden = true;
}
function render(scores) {
  if (!scores.length || scores.some(s => !Number.isFinite(s.confidence) || s.confidence < 0 || s.confidence > 1)) throw new Error('Output model tidak sah.');
  const sorted = [...scores].sort((a,b) => b.confidence-a.confidence), top = sorted[0];
  result = { prediction: top.confidence >= threshold() ? top.label : 'UNKNOWN', top_class: top.label,
    confidence: top.confidence, threshold: threshold(), scores,
    timestamp: new Date().toISOString(), source: sourceName,
    mode: $('mode').value, model: $('mode').value === 'browser' ? $('model-url').value : 'models/tflite' };
  $('prediction').textContent = result.prediction;
  $('confidence').textContent = (top.confidence*100).toFixed(2)+'%';
  $('confidence-bar').value = top.confidence;
  $('decision').textContent = result.prediction === 'UNKNOWN' ? 'KEYAKINAN RENDAH' : 'RAMALAN TERSEDIA';
  $('interpretation').textContent = result.prediction === 'UNKNOWN'
    ? `Calon tertinggi: ${top.label}. Cuba imej lebih jelas atau sudut lain.`
    : 'Semak objek sebenar. Confidence bukan jaminan bahawa ramalan betul.';
  $('scores').replaceChildren(...sorted.map(s => {
    const row = document.createElement('div'); row.className = 'score';
    const name = document.createElement('span'); name.textContent = s.label;
    const value = document.createElement('span'); value.textContent = (s.confidence*100).toFixed(1)+'%';
    const bar = document.createElement('progress'); bar.max=1; bar.value=s.confidence; bar.setAttribute('aria-label', s.label);
    row.append(name,value,bar); return row;
  }));
  $('record').disabled = false;
}
async function predict(token) {
  predictionPending = true;
  try {
  let scores;
  if ($('mode').value === 'browser') {
    scores = (await model.predict(canvas)).map(s => ({label:s.className,confidence:s.probability}));
  } else {
    const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg', .92));
    if (!blob) throw new Error('Imej tidak dapat diproses.');
    const form = new FormData(); form.append('file',blob,'frame.jpg');
    const response = await fetch('/predict?threshold='+threshold(), {method:'POST',body:form});
    const data = await response.json();
    if (!response.ok) throw new Error(typeof data.detail === 'string' ? data.detail : 'Permintaan API gagal.');
    scores = data.scores;
  }
  if (token === generation) render(scores);
  } finally { predictionPending = false; }
}
$('load').onclick = async () => {
  reset(); ready = false; busy = true; controls();
  $('model-status').textContent = 'Memuatkan model…';
  const token = generation;
  try {
    if ($('mode').value === 'api') {
      const response = await fetch('/health');
      if (!response.ok) throw new Error('Server FastAPI tidak dapat dicapai.');
      const data = await response.json();
      if (!data.model_ready) throw new Error(data.message);
    } else {
      if (!window.tmImage) throw new Error('Library AI tidak tersedia. Semak folder static/vendor dan muat semula halaman.');
      let base = $('model-url').value.trim();
      if (!base) throw new Error('Masukkan URL model.');
      const parsed = new URL(base, document.baseURI);
      if (parsed.origin !== location.origin && (parsed.protocol !== 'https:' || parsed.hostname !== 'teachablemachine.withgoogle.com')) throw new Error('Gunakan URL HTTPS Teachable Machine atau folder model tempatan.');
      base = parsed.href.replace(/\/?$/, '/');
      const loaded = await tmImage.load(base+'model.json',base+'metadata.json');
      if (token !== generation) { loaded.dispose?.(); return; }
      if (loaded.getTotalClasses() < 3) { loaded.dispose?.(); throw new Error('Tugasan memerlukan minimum tiga kelas.'); }
      model?.dispose?.(); model = loaded;
    }
    if (token !== generation) return;
    ready = true; $('model-status').textContent = 'Model tersedia. Anda boleh mula menguji.';
    say('Pilih kamera atau muat naik imej.');
  } catch(error) {
    if (token === generation) { $('model-status').textContent = 'Model belum tersedia.'; say(error.message.includes('404') ? 'Fail model tidak ditemui. Letak eksport dalam models/tfjs atau masukkan URL Teachable Machine yang sah.' : error.message, true); }
  } finally { if (token === generation) { busy=false; controls(); } }
};
function invalidateModel() {
  reset(); ready=false; model?.dispose?.(); model=null; controls();
  $('model-status').textContent='Muatkan model untuk tetapan ini.';
  $('url-field').hidden = $('mode').value === 'api';
  say('Muatkan model terlebih dahulu.');
}
$('mode').onchange = invalidateModel;
$('model-url').onchange = invalidateModel;
async function acquireCamera(token) {
  let expired = false, timer;
  const request = navigator.mediaDevices.getUserMedia({video:{width:640,height:480},audio:false})
    .then(acquired => {
      if (expired || token !== generation) acquired.getTracks().forEach(track => track.stop());
      return acquired;
    });
  try {
    return await Promise.race([request, new Promise((_, reject) => {
      timer = setTimeout(() => {
        expired = true;
        reject(new Error('Tiada respons kamera selepas 15 saat. Semak kebenaran kamera atau gunakan muat naik imej.'));
      }, 15000);
    })]);
  } finally { clearTimeout(timer); }
}
$('camera').onclick = async () => {
  reset(); const token=generation; busy=true; controls();
  try {
    if (!navigator.mediaDevices?.getUserMedia) throw new Error('Kamera memerlukan localhost atau HTTPS.');
    const acquired = await acquireCamera(token);
    if (token !== generation) { acquired.getTracks().forEach(t=>t.stop()); return; }
    stream=acquired; $('video').srcObject=stream; await $('video').play();
    if (token !== generation) return;
    running=true; busy=false; sourceName='webcam'; $('source').textContent='Kamera langsung'; controls();
    say('Kamera aktif. Hentikan kamera untuk merekod satu ramalan.');
    let last=0;
    async function loop(time) {
      if (!running || token !== generation) return;
      const interval=$('mode').value === 'api' ? 700 : 160;
      if (time-last >= interval) {
        last=time;
        try { draw($('video')); await predict(token); }
        catch(error) { if(token===generation){stopCamera();say(error.message,true);} return; }
      }
      if(running && token===generation) frameId=requestAnimationFrame(loop);
    }
    frameId=requestAnimationFrame(loop);
  } catch(error) { if(token===generation){stopCamera();say('Kamera gagal: '+error.message,true);} }
  finally { if(token===generation){busy=false;controls();} }
};
$('stop').onclick=()=>{const pending=predictionPending;generation++;stopCamera();if(pending)clearResult();say(pending ? 'Kamera dihentikan semasa inferens. Cuba upload imej untuk merekod keputusan tetap.' : 'Kamera dihentikan. Keputusan terakhir dikekalkan.');};
$('upload-button').onclick=()=>{$('upload').value='';$('upload').click();};
$('upload').onchange=async event=>{
  const file=event.target.files[0]; if(!file)return;
  reset(); const token=generation; busy=true;controls();
  let url;
  try {
    if(!['image/jpeg','image/png','image/webp'].includes(file.type))throw new Error('Gunakan JPEG, PNG atau WebP.');
    if(file.size>8*1024*1024)throw new Error('Fail melebihi 8 MB.');
    url=URL.createObjectURL(file); const img=new Image();img.src=url;await img.decode();
    if(token!==generation)return;
    if(img.naturalWidth*img.naturalHeight>16_000_000)throw new Error('Had resolusi ialah 16 megapiksel.');
    sourceName=file.name;$('source').textContent=file.name;draw(img);say('Memproses imej…');
    await predict(token);if(token===generation)say('Ramalan selesai.');
  }catch(error){if(token===generation)say(error.message,true);}
  finally{if(url)URL.revokeObjectURL(url);if(token===generation){busy=false;controls();}}
};
$('threshold').oninput=()=>{$('threshold-value').textContent=$('threshold').value+'%';if(result)render(result.scores);};
$('reset').onclick=reset;
$('record').onclick=()=>{
  if(!result)return;
  if(running){say('Hentikan kamera sebelum menyimpan rekod supaya imej dan keputusan kekal.',true);return;}
  const actual=$('actual').value.trim();if(!actual){say('Isi label sebenar sebelum merekod ujian.',true);$('actual').focus();return;}
  records.push({...result,experiment:$('experiment').value,actual,
    correct:actual===result.top_class,accepted_correct:actual===result.prediction});
  $('export').disabled=false;$('export').textContent=`Eksport CSV (${records.length})`;
  say('Rekod disimpan. Eksport CSV sebelum menutup halaman.');
};
$('export').onclick=()=>{
  const fields=['timestamp','experiment','source','mode','model','actual','top_class','prediction','confidence','threshold','correct','accepted_correct'];
  const escape=value=>'"'+String(value).replace(/^[=+@-]/,"'$&").replaceAll('"','""')+'"';
  const csv=[fields.join(','),...records.map(r=>fields.map(f=>escape(r[f])).join(','))].join('\r\n');
  const url=URL.createObjectURL(new Blob(['\ufeff'+csv],{type:'text/csv;charset=utf-8'}));
  const a=document.createElement('a');a.href=url;a.download='rekod-ujian.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
};
window.addEventListener('pagehide',stopCamera);
// The public static deployment ships E2 and starts it automatically.
if (document.documentElement?.dataset.deployment === 'pages') $('load').click();
