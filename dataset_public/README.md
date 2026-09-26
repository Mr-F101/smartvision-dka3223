# Dataset awam SmartVision — 24 September 2026

210 imej unik: BOTOL, BUKU dan TELEFON, 70 setiap kelas. Setiap kelas mempunyai 50 imej latihan, 10 validation dan 10 test. `train_e2` ialah salinan sengaja `train_e1`: E1/E2 membandingkan epoch 50/100, bukan pertambahan data. Batch size 16, learning rate 0.001. Hasil eksperimen hanya sah selepas latihan dan eksport sebenar.

Sumber: subset validation/test Open Images V7. Nama subset asal bukan split eksperimen SmartVision: pemisahan projek dibuat semula secara deterministik dan direkod dalam manifest. Gambar asal tidak diedit atau dijana. Penukaran/crop tengah oleh Teachable Machine semasa latihan ialah preprocessing, bukan sampel tambahan.

## Provenans dan lesen

Rujuk `../evidence/public_dataset/attribution.csv` untuk pengarang, tajuk, URL asal, lesen dan SHA-256 setiap imej; `manifest.json` menyimpan metadata terperinci. Metadata Open Images menyenaraikan imej terpilih sebagai CC BY 2.0. Ini bukan jaminan bahawa status setiap halaman asal telah diaudit semula. Kekalkan atribusi apabila mengedar gambar dan semak syarat asal sebelum penerbitan awam.

Sumber rasmi: https://storage.googleapis.com/openimages/web/download_v7.html dan https://storage.googleapis.com/openimages/web/factsfigures_v7.html . Lesen yang direkod: https://creativecommons.org/licenses/by/2.0/ . Anotasi Open Images mempunyai lesen berasingan daripada gambar.

## Semakan yang dilaksanakan

- Semakan visual contact sheet sebelum pemilihan. Contoh ditolak: tin/kotak minuman, balang, screenshot telefon tanpa peranti, GPS, PDA/toy yang mengelirukan, dan pemandangan bilik/orang yang tidak menunjukkan buku dengan jelas.
- Pemilihan buku turut mengandungi buku terbuka, komik, buku nota, terbitan berjilid, kumpulan buku dan konteks membaca; kelas ini bukan hanya satu buku bertutup di latar kosong. Sebahagian telefon ialah gambar produk berlatar seragam. Variasi dan domain bias ini mesti dinyatakan dalam laporan.
- 210 SHA-256, ImageID dan URL profil pengarang berbeza. Tiada hash/sumber pengarang merentasi train–validation–test; E1/E2 berkongsi train sahaja. Semakan hash tidak menjamin ketiadaan semua imej hampir serupa.
- Dataset lama `../dataset` dikekalkan untuk rekod pengguna tetapi mempunyai pendua merentasi split; jangan gunakan untuk keputusan accuracy akhir.

## Penggunaan

Muat naik 50 JPG daripada setiap folder `train_e1/<LABEL>` ke kelas Teachable Machine yang sepadan. ZIP disediakan sebagai kemudahan pemindahan sahaja; import ZIP dalam sesi pelayar ini tidak berjaya, manakala pemilihan JPG berjaya.

Jangan muat naik validation/test ke latihan. Pilih model berdasarkan validation yang sama untuk kedua-dua eksperimen. Gunakan test hanya selepas model dipilih. 30 imej test ialah sampel kecil; jangan menuntut generalisasi dunia sebenar atau prestasi webcam tanpa ujian tambahan.

Pengesahan: `.venv/Scripts/python.exe tools/check_dataset.py dataset_public`.
