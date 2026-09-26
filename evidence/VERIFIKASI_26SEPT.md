# Verifikasi teknikal 26 September 2026

Model aktif E2 dapat dijalankan melalui FastAPI dan Pydantic dengan Google LiteRT 2.2.0. Pakej TensorFlow penuh sebelumnya gagal kerana komponen ml_dtypes disekat dalam persekitaran semakan. Polisi Windows tidak dinyahaktifkan; aplikasi kini menggunakan runtime inferens rasmi Google LiteRT.

## Ujian yang selesai

- Python pytest: 21 lulus, 2 amaran deprecation; 3 ujian integrasi mengulang 90 inferens sebenar (E1 validation, E2 validation, E2 test). Kelas, keputusan threshold dan confidence sepadan dengan CSV asal dalam toleransi 0.0001. Tiada latihan atau pemilihan semula menggunakan test.
- Node: 4 ujian lifecycle kamera lulus (penolakan, henti/reset, izin selepas reset, timeout/stream lewat). Ini simulasi kod, bukan bukti kamera fizikal.
- Semakan sintaks JavaScript lulus.
- Dataset: 50/50/10/10 setiap kelas bagi train_e1/train_e2/validation/test, tanpa pendua tepat antara latihan dan holdout.
- Live HTTP model sebenar: valid 200, kosong 400, rosak 400, lebih 8 MB 413, threshold luar julat 422. evidence/live_api_checks_26sept.json.
- UI TFJS menggunakan library dan model tempatan: BOTOL 99.9996185%; screenshot demo_tfjs_26sept.png.
- UI Python: imej buku 33040e3951cc688c.jpg menghasilkan calon TELEFON 62.2235%, lalu UNKNOWN pada threshold 70%.
- CSV UI benar-benar diterima dalam Downloads dan disalin tanpa mengubah hasil ke evidence/ui_export_26sept.csv. Baris E2, BOTOL, confidence 0.9999961853027344 disahkan.
- Ujian luar skop API dengan imej Bumi NASA: BOTOL 96.6985%. Ini kegagalan mengenal objek asing, bukan keputusan yang disembunyikan. UNKNOWN bukan jaminan novelty detection. Sumber dan JSON dalam evidence/out_of_scope.

- UI imej Bumi turut diuji: BOTOL 95.5536%; perbezaan berbanding API asal berpunca daripada aliran canvas/JPEG. Screenshot out_of_scope_26sept.png.
- Timeout kamera sebenar dalam pelayar kawalan disahkan selepas 15 saat; kawalan upload kembali aktif. Screenshot camera_timeout_26sept.png. Stream fizikal tidak tersedia.

## Had dan pengesahan manusia

Kamera fizikal dan demo setiap ahli belum dibuktikan. Pengendalian kamera diuji secara simulasi; upload imej sebenar memenuhi syarat alternatif input tugasan. Dua amaran ujian ialah deprecation Starlette/httpx dan AnyIO, bukan kegagalan. Dockerfile disediakan tetapi build Docker belum diuji. Bukti status GitHub dan semakan clone direkod dalam GITHUB_DELIVERY.md selepas penerbitan.

Laporan/slaid dikecualikan. evidence/SEMAKAN_26SEPT_2026.md ialah audit sebelum pembaikan; kekurangannya tidak patut dibaca sebagai status selepas pembaikan ini.
