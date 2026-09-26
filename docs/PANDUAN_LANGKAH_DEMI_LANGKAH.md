> Status selepas pembaikan 26 September 2026: rujuk ../evidence/VERIFIKASI_26SEPT.md. Catatan berikut dikekalkan sebagai sejarah/panduan proses.

# Panduan lengkap projek DKA3223

Panduan ini menyambungkan kehendak dokumen tugasan kepada 12 fasa dalam gambar. Mulakan dengan persediaan data kerana gambar menganggap model sudah dilatih. Kod siap berada dalam folder aplikasi, tetapi anda perlu melatih model menggunakan imej sebenar.

## A Persediaan sebelum Fasa 1

### A1 Masalah dan skop

SmartVision memerlukan prototaip yang mengenal pasti kategori objek melalui imej. Pilih Skop A: BOTOL, BUKU, TELEFON. Letakkan satu objek dominan dalam setiap imej. Ini image classification, bukan object detection atau pengiraan objek.

Objektif: membina model tiga kelas, menguji generalisasi pada imej baharu, membandingkan dua eksperimen dan mengintegrasikan model ke dalam aplikasi pelayar serta Python.

### A2 Kumpul data yang sah

Ambil gambar objek milik sendiri. Elakkan muka, nombor telefon, dokumen peribadi dan paparan telefon yang mengandungi maklumat peribadi. Gunakan beberapa botol, beberapa buku dan beberapa telefon jika tersedia. Ambil sudut depan/sisi/atas, jarak berbeza, latar meja polos serta latar lain, cahaya terang dan sederhana. Jangan ambil semua botol dengan latar yang sama tetapi semua buku dengan latar lain.

Pelan sampel yang dicadangkan, **belum dikumpulkan**:

| Set | BOTOL | BUKU | TELEFON | Kegunaan |
|---|---:|---:|---:|---|
| train_e1 | 50 | 50 | 50 | Baseline |
| train_e2 | 100 | 100 | 100 | E1 ditambah variasi |
| validation | 20 | 20 | 20 | Banding E1/E2 dan pilih model |
| test | 20 | 20 | 20 | Penilaian akhir selepas pemilihan |

E2 boleh mengandungi 50 imej E1 dan 50 imej tambahan setiap kelas. Ini memerlukan 140 imej unik setiap kelas, 420 keseluruhan. Cadangan ini melebihi minimum tiga kelas dan cadangan 50–100 imej latihan setiap kelas. Jika jumlah sebenar berbeza, rekodkan dengan jujur.

Pisahkan mengikut sesi pengambilan dan, jika boleh, objek fizikal. Jangan letak bingkai hampir sama daripada rakaman webcam dalam train dan test. Set validation dan test tidak dimuat naik untuk training. Validation dalaman Teachable Machine berbeza daripada set validation luaran yang anda sediakan.

### A3 Susun folder dan rekod sumber

Gunakan `dataset/train_e1/BOTOL`, `dataset/train_e2/BOTOL`, `dataset/validation/BOTOL`, `dataset/test/BOTOL` dan ulang untuk dua label lain. Isi `evidence/dataset_sources.csv`. Jalankan `python tools/check_dataset.py dataset`. Semakan hash mengesan pendua tepat sahaja; semak gambar hampir sama secara manual.

### A4 Latih E1

1. Buka https://teachablemachine.withgoogle.com/train/image.
2. Pilih Image Project, Standard image model.
3. Wujudkan tiga kelas dengan ejaan tepat BOTOL, BUKU, TELEFON.
4. Upload 50 imej bagi setiap kelas dari train_e1 sahaja.
5. Dalam Advanced, cadangan permulaan ialah epochs 50, batch size 16, learning rate 0.001. Jika pilihan berbeza, catat nilai sebenar yang dipaparkan.
6. Tekan Train Model, tunggu sehingga selesai dan simpan tangkapan skrin konfigurasi serta hasil latihan.
7. Simpan projek sumber, eksport E1 dan rekod tarikh/konfigurasi dalam `evidence/experiments.csv`.

### A5 Latih E2

Ulang dalam projek E2 dengan 100 imej setiap kelas. Kekalkan parameter latihan E1 agar perbandingan memfokuskan perubahan jumlah dan variasi data. Simpan kedua-dua versi secara berasingan. Anda tidak boleh menyatakan eksperimen lebih baik sebelum mengukur hasilnya.

### A6 Banding dan pilih model

Gunakan set validation luaran yang sama untuk E1 dan E2. Rekod label sebenar, top class, confidence dan sama ada diterima pada threshold 0.70. Gunakan fungsi CSV aplikasi atau `tools/evaluate.py`. Pilih berdasarkan accuracy validation, keseimbangan antara kelas dan analisis kesilapan. Freeze pilihan model dan threshold, kemudian nilai sekali pada test akhir. Jika mengubah model berdasarkan test akhir, kumpul set test baharu untuk penilaian akhir yang adil.

Accuracy top-1 = bilangan top_class betul / jumlah imej. Coverage = bilangan confidence melepasi threshold / jumlah imej. Accuracy diterima = ramalan diterima yang betul / bilangan diterima. Jika tiada yang diterima, accuracy diterima tidak ditakrifkan. UNKNOWN tidak dianggap ramalan kelas yang betul untuk imej tiga kelas.

## Fasa 1 Eksport model

Pilih model selepas perbandingan. Klik Export Model → TensorFlow.js → Upload my model. Salin URL penuh berakhir `/`. Simpan URL dan versi model dalam `evidence/model_registry.csv`. Atau Download my model dan ekstrak semua fail ke `models/tfjs`. Simpan eksport E1 dan E2 dalam arkib berasingan supaya perbandingan boleh diulang.

