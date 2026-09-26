> Status selepas pembaikan 26 September 2026: rujuk VERIFIKASI_26SEPT.md. Catatan berikut dikekalkan sebagai sejarah/panduan proses.

# Status integrasi 23 September 2026

## Kemas kini 24 September 2026 — status semasa

Dataset_public mengandungi 210 imej unik: 50 latihan + 10 validation + 10 test setiap kelas. E1/E2 menerima latihan sama, 50/100 epoch, batch 16, learning rate 0.001. Eksport TM TFJS sebenar dan TFLite hasil penukaran tempatan tersedia dalam models/experiments. TFLite bukan muat turun panel TM yang berjaya disahkan.

E1: https://teachablemachine.withgoogle.com/models/v5ZQtNpgc/ . E2: https://teachablemachine.withgoogle.com/models/A8ibBF5HJ/ . Pengguna membenarkan pautan model awam; ini bukan deployment aplikasi FastAPI.

Validation E1 26/30 (86.67%), E2 27/30 (90.00%). E2 dipilih sebelum test; test E2 28/30 (93.33%). Bukti lengkap dalam validation, testing dan MODEL_SELECTION.md. E2 dipasang dalam models/tfjs dan models/tflite. Model asal disalin ke models/original_user tanpa memadam fail asal.

18 ujian kod dan lima semakan HTTP model sebenar lulus. UI load, upload, ralat imej, reset dan UNKNOWN diuji; lihat UJIAN_MANUAL_24SEPT.md untuk had. Screenshot latihan dan demo tersedia. Slaid edisi 24SEPT dirender dan disemak; laporan edisi 24SEPT masih menunggu render jika Word belum dibenarkan. Fail lama ialah draf sejarah.

Baki penyerahan: kamera/penolakan kamera, objek luar skop, penerimaan CSV UI, nama/matrik ahli, tarikh, GitHub, arahan deployment pensyarah dan latihan demo ahli. Tiada jaminan markah.

## Rekod sejarah berikut bukan status semasa

Eksport pengguna telah dipasang tanpa mengubah fail asal:

- TensorFlow.js daripada Downloads/tm-my-image-model.zip ke models/tfjs: metadata.json, model.json dan weights.bin.
- TensorFlow Lite daripada models/tflite/converted_tflite (1) ke models/tflite: model_unquant.tflite dan labels.txt.

Label eksport kekal Class 1, Class 2 dan Class 3. Pemetaan kepada BOTOL, BUKU dan TELEFON belum disahkan daripada projek latihan. Eksport ini tidak ditandakan sebagai E1 atau E2 kerana asal eksperimennya belum diketahui.

## Semakan yang dilaksanakan

18 ujian kod lulus semula menggunakan .venv/Scripts/python.exe -m pytest -q -p no:cacheprovider --tb=short. Terdapat 9 amaran deprecation; tiada kegagalan ujian.

Server sementara dijalankan di http://127.0.0.1:8001 kerana port 8000 sedang digunakan. GET /health melaporkan model_ready: true dan model_id 1ab78c6a1d2dbeb811a6b247a09aa468821aef53489533272a7d492ceb48897b.

POST /predict?threshold=0.7 dengan dataset/train_e1/BUKU/6167844595413226806.jpg menghasilkan prediction Class 2, confidence 1.0 dan status recognized melalui HTTP. Ini ialah semakan integrasi pada imej sedia ada, bukan pengukuran accuracy atau ujian akhir berasingan.

Halaman aplikasi dapat dibuka dalam pelayar aplikasi. Kejayaan pemuatan TF.js, upload melalui UI, webcam, reset dan eksport CSV belum disahkan dalam sesi ini.

## Keperluan asal yang disahkan

Dokumen Downloads/DKA3223 FA .docx menyatakan deployment mengikut kaedah pensyarah; URL awam tidak dinyatakan sebagai syarat umum. Penggunaan AI sekurang-kurangnya dua kali/sesi perlu didokumentasikan. Dokumen tidak menyatakan dua perbualan berasingan wajib.

## Perkara yang menghalang penyerahan akhir

- Chrome pengguna tidak tersedia dalam sambungan kawalan; hanya pelayar dalam aplikasi dapat dikesan.
- Dataset masih enam imej unik yang disalin ke semua split, termasuk validation dan test.
- Eksport E1 dan E2 berasingan serta rekod latihan belum tersedia.
- Pengguna memaklumkan lokasi data tambahan, identiti ahli, tarikh penyerahan dan arahan hos awam belum diketahui.
- Laporan dan slaid masih draf. Keputusan eksperimen dan sumbangan ahli tidak boleh diisi sebelum bukti tersedia.

Langkah seterusnya: sambungkan Chrome dengan projek Teachable Machine terbuka, sediakan gambar baharu atau pilih dataset awam berlesen, kemudian latih dan nilai dua eksperimen. Latihan pembentangan individu perlu dilakukan bersama ahli sebenar.
