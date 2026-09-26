# Penerbitan GitHub yang disahkan

Tarikh: 26 September 2026.

- Repository awam: https://github.com/Mr-F101/smartvision-dka3223
- Pemilik: Mr-F101; nama paparan muhdFaris. Pengguna log masuk sendiri dan meluluskan penerbitan awam secara jelas.
- Branch: main. Push pertama berjaya; kod yang disahkan ialah commit 2c6f91cb78188b9e764a221a0b87e5253f77d2f0.
- GitHub Actions: SUCCESS pada https://github.com/Mr-F101/smartvision-dka3223/actions/runs/36247215924 . Workflow memasang kebergantungan pada Ubuntu/Python 3.12 dan menjalankan smoke test model, semakan dataset, pytest serta ujian JavaScript.
- Clone baharu daripada GitHub berjaya; menggunakan runtime Python tempatan yang telah dipasang, tools/verify_install.py lulus, 21 ujian Python lulus (termasuk 90 inferens model sebenar) dan 4 ujian lifecycle kamera simulasi lulus.
- Clone tempatan berasingan juga mengesahkan checksum library dan tiada pendua tepat merentasi split dataset.
- Screenshot repository: screenshots/github_published_26sept.png.

Model aktif, eksport E1/E2, dataset, metadata atribusi, keputusan validation/test dan bukti UI/API disertakan dalam Git. Repository awam boleh dibaca tanpa akaun penilai. Tiada token/password dimasukkan dalam fail projek; semakan pola kelayakan pada fail penyerahan tidak menemui padanan.

ZIP SmartVision_DKA3223.zip di folder induk dibina daripada git archive main selepas dokumentasi ini di-commit. ZIP tidak mengandungi .git, .venv, laporan, slaid atau screenshot webcam E1 yang mengandungi wajah. Salinan ZIP lama disimpan secara tempatan dalam .build. Commit sejarah sebelum skop pengecualian ini dikekalkan, termasuk sejarah fail draf yang pernah direkod; fail laporan/slaid tidak berada dalam pokok main semasa.

Sumbangan AIEREL/HAIRIS dan latihan demo individu masih memerlukan pengesahan ahli. Kamera fizikal pada mesin pembentangan belum disahkan; pengendalian timeout sebenar serta lifecycle simulasi sudah diuji. Upload imej sebenar memenuhi syarat input alternatif tugasan.
