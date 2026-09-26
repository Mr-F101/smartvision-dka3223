# Ujian aplikasi sebenar 24 September 2026

Model E2, aplikasi http://127.0.0.1:8002, Codex In-app Browser. Chrome pengguna tidak tersedia. Rekod ini berasingan daripada 18 ujian kod dan evaluation model.

| ID | Senario | Hasil sebenar | Status |
|---|---|---|---|
| UI01 | Model tiada | /models/not-present/ memaparkan ralat fail model tidak ditemui | PASS |
| UI02 | Kamera dibenarkan | Menunggu tanpa preview; reset membatalkannya | BLOCKED |
| UI03 | Kamera ditolak | Prompt penolakan tidak tersedia untuk dikawal | NOT RUN |
| UI04 | Upload TFJS | 049d99faa622b032.jpg menjadi BOTOL, confidence 0.9999961853 | PASS |
| UI05 | Fail rosak | invalid_image.jpg: The source image cannot be decoded; kawalan kembali tersedia | PASS |
| UI06 | Reset | Preview dan ramalan dibersihkan; membatalkan kamera menunggu | PASS bagi keadaan diuji; stream aktif belum disahkan |
| UI07 | UNKNOWN | Python, 33040e3951cc688c.jpg: TELEFON 62.22%, UNKNOWN pada 70%; diterima pada 50%; dipulihkan kepada 70% | PASS |
| UI08 | Objek luar skop | Belum diuji pada aplikasi akhir | NOT RUN |
| UI09 | Rekod dan CSV | Dua rekod disimpan; butang Eksport CSV (2); fail muat turun belum dapat disahkan | PARTIAL |
| UI10 | Load Python | model_ready true; UI upload dan inferens berjaya | PASS |

Bukti: screenshots/demo_tfjs_botol.png dan demo_api_unknown.png. Lima semakan HTTP live automatik (bukan manual UI) lulus dalam live_api_checks.json: imej sah 200, kosong 400, rosak 400, lebih 8 MB 413, threshold 1.1 menghasilkan 422. CSV evaluation model tersedia walaupun muat turun CSV UI belum disahkan.

UI crop ke canvas 400x400/JPEG; batch API menerima imej asal. Perbezaan skor bukan perbandingan preprocessing yang sama.

Baki ahli: uji kamera, Henti/Reset ketika stream aktif, kebenaran ditolak, objek luar skop dan fail CSV dalam Chrome. Catat hasil sebenar, bukan PASS andaian.
