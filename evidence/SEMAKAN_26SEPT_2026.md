> Status selepas pembaikan 26 September 2026: rujuk VERIFIKASI_26SEPT.md. Catatan berikut dikekalkan sebagai sejarah/panduan proses.

# Semakan kesiapan projek 26 September 2026

Projek belum lengkap untuk penyerahan. Semakan ini mengecualikan laporan dan slaid. Sumber keperluan ialah C:/Users/Faris/Downloads/DKA3223 FA .docx, khususnya bahagian 2, 6, 8–12, 14, 16, 17 dan 19. Tiada kod, model atau keputusan eksperimen diubah dalam semakan ini.

## Padanan keperluan

| Keperluan | Status dan bukti |
|---|---|
| Skop, tujuan dan sekurang-kurangnya tiga kelas | Tersedia: BOTOL, BUKU, TELEFON; README dan halaman utama. |
| Dataset dan sumber | Tersedia: dataset_public, 210 imej unik; 50 latihan, 10 validation dan 10 test setiap kelas. Sumber/atribusi dalam evidence/public_dataset. Semakan hash tidak menemukan pendua tepat antara latihan dan holdout; ini tidak membuktikan tiada imej hampir sama. |
| Latihan Teachable Machine | Bukti eksport, metadata, konfigurasi dan screenshot E1/E2 tersedia. |
| Dua eksperimen dan perbandingan | Tersedia: E1 50 epoch, E2 100 epoch, data import sama. Validation E1 26/30, E2 27/30. evidence/validation/PERBANDINGAN.md dan MODEL_SELECTION.md. |
| Testing pada data baharu | Rekod tersedia: FINAL_E2 28/30 (93.33% top-1), CSV ramalan/confidence dan confusion matrix. Angka daripada rekod 24 September, bukan inferens yang berjaya diulang pada 26 September. |
| Eksport model akhir | TFJS dan TFLite tersedia. TFLite ialah hasil penukaran tempatan TFJS. Hash model E1/E2 dan imej validation/test sepadan dengan bukti; fail model aktif sepadan dengan E2. |
| Antaramuka dan fungsi asas | Kod untuk upload/kamera, kelas, confidence, status, threshold UNKNOWN dan reset tersedia. Bukti ujian UI 24 September tersedia; UI tidak diuji semula dalam semakan ini. |
| Python, FastAPI dan Pydantic | Kod lengkap, tetapi pemuatan model sebenar GAGAL dalam persekitaran semakan semasa. Lihat masalah utama di bawah. |
| Ujian kod | Diulang: 18 passed, 2 warnings, 21.51 saat. Test double digunakan dalam ujian kontrak; keputusan ini bukan bukti inferens model sebenar. |
| Git dan GitHub | Empat commit tempatan wujud, terakhir 23 September. git remote -v kosong. Banyak fail akhir belum di-commit; akses repository oleh penilai belum dibuktikan. |
| README dan cara menjalankan | Tersedia. Pernyataan lama bahawa mod Python siap perlu dibaca bersama masalah semasa ini. |
| Dua penggunaan AI dan bukti | AI_LOG mencatat beberapa penggunaan sebenar, tetapi masih ada placeholder semakan pelajar. Bukti prompt/hasil sebenar yang digunakan dan pengesahan pemahaman pelajar belum lengkap dalam pakej yang disemak. Dokumen tidak menyatakan dua perbualan berasingan wajib. |
| Peranan dan sumbangan ahli | Belum lengkap: bukti sumbangan sebenar setiap ahli belum disahkan. Commit oleh AI Assistant bukan bukti kerja semua ahli. |
| Demo individu | Skrip tersedia; pelaksanaan/penguasaan setiap ahli belum disahkan. |
| Deployment mengikut pensyarah | Implementasi tempatan tersedia tetapi mod Python gagal dalam semakan ini. URL awam tidak diwajibkan secara umum dalam dokumen; kaedah khusus pensyarah perlu dipatuhi. |
| Video demo | Hanya wajib jika diminta pensyarah; arahan tersebut belum diketahui. |
| ZIP penyerahan | TIDAK TERKINI: SmartVision_DKA3223.zip mempunyai 74 entri dan README bertarikh 23 September; tiada dataset_public, model TFLite, model.weights.bin, eksperimen E1/E2 atau keputusan validation/test akhir. |

