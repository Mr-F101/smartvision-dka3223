# Pemilihan model sebelum ujian akhir

Tarikh: 24 September 2026. Sumber: validation/E1.json dan validation/E2.json. Pemilihan dibuat sebelum menilai dataset_public/test.

Model dipilih: **E2**, ID `4860b5a9063c1153b4824ab0271e9f66094e2d5ad9c7ce8d3da15a9ee5e225c0`. Threshold dikekalkan **0.70**.

Pada validation 30 imej yang sama, E1 mencapai 26/30 (86.67%) top-1, E2 27/30 (90.00%). E2 membetulkan satu tambahan BOTOL. Kedua-dua model mendapat 8/10 BUKU dan 10/10 TELEFON. E2 dipilih berdasarkan top-1 lebih tinggi; kelebihannya hanya satu imej, bukan bukti peningkatan statistik yang kukuh.

Trade-off: coverage E1 29/30, E2 28/30. Jumlah ramalan diterima yang betul sama, 25/30. Accuracy antara yang diterima E1 25/29 (86.21%), E2 25/28 (89.29%). UNKNOWN bukan jaminan mengesan objek asing.

E1/E2 menerima 150 imej import yang sama, batch 16 dan learning rate 0.001. Epoch E1 50, E2 100. Pembahagian dalaman dan inisialisasi TM tidak dikawal dengan seed; jangan mendakwa epoch sahaja terbukti menyebabkan perubahan. Percubaan E2 terdahulu terputus sebelum eksport dan tidak digunakan dalam perbandingan.

Pautan E1: https://teachablemachine.withgoogle.com/models/v5ZQtNpgc/

Pautan E2: https://teachablemachine.withgoogle.com/models/A8ibBF5HJ/

Eksport tempatan dalam models/experiments/E1 dan E2 ialah rujukan versi tetap. TFLite ditukar secara tempatan daripada TFJS tanpa latihan semula; butiran parity dan SHA-256 dalam conversion.json setiap eksperimen.
