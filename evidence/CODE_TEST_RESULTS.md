# Keputusan ujian kod

Tarikh: 23 September 2026. Persekitaran: Windows, Python 3.12.14.

**18 ujian lulus.** Arahan: `python -m pytest tests -q -p no:cacheprovider --tb=short`.

Tambahan semakan: cap jari model dalam respons API, perbandingan eksperimen yang sepadan, penolakan model sama, threshold berlainan, dataset berlainan, jumlah tidak sah, metrik NaN dan keadaan tiada ramalan diterima. Data ujian ini sintetik untuk semakan perisian sahaja.

Liputan: halaman utama dan health, keadaan tiada model (503), fail kosong/rosak (400), fail lebih 8 MB (413), threshold di luar julat (422), kontrak respons berjaya menggunakan test double, UNKNOWN, sempadan 0.70, normalisasi RGB dan tensor, output skor tidak sah dan label eksport.

JavaScript: `node --check static/script.js` lulus. Pemeriksaan pelayar mengesahkan halaman utama serta mesej apabila model belum tersedia. Fail model memang belum disertakan.

Kebergantungan ujian: FastAPI 0.141.1, Starlette 1.6.0, Pydantic 2.13.5, pytest 9.1.1, httpx 0.28.1. Dua amaran deprecation datang daripada Starlette/httpx dan alias AnyIO; ia tidak menggagalkan ujian. Persekitaran ujian memasang dependency secara berasingan daripada kod projek.

Had: TensorFlow dan model sebenar belum diuji. Webcam dengan model, inferens TF.js sebenar, endpoint TFLite sebenar, penilaian E1/E2, Docker dan deployment awam belum disahkan. Ujian test double tidak boleh dijadikan bukti accuracy atau bukti endpoint model terlatih.

Masalah persekitaran yang diselesaikan: folder sementara pytest tidak boleh diakses dalam sandbox Windows. Ujian label ditukar kepada stub pembacaan fail supaya semakan parser bebas filesystem; testpaths ditetapkan kepada tests. Tiada keputusan model direka dalam proses debugging ini.
