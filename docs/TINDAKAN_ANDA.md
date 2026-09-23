# Tindakan anda untuk melengkapkan projek

Kod, alat penilaian, panduan, draf laporan dan slaid sudah disediakan. Anda tidak perlu menulis semula kod atau mengira keputusan secara manual. Saya boleh menyambung integrasi, ujian dan penulisan hasil apabila data/model sebenar tersedia.

## Buat sekarang

### 1 Ambil gambar objek

Sediakan BOTOL, BUKU dan TELEFON. Gunakan beberapa objek fizikal jika boleh, contohnya botol dengan bentuk berlainan dan buku berlainan kulit. Ambil satu objek dominan dalam satu gambar. Pastikan skrin telefon tidak mengandungi maklumat peribadi.

Untuk setiap kelas, sasarkan 140 gambar unik:

| Kumpulan gambar | Bilangan setiap kelas | Tujuan |
|---|---:|---|
| Latihan awal | 50 | E1 |
| Tambahan latihan | 50 | Digabungkan dengan 50 E1 untuk E2 |
| Validation luaran | 20 | Membandingkan E1 dan E2 |
| Test akhir | 20 | Mengukur model terpilih |

Jumlah keseluruhan ialah 420 gambar unik. Angka ini ialah pelan yang dicadangkan, bukan syarat minimum wajib dalam dokumen. Dokumen mencadangkan 50–100 imej latihan setiap kelas. Jika jumlah ini sukar, beritahu jumlah yang mampu disediakan supaya pelan boleh disesuaikan tanpa mereka data.

Variasikan sudut depan, sisi dan atas, jarak dekat/sederhana, cahaya serta latar. Set validation dan test hendaklah diambil dalam sesi berasingan, dan gunakan objek fizikal berbeza jika tersedia. Jangan pecahkan foto berturutan yang hampir sama antara latihan dan ujian.

### 2 Simpan dalam folder yang disediakan

Dalam folder SmartClassifier/dataset terdapat empat set, setiap satu mempunyai folder BOTOL, BUKU dan TELEFON:

```text
dataset/
  train_e1/     50 gambar setiap kelas
  train_e2/     100 gambar setiap kelas, termasuk salinan 50 E1
  validation/   20 gambar baharu setiap kelas
  test/         20 gambar baharu lain setiap kelas
```

Salinan E1 di E2 dibenarkan kerana kedua-duanya data latihan. Jangan salin mana-mana gambar latihan ke validation atau test. Jika sukar menyusun, berikan gambar mengikut kelas dan sesi pengambilan; saya boleh membantu menyusunnya. Penamaan contoh: BOTOL_sesi1_001.jpg.

### 3 Berikan maklumat yang masih belum ada

- Nombor matrik AIEREL dan HAIRIS serta nama penuh jika ejaan yang diberi belum lengkap.
- Tarikh penyerahan.
- Sumber gambar dan siapa yang mengambilnya.
- Sumbangan sebenar setiap ahli. Cadangan peranan dalam laporan belum dianggap sumbangan yang telah dibuat.
- Jika pensyarah menentukan hos deployment atau mewajibkan URL awam, berikan arahan tersebut.

### 4 Maklumkan apabila data tersedia

Beritahu lokasi folder atau lampirkan ZIP dataset. Contoh mesej:

“Dataset sudah tersedia di [lokasi]. Tolong semak pembahagian, bantu latihan E1/E2 dan sambung integrasi serta penilaian projek.”

Jangan hantar kata laluan, token atau API key. Jika login diperlukan, lakukan sendiri pada halaman rasmi.

## Selepas data tersedia

Saya boleh menyemak jumlah/pendua, membantu proses latihan Teachable Machine, menyambungkan eksport, menjalankan penilaian E1/E2 dan test akhir, serta memasukkan hasil sebenar ke laporan dan slaid. Langkah platform yang memerlukan interaksi anda akan diberitahu pada ketika itu. Anda tetap perlu memahami proses training dan kod untuk penilaian individu.

Jika anda melatih model terlebih dahulu, simpan untuk kedua-dua E1 dan E2:

1. Projek sumber Teachable Machine dan screenshot label, jumlah imej serta parameter latihan.
2. Eksport TensorFlow.js lengkap atau URL model.
3. Eksport TensorFlow Lite jenis FLOAT/unquantized, dengan labels.txt.
4. Catatan tarikh dan perubahan antara E1 dengan E2.

Jangan hanya memberi satu model akhir kerana tugasan memerlukan perbandingan dua eksperimen.

## Sebelum penyerahan

Anda perlu login GitHub apabila diperlukan, menyemak akses penilai, menyimpan screenshot perbualan AI sebenar, mengesahkan sumbangan ahli dan menjalankan demo individu. Jika pensyarah mentakrifkan dua sesi AI sebagai dua perbualan berasingan, lakukan satu sesi berasingan lagi. Interaksi penambahbaikan sekarang direkodkan dengan jujur dalam AI_LOG.md tetapi tidak disamarkan sebagai perbualan baharu.

Laporan dan slaid kekal draf sehingga data, keputusan, bukti dan identiti lengkap. Jangan mengisi nombor accuracy secara anggaran.
