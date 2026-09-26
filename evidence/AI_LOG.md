# Penggunaan AI pada 26 September 2026

Rekod ini menyimpan prompt sebenar serta hasil yang digunakan. Alamat e-mel pengguna dikecualikan daripada salinan awam. Interaksi berlaku dalam task yang sama; tidak didakwa sebagai dua perbualan berasingan.

## Penggunaan 1 — audit projek

Prompt: “periksa adakah semuanya sudah siap dan menjawab semua soalan untuk project itu ( tidak termasuk laporan dan slide )”

Hasil yang digunakan: padanan dokumen DKA3223, semakan fail/model/dataset, ujian kod dan penemuan GitHub/ZIP lama serta masalah runtime. Jawapan utama AI: “Belum 100% siap”, dengan senarai kekurangan. Bukti terperinci: SEMAKAN_26SEPT_2026.md. Pelajar meminta pembaikan berdasarkan audit ini.

## Penggunaan 2 — pembaikan dan penyediaan GitHub

Prompt: “selesaikan semuanya secara menyeluruh ( kecualikan laporan dan slide ) … masukkan ke dalam github saya mengikut kehendak soalan”

Hasil yang digunakan: migrasi inferens kepada Google LiteRT rasmi, persediaan automatik, library TFJS tempatan, timeout kamera, model E1/E2 dalam Git, ujian regresi 90 inferens, bukti HTTP/UI/CSV dan jawapan soalan kesilapan model. Jawapan kemajuan AI menyatakan runtime memuat model, 18 ujian asal lulus, kemudian semakan diperluas kepada 21 ujian Python dan 4 ujian kamera simulasi. Lihat commit, VERIFIKASI_26SEPT.md dan GITHUB_DELIVERY.md untuk hasil akhir.

Semakan: ujian automatik dan UI dilakukan oleh ejen; pengguna log masuk ke akaun GitHub sendiri dan meminta “continue”. Ini bukan bukti semua ahli telah membaca atau memahami kod. Semakan pemahaman dan sumbangan ahli masih perlu disahkan dalam docs/SUMBANGAN_AHLI.md. Tiada kata laluan/token dimasukkan dalam bukti repository.

---

# Rekod penggunaan AI Code Assistant

## Penggunaan sebenar 24 September 2026

Prompt pengguna meminta menyelesaikan dataset baharu, eksport E1/E2, screenshot, integrasi, 18 ujian, laporan dan slaid, diikuti “continue”. Pengguna membenarkan dataset awam serta menjawab “Ya, benarkan pautan model” untuk penerbitan model TM.

Hasil: 210 imej Open Images dengan atribusi dan split bebas hash; latihan TM sebenar E1 50 epoch/E2 100 epoch; eksport TFJS dan penukaran TFLite tanpa latihan semula; validation E1 86.67%/E2 90.00%; test akhir E2 93.33% pada 30 imej. 18 ujian kod lulus, lima semakan HTTP live lulus, sebahagian ujian UI selesai. Kamera dan penerimaan CSV UI belum disahkan. Laporan/slaid dikemas kini berdasarkan bukti, bukan angka rekaan.

Ini penggunaan AI susulan dalam task yang sama. Dokumen tugasan menyebut sekurang-kurangnya dua kali/sesi, bukan secara jelas dua perbualan berasingan. Pelajar masih perlu menyimpan bukti prompt/jawapan, menerangkan kod dan mengesahkan sumbangan sendiri. Bantuan ejen tidak boleh dilabel sebagai kerja manual ahli yang tidak berlaku.

## Rekod sejarah di bawah

## Sesi 1 yang benar-benar berlaku

Tarikh: 23 September 2026. Alat: Codex. Permintaan pengguna: “bolehkah anda bantu saya siapkan tugasan ini secara keseluruhan mengikut kehendak project dan step by step yang berada di photo kedua itu”. Sumber: dokumen DKA3223 FA dan gambar tutorial.

Hasil bantuan: cadangan skop, kod HTML/CSS/JavaScript, backend FastAPI/Pydantic/TFLite, pengendalian input, skrip ujian, panduan eksperimen serta bahan laporan/pembentangan. Model terlatih, dataset dan ketepatan tidak dihasilkan atau didakwa tersedia.

Semakan pelajar yang masih perlu dibuat: fahami `format_prediction`, `preprocess`, endpoint `/predict`, pemuatan model dan gelung kamera. Jalankan aplikasi dengan model sendiri, simpan output serta screenshot perbualan ini. Nyatakan kod yang diterima, diubah atau ditolak. Rekod sumbangan sebenar anda di bawah:

[ISI pemahaman, perubahan dan ujian pelajar]

## Status sesi 2 pada rekod awal

### Interaksi susulan pembangunan dalam perbualan yang sama

Prompt sebenar: “selesaikan apa yang boleh anda selesaikan dan saya akan selesaikan apa yang perlu saya selesaikan mengikut kehendak anda untuk selesaikan tugas ini”.

Hasil: semakan semula kod, penambahan cap jari model dalam API, penjejakan dataset/model pada evaluation, alat perbandingan E1/E2 dengan pengesahan kesetaraan set ujian, tambahan ujian automatik dan senarai tindakan pelajar. Sebanyak 18 ujian automatik lulus selepas perubahan. Data sintetik dalam ujian perisian tidak digunakan sebagai bukti hasil eksperimen model.

Ini penggunaan susulan sebenar, masih dalam perbualan yang sama. Jika pensyarah menghendaki dua sesi/perbualan berasingan, keperluan itu masih perlu dilengkapkan. Simpan screenshot prompt dan jawapan, fahami perubahan serta tulis semakan pelajar sendiri.

Jalankan sesi kedua selepas mempunyai model atau hasil ujian. Contoh prompt yang boleh digunakan, **belum dikira bukti sesi**:

“Ini CSV keputusan E1 dan E2 serta contoh imej salah. Tolong analisis kesilapan, semak pengiraan accuracy dan cadangkan satu pembaikan. Jangan reka keputusan.”

Selepas sesi sebenar, isi tarikh, prompt tepat, ringkasan jawapan, fail berubah, semakan manual, ujian dan pautan/screenshot. Dua bahagian dalam fail ini tidak bermaksud dua sesi sudah berlaku.
