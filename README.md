# SmartVision Object Classifier

Prototaip DKA3223 untuk mengenal pasti **BOTOL, BUKU dan TELEFON**. Model dilatih menggunakan Google Teachable Machine; aplikasi menyediakan inferens dalam pelayar (TensorFlow.js) dan backend Python (FastAPI, Pydantic dan Google LiteRT).

[Repository awam](https://github.com/Mr-F101/smartvision-dka3223) · [GitHub Actions lulus](https://github.com/Mr-F101/smartvision-dka3223/actions/runs/36247215924) · [Bukti penerbitan](evidence/GITHUB_DELIVERY.md)

## Jalankan aplikasi

Windows, Python 3.12 64-bit:

1. Muat turun/clone repository ini dan buka folder projek.
2. Jalankan `SETUP.bat` sekali. Ia memasang runtime dan mengesahkan model sebenar.
3. Jalankan `MULA.bat`, kemudian buka **http://127.0.0.1:8000**.
4. Pilih mod Pelayar atau Python, tekan **Muatkan model**, kemudian upload imej. Model aktif ialah E2.

Arahan terminal (Linux/macOS: gunakan `python3` dan `.venv/bin/python`):

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-model.txt
.\.venv\Scripts\python.exe tools/verify_install.py
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Fail model dan library pelayar disertakan. Selepas pemasangan Python, demo menggunakan model tempatan tanpa memerlukan CDN atau pautan model awam. Jangan buka index.html melalui file://. Untuk kamera, gunakan localhost atau HTTPS dan benarkan kebenaran pelayar; upload imej ialah laluan demo yang telah disahkan.

## Dataset dan keputusan sebenar

Dataset mempunyai **210 imej unik**: 50 latihan, 10 validation dan 10 test setiap kelas. train_e1 dan train_e2 sengaja berkongsi 150 imej latihan yang sama. Sumber Open Images dan atribusi setiap gambar tersedia dalam [dataset_public](dataset_public/README.md) dan [attribution.csv](evidence/public_dataset/attribution.csv).

| Eksperimen | Epoch | Batch | Learning rate | Validation |
|---|---:|---:|---:|---:|
| E1 | 50 | 16 | 0.001 | 26/30 (86.67%) |
| E2 | 100 | 16 | 0.001 | 27/30 (90.00%) |

E2 dipilih berdasarkan validation sebelum test akhir: **28/30 (93.33% top-1)**. Ini bukan jaminan prestasi dunia sebenar; hanya 30 imej test. Seed dan split dalaman TM tidak dikawal, jadi epoch bukan punca peningkatan yang terbukti secara tersendiri. [Pemilihan model](evidence/MODEL_SELECTION.md), [perbandingan](evidence/validation/PERBANDINGAN.md), [CSV test](evidence/testing/FINAL_E2.csv).

Eksport TFJS asal dan TFLite untuk kedua-dua versi berada dalam `models/experiments`. TFLite ditukar secara tempatan daripada TFJS tanpa latihan semula. `models/tfjs` dan `models/tflite` ialah salinan E2 untuk aplikasi. Cap jari model dan imej sepadan dengan bukti penilaian.

## Ciri dan had

- Upload JPEG/PNG/WebP, maksimum 8 MB dan 16 megapiksel; kamera jika tersedia.
- Kelas ramalan, confidence, skor setiap kelas, status dan reset.
- Ambang 70% menghasilkan UNKNOWN apabila confidence rendah. Ini **bukan pengesan semua objek asing**: imej Bumi di luar kelas mendapat BOTOL 96.70% melalui API. Lihat [bukti luar skop](evidence/out_of_scope/api_result.json).
- Simpan label sebenar dan eksport CSV. Rekod hanya kekal dalam sesi pelayar; muat turun sebelum menutup halaman.
- Kamera yang tidak memberi respons berhenti menunggu selepas 15 saat; upload kekal boleh digunakan. Ujian logik kamera menggunakan simulasi dan tidak membuktikan webcam fizikal setiap mesin.

## Aliran inferens dan API

Pelayar: imej/webcam → crop tengah canvas 400×400 → tmImage.predict → skor → threshold → UI.

Python: imej → POST /predict → semakan fail → EXIF/RGB → crop tengah/resize → normalisasi [-1,1] → model TFLite melalui LiteRT → respons Pydantic → UI.

GET `/health` mesti menunjukkan `model_ready: true`. Dokumentasi interaktif: `/docs`.

```powershell
curl.exe -X POST "http://127.0.0.1:8000/predict?threshold=0.7" -F "file=@dataset_public/test/BOTOL/049d99faa622b032.jpg"
```

Respons mengandungi `prediction`, `top_class`, `confidence`, `status`, `threshold`, `scores` dan SHA-256 `model_id`. UI menukar canvas kepada JPEG; ujian batch membaca imej asal. Perbezaan resampling boleh mengubah skor sedikit. Bandingkan eksperimen pada aliran preprocessing yang sama.

## Pengesahan

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe tools/check_dataset.py dataset_public
node --check static/script.js
node tests/test_camera.cjs
```

26 September 2026: **21 ujian Python lulus**, termasuk 90 inferens sebenar yang sepadan dengan keputusan E1/E2 terdahulu; **4 ujian logik kamera lulus**; lima semakan HTTP sebenar lulus. TFJS, Python, UNKNOWN dan fail CSV muat turun disahkan melalui UI. Bukti: [VERIFIKASI_26SEPT.md](evidence/VERIFIKASI_26SEPT.md). Workflow GitHub Actions menjalankan semakan yang sama; status run sebenar boleh dilihat pada tab Actions.

Untuk penilaian tambahan tanpa menimpa bukti asal:

```powershell
.\.venv\Scripts\python.exe tools/evaluate.py --data dataset_public/validation --experiment E2_RECHECK --out evidence/recheck
```

Jangan gunakan hasil test untuk menala semula model atau menulis hasil rekaan.

## Panduan penyerahan

- [Senarai padanan kehendak soalan](docs/SENARAI_SEMAK_PENYERAHAN.md)
- [Skrip demo dan jawapan 12 soalan lisan](docs/SKRIP_DEMO_DAN_SOAL_JAWAB.md)
- [Deployment dan GitHub](docs/DEPLOYMENT_DAN_GITHUB.md)
- [Rekod penggunaan AI](evidence/AI_LOG.md)
- [Sumbangan sebenar ahli](docs/SUMBANGAN_AHLI.md)

Laporan dan slaid dikecualikan daripada kerja serta pakej semasa. Rekod bertarikh lebih awal ialah sejarah; rujuk bukti 26 September untuk status terkini. Latihan demo dan pengesahan sumbangan mesti dibuat oleh ahli sebenar.

## Sumber teknikal dan lesen

- [Google LiteRT migration](https://developers.google.com/edge/litert/migration)
- [Teachable Machine library](https://github.com/googlecreativelab/teachablemachine-community/tree/master/libraries/image)
- [FastAPI file uploads](https://fastapi.tiangolo.com/tutorial/request-files/)
- [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/)

Library pihak ketiga dan lesen asal disimpan dalam `static/vendor`, bersama URL sumber dan SHA-256. Dataset mengikuti lesen sumber setiap imej; jangan anggap lesen library terpakai pada dataset. Screenshot latihan E1 yang mengandungi wajah webcam dikekalkan secara tempatan sahaja; bukti latihan E1 tanpa preview wajah disertakan.