## Masalah utama semasa

Percubaan menjalankan lifespan aplikasi melalui FastAPI TestClient dengan model sebenar menghasilkan model_ready: false. Import TensorFlow secara terus mengesahkan punca:

`ImportError: DLL load failed while importing _ml_dtypes_ext: An Application Control policy has blocked this file.`

Ini sekatan komponen runtime dalam persekitaran semakan, bukan bukti fail model hilang atau latihan gagal. Semakan POST /predict model sebenar tidak diteruskan selepas kegagalan pemuatan. Rekod lima semakan HTTP yang lulus pada 24 September kekal sebagai bukti sejarah. Persekitaran demo perlu membenarkan runtime yang diperlukan dan inferens perlu diuji semula; jangan memintas polisi keselamatan.

## Liputan 12 soalan lisan bahagian 16

Rujukan jawapan: docs/SKRIP_DEMO_DAN_SOAL_JAWAB.md.

| Soalan | Liputan |
|---|---|
| Classification berbanding detection | Jawapan khusus tersedia. |
| Mengapa beberapa kelas | Jawapan khusus tersedia. |
| Pengaruh dataset | Jawapan khusus tersedia. |
| Maksud confidence | Jawapan khusus tersedia. |
| Mengapa model tersalah klasifikasi | Diliputi secara tidak langsung melalui dataset, overfitting, had confidence dan dua contoh salah ramalan. Belum ada jawapan khusus yang dihimpunkan untuk soalan ini. |
| Overfitting | Jawapan khusus tersedia. |
| Fungsi CNN | Jawapan khusus tersedia. |
| Mengapa test berasingan | Jawapan khusus tersedia. |
| Integrasi model TM | Jawapan khusus tersedia. |
| FastAPI dan Pydantic | Jawapan khusus tersedia. |
| Kelebihan GitHub | Jawapan khusus tersedia. |
| Risiko menggunakan AI tanpa semakan | Jawapan khusus tersedia. |

ANN, transfer learning dan accuracy turut diterangkan. Bahan jawapan tersedia tidak membuktikan ahli sudah boleh menjawab secara lisan. Untuk soalan kesilapan model, jawapan yang sesuai ialah: model boleh belajar ciri latar atau rupa yang mengelirukan, data latihan mungkin kurang mewakili imej baharu, dan overfitting boleh mengurangkan generalisasi. Confidence tinggi masih boleh salah. Ini kemungkinan umum, bukan punca khusus yang telah dibuktikan bagi setiap imej salah projek ini.

## Kerja yang masih diperlukan

1. Selesaikan keserasian/kebenaran runtime pada mesin demo melalui kaedah yang dibenarkan, kemudian sahkan model_ready dan POST /predict dengan model sebenar.
2. Commit perubahan sebenar yang belum direkod, sediakan repository GitHub projek dan sahkan akses penilai. Jangan reka sejarah commit atau sumbangan ahli.
3. Lengkapkan bukti penggunaan AI dan sumbangan sebenar setiap ahli.
4. Lengkapkan pengesahan UI: kamera hidup/ditolak, Henti/Reset stream aktif, objek luar skop dan muat turun CSV. Webcam bukan syarat mutlak kerana soalan membenarkan upload dan/atau webcam; CSV ialah ciri tambahan aplikasi. Ujian ini diperlukan untuk mengesahkan semua ciri yang ditawarkan.
5. Jalankan demo setiap ahli dan latihan semua soalan lisan. Sahkan arahan deployment/video pensyarah jika ada.
6. Bina pakej penyerahan terkini selepas pembetulan. ZIP sekarang tidak mewakili projek akhir.
