# Skrip demo dan persediaan soalan lisan

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
