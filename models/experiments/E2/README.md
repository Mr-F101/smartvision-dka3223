# Eksperimen E2 — model akhir

Dilaksanakan dalam Teachable Machine pada 24 September 2026. Tiga kelas mengikut susunan metadata: BOTOL, BUKU, TELEFON. Set import sama seperti E1: 50 imej setiap kelas, 150 keseluruhan. Parameter: 100 epoch, batch 16, learning rate 0.001. Seed dan split dalaman TM tidak dikawal.

Pautan eksport yang diterbitkan dengan kebenaran pengguna: https://teachablemachine.withgoogle.com/models/A8ibBF5HJ/

`tfjs` mengandungi model.json, metadata.json dan model.weights.bin yang dimuat turun daripada pautan tersebut. `tflite` mengandungi model_unquant.tflite dan labels.txt hasil tools/convert_tm_export.py tanpa latihan semula. Ini bukan muat turun TFLite melalui panel TM yang disahkan berjaya. Rekod penukaran dan semakan numerik ada dalam conversion.json; semakan itu bukan ukuran accuracy atau bukti kesetaraan terus dengan runtime TFJS.

SHA-256 TFLite: 642bbfea613d39935ae60e894124c7d2a958e8ee7d0bddc01da5f9f11de82a55.

API model_id (model + labels): 4860b5a9063c1153b4824ab0271e9f66094e2d5ad9c7ce8d3da15a9ee5e225c0.

Validation 27/30 (90.00%) pada threshold 0.7. Dipilih sebelum test; test akhir 28/30 (93.33%). Lihat evidence/MODEL_SELECTION.md dan evidence/testing/FINAL_E2.json untuk keputusan, coverage dan batasan. Accuracy dalaman TM tidak sama dengan validation/test projek.
