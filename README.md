# Aplikasi Enkripsi Modern

Aplikasi web sederhana berbasis Streamlit untuk mengenkripsi dan mendekripsi teks serta berkas menggunakan **AES-256-GCM**. Kunci enkripsi diturunkan dari kata sandi pengguna dengan **PBKDF2-HMAC-SHA256**.

> Aplikasi ini merupakan proyek pembelajaran. Baca [Catatan keamanan](#catatan-keamanan) sebelum menggunakannya untuk data penting.

## Fitur

- Enkripsi teks dan keluaran dalam bentuk token Base64.
- Dekripsi teks dari token Base64.
- Enkripsi berkas menjadi berkas biner berekstensi `.enc`.
- Dekripsi berkas `.enc` dan unduh hasilnya.
- Verifikasi integritas dan autentikasi oleh AES-GCM saat dekripsi; kata sandi salah atau data yang berubah menyebabkan dekripsi gagal.
- Skrip `pengujian.py` untuk mengukur waktu enkripsi/dekripsi pada data acak berukuran 1 KB, 1 MB, dan 10 MB, serta demonstrasi avalanche.

Antarmuka menerima unggahan berkas tanpa memeriksa jenis atau ekstensi berkas. Karena itu, walaupun label antarmuka menyebut PDF/gambar, proses kriptografi bekerja pada byte berkas dan tidak terbatas pada kedua jenis tersebut.

## Teknologi dan algoritma

- **Python** sebagai bahasa pemrograman.
- **Streamlit** untuk antarmuka web.
- **cryptography** untuk AES-GCM dan PBKDF2.
- **AES-256-GCM** menyediakan enkripsi terautentikasi dengan kunci 256-bit.
- **PBKDF2-HMAC-SHA256** menurunkan kunci 32-byte dari kata sandi, salt acak 16-byte, dan 480.000 iterasi.
- Nonce acak 12-byte dibuat untuk setiap enkripsi. Salt, nonce, dan hasil AES-GCM disimpan bersama dalam urutan `salt || nonce || ciphertext+tag`.
- Untuk teks, gabungan byte tersebut dikodekan sebagai Base64. Untuk berkas, gabungan disimpan sebagai byte mentah.

AES-GCM menyertakan authentication tag pada hasil enkripsi. Aplikasi tidak menyimpan kata sandi atau kunci ke berkas; pengguna memasukkan kata sandi untuk setiap operasi.

## Persyaratan

- Python terpasang.
- Koneksi internet untuk memasang paket melalui pip (atau paket tersedia dari sumber lokal).

Repository ini belum menyediakan `requirements.txt` atau berkas pengunci dependensi. Paket yang digunakan aplikasi dapat dipasang langsung:

```bash
python -m pip install streamlit cryptography
```

Di Windows, bila perintah `python` tidak tersedia, gunakan `py -m pip ...`.

## Instalasi dan menjalankan aplikasi

1. Clone repository dan masuk ke foldernya:

   ```bash
   git clone https://github.com/ranji4559/Aplikasi-Enkripsi-Modern.git
   cd Aplikasi-Enkripsi-Modern
   ```

2. (Disarankan) Buat dan aktifkan virtual environment, lalu pasang paket:

   ```bash
   python -m venv .venv
   # Windows PowerShell
   .\.venv\Scripts\Activate.ps1
   # macOS/Linux: source .venv/bin/activate
   python -m pip install streamlit cryptography
   ```

3. Jalankan aplikasi:

   ```bash
   streamlit run app.py
   ```

Streamlit akan menampilkan alamat aplikasi lokal di terminal dan/atau membuka browser.

## Cara menggunakan

### Enkripsi dan dekripsi teks

1. Buka tab **Enkripsi Teks**, masukkan teks dan kata sandi, lalu pilih **Enkripsi Teks**.
2. Salin token Base64 yang ditampilkan dan simpan bersama kata sandi secara aman. Aplikasi tidak menyediakan penyimpanan token otomatis.
3. Untuk membuka pesan, pilih tab **Dekripsi Teks**, masukkan token Base64 dan kata sandi yang sama, lalu pilih **Dekripsi Teks**.

### Enkripsi dan dekripsi berkas

1. Buka tab **Enkripsi Berkas**, unggah berkas dan masukkan kata sandi, lalu pilih **Enkripsi Berkas**.
2. Unduh hasil berkas dengan akhiran `.enc` dan simpan kata sandinya secara terpisah.
3. Buka tab **Dekripsi Berkas**, unggah berkas `.enc`, masukkan kata sandi yang sama, lalu pilih **Dekripsi Berkas** untuk mengunduh hasilnya.

Nama hasil dekripsi dibentuk dengan menghapus akhiran `.enc` dari nama berkas unggahan. Simpan salinan asli sebelum mengenkripsi; kata sandi yang hilang tidak dapat dipulihkan oleh aplikasi.

## Struktur berkas

```text
.
├── app.py             # Antarmuka Streamlit untuk teks dan berkas
├── crypto_engine.py   # Derivasi kunci serta fungsi enkripsi/dekripsi
├── pengujian.py       # Skrip pengukuran waktu dan demonstrasi avalanche
└── README.md          # Dokumentasi proyek
```

## Pengujian yang tersedia

Jalankan skrip pengukuran secara manual dengan:

```bash
python pengujian.py
```

Skrip membuat data acak, mengukur durasi enkripsi/dekripsi untuk tiga ukuran, lalu mencetak demonstrasi avalanche. Angka waktu bergantung pada perangkat dan kondisi saat dijalankan; README ini tidak menyatakan hasil benchmark tertentu.

Bagian avalanche pada skrip mengubah karakter `S` menjadi `T` (bukan tepat satu bit). Selain itu, setiap pemanggilan enkripsi menghasilkan salt dan nonce baru secara acak, sementara skrip membandingkan byte keluaran yang memuat keduanya. Jadi hasil tersebut hanya demonstrasi sederhana dan **bukan pengukuran avalanche terkontrol**. Repository saat ini tidak berisi suite unit test otomatis.

## Catatan keamanan

- Gunakan kata sandi yang kuat dan unik. Kehilangan kata sandi berarti data tidak dapat didekripsi.
- Jangan membagikan kata sandi bersama ciphertext atau berkas `.enc` melalui kanal yang sama.
- Salt dan nonce bukan rahasia dan memang disimpan bersama ciphertext. Jangan mengubah atau memotong berkas terenkripsi; verifikasi GCM akan gagal.
- Enkripsi dilakukan di proses aplikasi Streamlit yang sedang berjalan. Jangan mengunggah data sensitif ke server yang tidak Anda kendalikan atau percayai.
- Aplikasi tidak mengimplementasikan manajemen kunci, pemulihan kata sandi, penyimpanan aman, maupun format berkas terversi.
- `crypto_engine.py` menampilkan detail exception sebagai bagian dari pesan kegagalan dekripsi teks. Hindari menampilkan keluaran aplikasi kepada pihak yang tidak tepercaya.
- Tinjau dan uji aplikasi sebelum memakainya untuk melindungi data penting atau menjalankannya sebagai layanan publik.

## Lisensi

Repository ini belum menyertakan berkas lisensi. Hak penggunaan dan distribusi mengikuti ketentuan pemilik repository.
