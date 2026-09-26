# Eksperimen E1

Model dilatih dalam Google Teachable Machine: 50 imej import setiap kelas, 50 epoch, batch 16, learning rate 0.001. Label BOTOL, BUKU, TELEFON. Teachable Machine menggunakan pembahagian dalaman 85/15 daripada imej import; 150 imej import bukan semuanya digunakan untuk kemas kini bobot. Paparan dalaman selepas latihan menunjukkan 8/8 betul setiap kelas. Itu bukan set validation/test projek.

Eksport asal TFJS dimuat turun daripada https://teachablemachine.withgoogle.com/models/v5ZQtNpgc/ . Metadata timestamp: 2026-09-24T00:19:50.219Z. Arkib tempatan ialah rujukan versi E1 yang tetap; pautan hos berpotensi berubah jika pemilik mengemas kini model.

`tflite/` ialah penukaran tempatan daripada eksport TFJS sebenar, bukan fail yang berjaya dimuat turun daripada panel TFLite TM. Panel penukaran awan selesai tetapi fail muat turun tidak dapat disahkan dalam pelayar. `tools/convert_tm_export.py` memindahkan 263 tensor float32 dengan padanan nama dan menukar format melalui TensorFlow 2.20.0 / tf-keras 2.20.1. Tiada latihan tempatan atau perubahan bobot. Semakan Keras–TFLite pada 3 imej latihan direkod dalam conversion.json; ia bukan ujian accuracy atau bukti parity TFJS bebas.

Validation luaran melalui API: 26/30 top-1 betul (86.67%), threshold 0.70, coverage 29/30. Rujuk evidence/validation/E1.json dan E1.csv untuk ramalan, hash imej dan ID model. Test akhir belum dijalankan pada waktu rekod ini ditulis.

Screenshot sebenar: evidence/screenshots/E1_training_complete.png, E1_internal_metrics.png, E1_export_link.png. Screenshot latihan mungkin mengandungi bingkai webcam terakhir. Jangan terbitkan screenshot yang mengandungi wajah tanpa semakan pemilik.
