# -Sosmed-Scanner-

Sosmed-Scanner adalah sebuah perangkat lunak *backend* berbasis Python yang dirancang untuk melakukan pemindaian (*scanning*) profil publik di berbagai platform media sosial. Program ini berjalan sepenuhnya melalui baris perintah (*Command Line Interface* / CLI) secara efisien dan aman.

## 🛠️ Teknologi yang Digunakan

### 📝 Bahasa Pemrograman
* **Python 3.7** atau versi yang lebih baru.

### 📚 Pustaka / Modul yang Dipakai (Standard Library)
Proyek ini dibangun sepenuhnya menggunakan modul bawaan Python, sehingga **tidak memerlukan instalasi tambahan (*zero-dependency*)**:

| Modul | Fungsi |
| --- | --- |
| `sys` | Membaca input argumen langsung dari baris perintah. |
| `time` | Memberikan jeda (*rate-limiting*) antar permintaan agar tidak membebani server target. |
| `urllib.request` | Melakukan permintaan HTTP untuk mengakses halaman web profil publik. |
| `urllib.error` | Menangani kesalahan koneksi atau respon HTTP (seperti error 404 atau 403). |
| `datetime` | Mencatat stempel waktu (*timestamp*) dan penamaan berkas log hasil pemindaian secara otomatis. |
| `json` | Mengolah dan menyimpan data hasil pemindaian ke dalam format terstruktur. |

> ❌ **Tidak Menggunakan Framework Eksternal:** Proyek ini sengaja tidak bergantung pada framework atau pustaka pihak ketiga seperti *Requests*, *Flask*, atau *Django* agar tetap ringan dan dapat langsung dijalankan di lingkungan komputer mana pun yang sudah terpasang Python.

## 🚀 Cara Instalasi & Menjalankan

### Prasyarat
Pastikan Anda sudah menginstal Python (versi 3.7 ke atas) di perangkat Anda. Anda dapat mengeceknya dengan perintah:
```bash
python --version
```

### Langkah Menjalankan
1. Klon repositori ini ke komputer lokal Anda:
   ```bash
   git clone https://github.com
   ```
2. Masuk ke dalam direktori proyek:
   ```bash
   cd -Sosmed-Scanner-
   ```
3. Jalankan skrip utama (sesuaikan nama file utama Anda, misalnya `main.py`):
   ```bash
   python main.py
   ```

## 📝 Lisensi
Proyek ini dilisensikan di bawah **MIT License** - lihat berkas [LICENSE](LICENSE) untuk informasi lebih lanjut.