## Fasa 2 Aplikasi asas

Fail HTML, JavaScript dan CSS yang ditunjukkan dalam gambar disediakan dalam `static/`. Jalankan arahan setup README. FastAPI menyediakan halaman pada localhost. Mulakan dengan mod Pelayar; backend inferens hanya dipasang pada Fasa 12.

## Fasa 3 Sambungkan library dan URL

`index.html` memuat TensorFlow.js dan library Teachable Machine. Dalam aplikasi, tampal URL ke ruangan model. Untuk fail tempatan gunakan `/models/tfjs/`. Jangan tampal URL projek editor. Model URL mesti menunjukkan direktori yang mengandungi model.json dan metadata.json.

## Fasa 4 Muatkan model

Tekan Muatkan model. `tmImage.load()` membaca model.json, metadata.json dan fail weights yang dirujuk oleh model.json. Tunggu status Model tersedia. Jika gagal, periksa URL, internet dan nama fail weights. Model memerlukan minimum tiga kelas.

## Fasa 5 Sambungkan webcam

Tekan Buka kamera, kemudian Allow dalam dialog pelayar. Kamera memerlukan localhost atau HTTPS. Pastikan aplikasi lain tidak menggunakan kamera. Kamera tidak merakam video ke fail.

## Fasa 6 Ambil frame

JavaScript mengambil stream menggunakan getUserMedia dan melukis bahagian tengah frame pada canvas. Preview menunjukkan crop yang digunakan. Letakkan keseluruhan objek di dalam bingkai, satu objek setiap kali.

## Fasa 7 Prediction

Dalam mod Pelayar, `model.predict(canvas)` menghasilkan skor setiap kelas. Skor tertinggi menjadi top_class. UI menyusun skor dan menggunakan threshold untuk menentukan prediction. Gelung inferens mengelakkan permintaan bertindih.

## Fasa 8 Semak hasil pertama

Tunjuk botol, buku dan telefon secara berasingan. Semak kelas dan confidence berubah. Simpan tangkapan skrin sebenar dalam `evidence/screenshots`. Jangan gunakan contoh peratus dalam tutorial sebagai hasil projek. Cuba sudut atau latar baharu dan rekod contoh salah.

## Fasa 9 Upload imej

Tekan Muat naik imej dan pilih JPEG, PNG atau WebP. Had fail 8 MB, resolusi 16 megapiksel. Kamera dihentikan sebelum upload. Isi label sebenar tepat seperti model, pilih E1/E2, tekan Simpan rekod semasa dan eksport CSV. CSV perlu dieksport sebelum tab ditutup.

## Fasa 10 UI dan UX

UI sudah merangkumi nama dan tujuan aplikasi, preview, webcam/upload, prediction, confidence meter, skor semua kelas, status, reset dan paparan mudah alih. Semak saiz skrin telefon dan laptop. Uji juga butang tanpa model, fail rosak dan kamera ditolak.

## Fasa 11 Threshold

Default 70% mengikut gambar. `confidence >= 0.70` memaparkan kelas. Di bawahnya memaparkan UNKNOWN dan calon tertinggi. Slider membolehkan demonstrasi kesan threshold. Untuk eksperimen perbandingan, kekalkan threshold yang sama. Cuba objek luar skop seperti pen; ia masih mungkin menerima confidence tinggi. Terangkan had ini kepada penilai.

## Fasa 12 FastAPI dan deployment

1. Eksport model terpilih sekali lagi sebagai TensorFlow Lite FLOAT/unquantized.
2. Salin model_unquant.tflite dan labels.txt ke models/tflite.
3. Pasang requirements-model.txt menggunakan Python 3.12 64 bit dalam virtual environment.
4. Mulakan semula server, semak `/health`.
5. Pilih mod Python dalam UI dan tekan Muatkan model.
6. Cuba upload dan webcam. Imej akan dihantar ke server, dipraproses dan dinilai oleh model sebenar.
7. Buka `/docs`, pilih POST /predict, Try it out, masukkan fail dan Execute. Simpan bukti status 200 dan JSON sebenar.
8. Jalankan ujian batch dengan `tools/evaluate.py` dan simpan output.
9. Lengkapkan GitHub serta laporan. Jika URL awam diperlukan, rujuk panduan deployment.

## Jadual kerja satu minggu

Hari 1: skop, label dan pengumpulan awal. Hari 2: lengkap dan semak dataset. Hari 3: training E1/E2. Hari 4: validation, pemilihan, eksport dan integrasi. Hari 5: test akhir, UI, API dan pembaikan. Hari 6: laporan, slaid, GitHub dan bukti AI. Hari 7: latihan demo individu dan semakan penyerahan.

## Senarai semak sebelum hantar

- [ ] Kelas minimum tiga dan dataset sah tersedia.
- [ ] Eksport serta bukti latihan E1 dan E2 disimpan.
- [ ] Set ujian berasingan, keputusan serta kesilapan direkodkan.
- [ ] Model sebenar berjalan dalam pelayar dan endpoint Python.
- [ ] Repository GitHub boleh diakses penilai, commit sebenar tersedia.
- [ ] Dua sesi AI sebenar direkodkan, bukan dua prompt rekaan.
- [ ] Semua [ISI] dalam laporan/slaid diganti dengan maklumat sebenar.
- [ ] Laporan maksimum 15 muka surat selepas diedit.
- [ ] Setiap ahli boleh demo dan menjawab soalan sendiri.

Bahagian yang memerlukan tindakan anda: objek dan dataset sebenar, latihan E1/E2, butiran pelajar, akaun GitHub, sesi AI kedua dan bukti demo. Panduan ini tidak menggantikan bukti tersebut.
