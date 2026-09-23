# SmartVision Object Classifier

Prototaip DKA3223 untuk mengklasifikasikan **BOTOL, BUKU dan TELEFON** menggunakan Google Teachable Machine. Skop A (Object Image Classification). Kelas boleh diubah mengikut model terlatih.

## Status penting

Kod aplikasi dan panduan disediakan. **Dataset sebenar, model E1/E2, keputusan ketepatan, identiti pelajar dan pautan GitHub belum dibekalkan.** Tiada model atau keputusan eksperimen direka. Aplikasi akan memaparkan mesej model belum tersedia sehingga anda memasukkan eksport sebenar. Laporan dan slaid perlu dilengkapkan dengan bukti tersebut sebelum dihantar.

## Mula di sini

1. Baca `docs/PANDUAN_LANGKAH_DEMI_LANGKAH.md` untuk persediaan dataset dan semua 12 fasa gambar.
2. Pasang Python 3.12 (64 bit). Jalankan arahan berikut dalam folder `SmartClassifier`:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

3. Buka http://127.0.0.1:8000. Jangan buka `index.html` terus melalui `file://`.
4. Latih model di https://teachablemachine.withgoogle.com/train/image.
5. Pilih **TensorFlow.js**, muat naik model dan salin URL. Dalam aplikasi pilih mod Pelayar, tampal URL, tekan **Muatkan model**.
6. Alternatif: muat turun eksport TensorFlow.js, ekstrak semua fail ke `models/tfjs/`, gunakan `/models/tfjs/`.
7. Mulakan kamera atau muat naik imej. Model dikira dalam pelayar bagi mod ini. Internet diperlukan untuk library CDN, dan model jika dihoskan dalam Teachable Machine.

## Backend Python sebenar

1. Eksport versi model yang sama: **TensorFlow Lite → Floating point / unquantized**.
2. Letak `model_unquant.tflite` dan `labels.txt` dalam `models/tflite/`. Kekalkan susunan label eksport.
3. Pasang kebergantungan model dan mulakan semula server:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-model.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

4. Pilih mod **Python · FastAPI**, kemudian **Muatkan model**. `/health` mesti menunjukkan `model_ready: true`.
5. Buka http://127.0.0.1:8000/docs untuk menguji `POST /predict`. Input ialah multipart fail imej. Output menggunakan skema Pydantic.

```powershell
curl.exe -X POST "http://127.0.0.1:8000/predict?threshold=0.7" -F "file=@dataset/test/BOTOL/botol_001.jpg"
```

Contoh bentuk respons sahaja, **bukan keputusan ujian sebenar**:

```json
{"prediction":"BOTOL","top_class":"BOTOL","confidence":0.94,"status":"recognized","threshold":0.7,"scores":[{"label":"BOTOL","confidence":0.94},{"label":"BUKU","confidence":0.04},{"label":"TELEFON","confidence":0.02}]}
```

FastAPI melakukan inferens pada server dalam mod Python. Ia bukan sekadar menerima prediction daripada pelayar. Dalam mod Pelayar, FastAPI menyediakan fail aplikasi sahaja. Export TF.js tidak boleh dibaca terus oleh interpreter TFLite.

## Ciri aplikasi

- Kamera dan upload JPEG, PNG, WebP, had 8 MB / 16 megapiksel.
- Kelas ramalan, confidence peratus dan skor setiap kelas.
- Ambang default 70%, UNKNOWN jika di bawah ambang. Ini bukan pengesan objek asing yang terjamin.
- Reset, hentikan kamera dan mesej ralat untuk model, fail atau kebenaran kamera.
- Label sebenar dan eksport CSV rekod ujian. Hentikan kamera sebelum merekod keputusan.
- Antaramuka responsif dalam Bahasa Melayu.

## Aliran data

Pelayar: imej/webcam → crop tengah → tmImage.predict → skor kelas → threshold → UI.

Python: imej/webcam → POST /predict → pengesahan fail → EXIF/RGB → crop tengah dan resize mengikut model → normalisasi [-1,1] → TensorFlow Lite → Pydantic JSON → UI.

Kamera dipaparkan tanpa mirror untuk konsisten dengan imej upload. Input aplikasi dipotong kepada 400 × 400 sebelum inferens. Ujian batch API membaca imej asal lalu resize terus ke saiz model. Perbezaan resampling boleh menghasilkan sedikit perbezaan skor; gunakan mod dan aliran yang sama untuk perbandingan eksperimen serta rekodkan aliran ujian.

## Ujian kod dan penilaian model

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe tools/check_dataset.py dataset
.\.venv\Scripts\python.exe tools/evaluate.py --data dataset/validation --experiment E1 --out evidence/validation
.\.venv\Scripts\python.exe tools/evaluate.py --data dataset/test --experiment FINAL --out evidence/testing
```

Ujian `tests/test_api.py` menggunakan test double untuk kontrak respons. Ia **tidak membuktikan ketepatan model sebenar**. Skrip penilaian memerlukan model sebenar yang dimuat di server, menjana CSV setiap imej, accuracy top-1, coverage threshold dan confusion matrix. Jangan latih atau pilih model berdasarkan set test akhir. Tukar model dan restart server untuk menilai versi lain.

## Struktur

```text
app/                 FastAPI, skema Pydantic dan inferens TFLite
static/              index.html, script.js, style.css
models/tfjs/         eksport model untuk pelayar
models/tflite/       eksport FLOAT untuk Python
dataset/             train_e1, train_e2, validation, test
tools/               semakan dataset dan penilaian batch
tests/               ujian kod
docs/                panduan, laporan dan bahan pembentangan
evidence/            borang eksperimen, sumber dataset, bukti AI dan testing
```

## Deployment

Deployment tempatan di localhost sudah membolehkan demo aplikasi/API. Jika pensyarah memerlukan URL awam, gunakan hos Python yang menyokong TensorFlow, bind `0.0.0.0` dan port persekitaran hos, simpan model dalam storan deployment, gunakan HTTPS untuk kamera. Rujuk `docs/DEPLOYMENT_DAN_GITHUB.md`. Tiada deployment awam atau repository GitHub diterbitkan secara automatik.

## Rujukan rasmi

- Teachable Machine image library: https://github.com/googlecreativelab/teachablemachine-community/tree/master/libraries/image
- Model converter dan normalisasi: https://github.com/googlecreativelab/teachablemachine-community/blob/master/snippets/converter/image/api.py
- FastAPI file input: https://fastapi.tiangolo.com/tutorial/request-files/
- Pydantic models: https://docs.pydantic.dev/latest/concepts/models/
- TensorFlow Lite interpreter: https://www.tensorflow.org/api_docs/python/tf/lite/Interpreter

Arahan projek dalam `DKA3223 FA .docx` ialah sumber keperluan. Gambar tutorial ialah rujukan urutan pembangunan. Perancangan dan sasaran sampel di dalam pakej ini bukan keputusan yang telah dicapai.
