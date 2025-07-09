# 🧠 Ringkasan Dokumen AI + Dashboard

Platform AI full-stack cerdas untuk secara otomatis meringkas dokumen panjang — dirancang khusus untuk sektor hukum, keuangan, dan asuransi.

## 📌 Masalah Nyata & Solusinya

| Masalah Nyata                                                                      | Bagaimana Proyek Ini Menyelesaikannya                                                      |
|-------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| Meninjau dokumen panjang secara manual memakan waktu                               | Menggunakan AI untuk meringkas dokumen secara otomatis dalam hitungan detik                |
| Informasi penting seperti nama, tanggal, dan istilah sulit ditemukan               | Menggunakan Named Entity Recognition (NER) untuk menyorot entitas penting                  |
| Analis membuang waktu membaca laporan besar untuk mencari wawasan                  | Mengekstrak dan memvisualisasikan kata kunci dan statistik dokumen di dashboard interaktif |
| Biaya operasional tinggi untuk analisis dokumen hukum/keuangan                     | Mengurangi ketergantungan pada tinjauan manual, menghemat waktu dan biaya                 |
| Tidak ada platform terpusat untuk mengelola dan melacak dokumen yang diringkas     | Menyimpan ringkasan dan metadata dalam database PostgreSQL yang terstruktur                |
| Sulit mengintegrasikan peringkasan dokumen ke dalam alur kerja perusahaan          | Menyediakan RESTful API untuk integrasi pihak ketiga secara mudah                         |
| Sulit membagikan ringkasan dan wawasan ke tim                                      | Dashboard menampilkan ringkasan visual yang mudah diakses dan dibagikan                   |

## 🚀 Fitur

- ✨ **Peringkasan AI** menggunakan HuggingFace Transformers (model BART/T5).
- 📊 **Dashboard Interaktif** dibangun dengan React.js dan Chart.js untuk:
  - Statistik dokumen
  - Named Entity Recognition (NER)
  - Ekstraksi Kata Kunci
- 🗄️ **Backend API** menggunakan FastAPI.
- 🧾 **Penyimpanan Data** di PostgreSQL untuk dokumen dan metadata.
- 🔌 **Public REST API** untuk integrasi pihak ketiga.
- 📦 **Dockerized Sepenuhnya** siap produksi.
- 🔁 **CI/CD Pipeline** melalui GitHub Actions.

## 🛠️ Teknologi yang Digunakan

| Lapisan     | Teknologi                           |
|-------------|-------------------------------------|
| Frontend    | React.js, Chart.js, Axios           |
| Backend     | FastAPI, HuggingFace Transformers   |
| Basis Data  | PostgreSQL                          |
| DevOps      | Docker, GitHub Actions              |
| Tugas NLP   | Peringkasan, NER, Ekstraksi Kata Kunci |
