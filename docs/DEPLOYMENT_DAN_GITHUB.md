# Deployment dan GitHub

## Deployment tempatan

Jalankan `python -m uvicorn app.main:app --host 127.0.0.1 --port 8000` dalam virtual environment. Buka localhost, semak UI, `/health` dan `/docs`. Gunakan fail model sebenar dan rekod bukti. Menjalankan server tanpa model hanya membuktikan aplikasi tersedia, bukan inferens berjaya.

## Deployment melalui Docker jika diperlukan

Dockerfile disediakan untuk Python 3.12 dan TensorFlow. Pastikan model_unquant.tflite dan labels.txt wujud sebelum build:

```powershell
docker build -t smartvision-classifier .
docker run --rm -p 8000:8000 smartvision-classifier
```

Imej Docker besar kerana TensorFlow. Build dan hosting belum dijalankan dalam pakej ini. Pilih hos dengan RAM dan ruang disk yang memadai untuk model. Pada hos, tetapkan port melalui PORT dan gunakan HTTPS jika pengguna mengakses webcam dari luar localhost. `/health` menunjukkan server hidup tetapi semak `model_ready` juga. Jangan jadikan health status `ok` sahaja sebagai bukti model siap. Jangan gunakan `--reload` untuk deployment awam. Endpoint tiada autentikasi atau rate limit; untuk penggunaan umum sebenar, tambah kedua-duanya serta had upload pada reverse proxy.

## Repository GitHub

Folder projek asal mempunyai repository Git tempatan dengan commit bantuan Codex. Ini bukan bukti sumbangan pelajar atau kerja berkala sepanjang minggu. Arkib ZIP mengandungi fail projek tanpa metadata .git; jika menggunakan ZIP, mulakan repository melalui arahan di bawah. Jika menggunakan folder asal, sambung sejarah yang sedia ada dan rekod kerja anda sendiri.

Bina repository kosong melalui akaun GitHub anda, contohnya `dka3223-smartvision`. Arahan berikut ialah tindakan masa hadapan, bukan bukti sudah diterbitkan:

```powershell
git init
git add app static requirements*.txt tests tools .gitignore README.md
git commit -m "Add image classifier application and API"
git add docs evidence Dockerfile .dockerignore dataset
git commit -m "Add experiment plan and project documentation"
git branch -M main
git remote add origin https://github.com/NAMA_ANDA/dka3223-smartvision.git
git push -u origin main
```

Jika repository sudah diinisialisasi atau remote sudah wujud, semak `git status` dan `git remote -v` dahulu. Gantikan NAMA_ANDA. Jangan masukkan token dalam URL. Gunakan login rasmi GitHub/Git credential manager.

Commit secara berkala selepas kerja sebenar: dataset manifest, eksport model, eksperimen, pembaikan hasil ujian dan laporan. Jangan cipta tarikh sejarah, sumbangan ahli atau commit kosong untuk membayangkan kerja terdahulu. Jika berkumpulan, setiap ahli menggunakan identiti sendiri dan menjelaskan perubahan yang dibuat.

Fail model binari dan gambar diabaikan oleh `.gitignore` bagi mengelakkan saiz besar serta perkongsian tidak sengaja. Penyerahan tetap memerlukan akses: kongsi dataset sah dan eksport E1/E2 melalui GitHub Release atau storan yang dibenarkan, kemudian isi pautan dalam model_registry.csv/dataset_sources.csv dan README. Atau ubah aturan ignore dan guna Git LFS jika sesuai. Jangan biarkan fail penting hanya di komputer anda.

## Bukti minimum

Simpan URL repository sebenar, screenshot sejarah commit, status API 200 dengan model sebenar, JSON sebenar, screenshot UI dan catatan persekitaran. Pastikan penilai mempunyai akses. Simpan video demo jika diminta pensyarah.
