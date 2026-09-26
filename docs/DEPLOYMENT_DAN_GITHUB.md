# Deployment dan GitHub

## Deployment tempatan

Jalankan SETUP.bat diikuti MULA.bat. Buka http://127.0.0.1:8000 dan sahkan /health menunjukkan model_ready: true. Model E2, label, TFJS dan library JavaScript tempatan disertakan. Python menggunakan Google LiteRT 2.2.0, bukan pakej TensorFlow penuh. Kejayaan HTTP inferens sebenar direkod dalam evidence/live_api_checks_26sept.json.

Dokumen tugasan mensyaratkan deployment mengikut pensyarah, bukan URL awam secara umum. Localhost menyediakan aplikasi/API untuk demo. URL model Teachable Machine dan URL repository GitHub bukan URL aplikasi Python.

## Docker pilihan

```sh
docker build -t smartvision-classifier .
docker run --rm -p 8000:8000 smartvision-classifier
```

Dockerfile disediakan; build Docker belum disahkan pada mesin ini. Ia menggunakan Python 3.12 dan LiteRT. Untuk hosting, tetapkan PORT dan HTTPS jika menggunakan kamera. Deployment awam perlu mengikut hos/arahan pensyarah. Jangan gunakan --reload untuk production; aplikasi pendidikan ini tidak menyediakan autentikasi atau rate limiting untuk pengguna umum.

## Repository dan sejarah kerja

Repository awam: https://github.com/Mr-F101/smartvision-dka3223 . Push, clone dan GitHub Actions sudah disahkan berjaya; lihat evidence/GITHUB_DELIVERY.md.

Sejarah commit tempatan 23 September dikekalkan. Commit 26 September mewakili pembaikan runtime, bukti/model sebenar dan penyediaan penyerahan. Tarikh dan sumbangan tidak direka. Commit bantuan AI bukan bukti semua ahli menulis kod sendiri.

Model E1/E2 dan dataset aktif dimasukkan terus dalam Git; pengguna clone tidak perlu mengambil model daripada komputer Faris. Fail runtime .venv, rahsia, dataset lama, eksport asal tidak digunakan dan screenshot webcam E1 tidak ditambah. Laporan/slaid tempatan tidak dikemas kini.

```sh
git clone https://github.com/Mr-F101/smartvision-dka3223.git
cd smartvision-dka3223
git log --oneline --decorate
```

Setiap ahli perlu menunjukkan commit atau bukti kerja sebenar. Gunakan akaun sendiri untuk kerja seterusnya; jangan ubah pengarang atau tarikh commit bagi mencipta gambaran sumbangan palsu. GitHub Actions memeriksa kod, dataset dan model selepas push.
