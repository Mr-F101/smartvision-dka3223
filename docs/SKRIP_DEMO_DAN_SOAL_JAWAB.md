# Skrip demo dan persediaan soalan lisan

## Fakta yang perlu disebut — 24 September 2026

Dataset awam mempunyai 210 imej unik: 150 latihan, 30 validation dan 30 test. E1/E2 menggunakan 150 imej import sama; perubahan ialah 50 kepada 100 epoch, batch 16 dan learning rate 0.001 kekal. Random seed dan pembahagian dalaman TM tidak dikawal, jadi peningkatan tidak boleh dikaitkan dengan epoch sahaja.

Validation E1 ialah 26/30 (86.67%), E2 27/30 (90.00%). Pilih E2 sebelum membuka keputusan test. Test E2 ialah 28/30 (93.33%); satu buku diramal telefon pada confidence 64.96% lalu UNKNOWN, dan satu telefon diramal buku pada 89.74%. Confidence bukan jaminan betul. Ambang 70% tidak mengesan semua objek asing.

Model TFJS ialah eksport Teachable Machine sebenar. Model TFLite ditukar secara tempatan daripada eksport sama tanpa latihan semula; muat turun TFLite melalui panel TM tidak berjaya disahkan. Pautan model awam bukan URL deployment aplikasi.

Untuk demo yang sudah diuji, pilih mod Pelayar, `/models/tfjs/`, eksperimen E2 dan upload `dataset_public/test/BOTOL/049d99faa622b032.jpg`. Untuk UNKNOWN dalam mod Python, gunakan `dataset_public/test/BUKU/33040e3951cc688c.jpg`; UI sekitar 62.22%, berbeza sedikit daripada batch kerana preprocessing. Pulihkan threshold kepada 70% selepas demonstrasi.

## Latihan setiap ahli — belum dilakukan

Faris, AIEREL dan HAIRIS perlu menjalankan demo sendiri. Dokumen ini ialah persediaan, bukan bukti mereka telah berlatih. Setiap ahli perlu menerangkan sumbangan sebenar, menjalankan kedua-dua mod, menunjukkan satu salah ramalan, menjawab tiga soalan di bawah dan mencatat masa serta masalah. Sahkan nama penuh/matrik sebelum penyerahan. CSV dan objek luar skop telah diuji pada 26 September. Kamera fizikal masih memerlukan semakan mesin demo; logik penolakan/henti/reset telah diuji secara simulasi. Rujuk evidence/VERIFIKASI_26SEPT.md.

## Demo individu sekitar 7 minit

0:00–0:45: “Projek SmartVision mengklasifikasikan botol, buku dan telefon. Prototaip ini menggunakan Teachable Machine dan aplikasi web.” Terangkan masalah dan sumbangan sebenar anda.

0:45–1:45: Tunjukkan folder dataset dan label. Terangkan bilangan sebenar, sumber imej dan pemisahan train/validation/test. Tunjukkan konfigurasi serta bukti latihan E1/E2.

1:45–2:45: Tunjukkan jadual keputusan sebenar. Jelaskan perubahan E2 dan sebab memilih model akhir. Terangkan satu kesilapan sebenar, bukan contoh rekaan.

2:45–4:15: Jalankan aplikasi, muat model, gunakan webcam atau upload imej baharu. Baca label dan confidence. Ubah threshold untuk menerangkan UNKNOWN, kemudian reset. Cuba objek luar skop dan jelaskan had softmax.

4:15–5:15: Tukar ke mod Python, uji endpoint di /docs dan terangkan input, preprocessing, model serta JSON. Jika mod ini belum berfungsi, nyatakan dengan jujur dan selesaikan sebelum demo akhir.

5:15–6:15: Tunjukkan GitHub, commit dan bukti dua sesi AI sebenar. Terangkan satu fungsi kod tanpa membaca bulat-bulat.

6:15–7:00: Kesimpulan berdasarkan data, batasan dan cadangan menambah variasi dataset. Masa setiap individu ikut arahan pensyarah; dua jam dalam dokumen ialah tempoh keseluruhan penilaian.

## Jawapan konsep

**ANN:** rangkaian nod berparameter yang belajar memetakan input kepada output melalui latihan. Bobot dilaras untuk mengurangkan fungsi loss.

**CNN:** rangkaian yang menggunakan operasi convolution untuk mempelajari ciri spatial seperti tepi, tekstur dan bentuk. Ciri ini membantu klasifikasi imej.

**Transfer learning:** menggunakan ciri daripada rangkaian pralatih dan melatih pengelas untuk kelas baharu. Catat maklumat model eksport sebenar jika menerangkan backbone atau bentuk seni bina tertentu.

**Classification berbanding detection:** classification memberikan kategori untuk keseluruhan imej; detection turut menghasilkan lokasi objek seperti bounding box. Projek ini tidak melukis bounding box.

**Mengapa tiga kelas:** memenuhi skop tugasan dan membolehkan model belajar membezakan kategori. Satu kelas sahaja tidak memberi perbandingan kategori yang bermakna untuk prototaip ini.

**Confidence:** skor model bagi kelas, lazimnya output softmax. Ia bukan accuracy keseluruhan dan bukan jaminan kebarangkalian sebenar bahawa keputusan betul.

**Accuracy:** pecahan label ramalan yang betul pada set ujian berlabel. Nyatakan saiz sampel, set dan kaedah pengiraan.

**Overfitting:** model menyesuaikan diri terlalu kuat kepada ciri data latihan lalu kurang baik pada imej baharu. Variasi data, pemisahan set dan penilaian luaran membantu mengesannya.

**Mengapa dataset penting:** latar, pencahayaan, sudut dan ketidakseimbangan kelas boleh membentuk ciri salah yang dipelajari model. Lebih banyak imej hampir sama tidak semestinya memperbaiki generalisasi.

**Mengapa test berasingan:** mengukur kebolehan menghadapi data yang belum dilihat. Menguji pada imej latihan memberikan penilaian terlalu optimistik.

**Integrasi Teachable Machine:** eksport TF.js dibaca oleh tmImage.load dalam pelayar; eksport TFLite FLOAT dibaca interpreter Python. Keduanya perlu daripada versi model yang sama jika membandingkan aliran deployment.

**FastAPI dan Pydantic:** FastAPI menyediakan endpoint dan pengendalian HTTP. Pydantic menetapkan bentuk serta batas nilai respons JSON. Input fail multipart diterima melalui UploadFile.

**GitHub:** menyimpan kod, sejarah perubahan dan bukti kerjasama. Commit mesti mewakili kerja sebenar dan tidak menyimpan rahsia.

**Risiko AI Code Assistant:** kod mungkin salah, tidak serasi atau sukar difahami. Pelajar perlu membaca, menguji dan merekod bantuan dengan jujur.

**Mengapa model tersalah mengklasifikasikan imej:** imej baharu mungkin berbeza daripada data latihan; latar, sudut, pencahayaan dan rupa antara kelas boleh mengelirukan, manakala overfitting mengurangkan generalisasi. Ini kemungkinan umum, bukan punca khusus yang telah dibuktikan bagi setiap kes. Contoh sebenar: satu telefon test diramal BUKU pada 89.74%. Imej Bumi di luar skop pula diramal BOTOL 96.70% melalui API, menunjukkan confidence tinggi tidak menjamin kelas betul.

**Runtime terkini:** fail model kekal TFLite E2 yang sama; interpreter Python kini daripada Google LiteRT 2.2.0. Semua 90 ramalan regresi masih sepadan. Library JavaScript dan model disimpan tempatan untuk demo.
