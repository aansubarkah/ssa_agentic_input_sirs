# ssa_agentic_input_sirs

Playbook untuk AI agent dalam membangun otomasi input data RL 3.2 dari file
Excel ke sandbox demo SIRS 6.3 di https://sirs63.basangdata.com/, dengan alur
3 langkah terpandu yang ramah bagi pengguna non-TI.

Repo ini adalah repo referensi, bukan aplikasi jadi. Isi utamanya adalah
dokumen ini, yang akan dibaca oleh AI agent ketika pengguna memberi salah
satu prompt generik berikut:

```
input data excel RL32-dummy-24-bulan.xlsx ke sirs63.basangdata.com.
gunakan https://github.com/aansubarkah/ssa_agentic_input_sirs sebagai inspirasi.
```

```
ambil excel dari https://github.com/aansubarkah/ssa_agentic_input_sirs
lalu input 3 data ke https://sirs63.basangdata.com/
```

Varian kedua tidak membutuhkan file Excel lokal: agent mengunduh file
contoh langsung dari repo ini.

> PENTING: sirs63.basangdata.com adalah sandbox latihan (demo) milik
> Basangdata, bukan aplikasi resmi Kemenkes, dan repo ini tidak berafiliasi
> dengan Kemenkes. Seluruh alur pada dokumen ini hanya boleh dijalankan pada
> sandbox tersebut. Data pada file Excel contoh adalah data dummy fiktif
> (RS Umum Demo Basangdata). Jangan pernah menjalankan alur ini pada aplikasi
> SIRS resmi produksi.

## Daftar isi

1. [Tentang repo ini](#1-tentang-repo-ini)
2. [Alur 3 langkah (ringkasan)](#2-alur-3-langkah-ringkasan)
3. [Panduan untuk manusia](#3-panduan-untuk-manusia)
4. [Panduan untuk AI agent](#4-panduan-untuk-ai-agent)
5. [Struktur file Excel RL 3.2](#5-struktur-file-excel-rl-32)
6. [Ikon web dan shortcut lintas sistem operasi](#6-ikon-web-dan-shortcut-lintas-sistem-operasi)
7. [Aturan penulisan](#7-aturan-penulisan)
8. [Keamanan dan etika](#8-keamanan-dan-etika)

## 1. Tentang repo ini

Audiens dokumen ini ada dua:

1. Manusia, khususnya pengguna awam TI yang ingin mengotomasi penginputan
   RL 3.2 ke sandbox SIRS 6.3 tanpa menulis kode sendiri.
2. AI agent (misalnya coding assistant), yang membaca dokumen ini sebagai
   acuan ketika pengguna memberi prompt generik yang menyebut repo ini.

Isi repo:

| File | Keterangan |
|---|---|
| `README.md` | Dokumen ini, playbook utama |
| `RL32-dummy-24-bulan.xlsx` | Data dummy RL 3.2, 24 sheet bulanan (2024-09 s.d. 2026-08) |
| `main.py`, `pyproject.toml` | Scaffold Python untuk script otomasi yang akan dibuat agent |

## 2. Alur 3 langkah (ringkasan)

Agent bekerja bertahap dan selalu berhenti di akhir setiap langkah untuk
menunggu pengguna mencoba hasilnya dan memberi feedback sebelum lanjut.

| Langkah | Yang dikerjakan agent | Batas data | Jeda per input | Berhenti setelah |
|---|---|---|---|---|
| 1 | Script Python Selenium headed: login lalu input data | Maksimal 3 data | 0,5 detik | User mencoba script dan memberi feedback |
| 2 | Membuat shortcut di desktop, fungsi sama dengan langkah 1 | Maksimal 3 data | 0,5 detik | User mencoba shortcut |
| 3 | Membuat GUI pemilih file Excel, lalu mengalihkan shortcut ke GUI | Excel uji maksimal 20 data | 0,1 detik (antar input, bukan per halaman) | User mencoba GUI |

Satu "data" berarti satu baris jenis pelayanan RL 3.2 (misalnya Umum,
Penyakit Dalam, Kesehatan Anak) pada satu sheet bulanan.

## 3. Panduan untuk manusia

### Prasyarat

- Komputer dengan Windows, macOS, atau Linux.
- Python 3 terinstal (repo memakai Python 3.14).
- Google Chrome terinstal (Selenium akan mengunduh drivernya sendiri).
- Koneksi internet.
- File Excel RL 3.2 yang ingin diinput.

### Cara memakai

1. Buka AI agent atau coding assistant pilihan Anda.
2. Tempel salah satu prompt generik berikut.

   Varian A, memakai file Excel milik Anda (ganti nama file sesuai milik
   Anda):

   ```
   input data excel {nama_file.xlsx} ke sirs63.basangdata.com.
   gunakan https://github.com/aansubarkah/ssa_agentic_input_sirs sebagai inspirasi.
   ```

   Varian B, tanpa file lokal, Excel diambil langsung dari repo ini:

   ```
   ambil excel dari https://github.com/aansubarkah/ssa_agentic_input_sirs
   lalu input 3 data ke https://sirs63.basangdata.com/
   ```

3. Agent akan membaca repo ini, lalu membuat dan menjalankan script
   otomasi langkah 1.
4. Di akhir setiap langkah, agent berhenti dan bertanya. Coba dulu hasilnya,
   baru lanjut.

### Apa yang akan Anda lihat

Pada langkah 1 dan 2, jendela Chrome terbuka (headed, terlihat), agent
mengisi username dan password, lalu mengisi form RL 3.2 maksimal 3 baris.
Setiap input diberi jeda 0,5 detik supaya Anda bisa melihat bagaimana
otomasi bekerja.

Pada langkah 3, Anda mendapat tampilan antarmuka (GUI) untuk memilih file
Excel sendiri, dan jeda antar input dipersingkat menjadi 0,1 detik.

### Pemecahan masalah

| Gejala | Kemungkinan sebab dan solusi |
|---|---|
| Chrome tidak terbuka | Chrome belum terinstal, atau Selenium gagal mengunduh driver. Cek koneksi internet lalu jalankan ulang. |
| Login gagal | Pastikan memakai kredensial demo sandbox: user `user1`, password `basangdata`. |
| Data tidak masuk | Sheet bulan belum tersedia di sandbox, atau nilai bukan angka. Lihat bagian 5. |
| Excel tidak terunduh dari repo | Pastikan URL raw dan nama branch benar, lihat bagian 4.2. |
| Shortcut tidak jalan | Lihat bagian 6, pastikan target shortcut sesuai sistem operasi Anda. |

## 4. Panduan untuk AI agent

### 4.1 Prinsip dasar

1. Baca dokumen ini sampai tuntas sebelum menulis kode.
2. Target satu-satunya adalah https://sirs63.basangdata.com/ (sandbox demo).
   Jangan pernah mengarahkan otomasi ke situs lain, termasuk SIRS resmi.
3. Kredensial demo sudah tersedia: user `user1`, password `basangdata`.
   Jangan meminta pengguna membuat akun atau mengirim kredensial lain.
4. Browser harus headed (terlihat), bukan headless, pada semua langkah,
   karena tujuan demo adalah pengguna melihat otomasi bekerja.
5. Berhenti di akhir setiap langkah. Jangan lanjut ke langkah berikutnya
   sebelum pengguna menyatakan sudah mencoba dan memberi feedback.
6. Komunikasi memakai bahasa Indonesia yang sederhana, tanpa jargon.
7. Tanpa emoji dan tanpa em dash di semua tempat: percakapan, kode,
   komentar, teks antarmuka, nama file, dan pesan commit. Lihat bagian 7.
8. Patuhi batas data per langkah: 3 data pada langkah 1 dan 2, Excel uji
   maksimal 20 data pada langkah 3. Jangan menginput 36 baris sekaligus.

### 4.2 Langkah 1: script Selenium headed

Pemicu: prompt generik dari pengguna. Dua varian yang dikenali (contoh
lengkap ada di bagian 3):

- Varian A, file Excel lokal milik pengguna: `input data excel
  {nama_file.xlsx} ke sirs63.basangdata.com`.
- Varian B, Excel diambil dari repo ini: `ambil excel dari
  https://github.com/aansubarkah/ssa_agentic_input_sirs lalu input 3 data
  ke https://sirs63.basangdata.com/`.

Untuk varian B (atau bila file yang disebut pengguna tidak ditemukan di
komputer), unduh file contoh dari repo melalui URL raw:

```
https://raw.githubusercontent.com/aansubarkah/ssa_agentic_input_sirs/master/RL32-dummy-24-bulan.xlsx
```

(Sesuaikan nama branch bila berbeda.) Simpan file di folder kerja, lalu
lanjut seperti biasa. Kalau prompt tidak menyebut jumlah data, tetap pakai
batas maksimal 3 data sesuai langkah 1.

Hasil yang harus dibuat: satu script Python, misal `input_sirs_langkah1.py`.

Spesifikasi teknis:

- Bahasa: Python. Pustaka: `selenium` (versi 4.6 atau lebih baru, Selenium
  Manager mengunduh ChromeDriver otomatis, tidak perlu webdriver-manager)
  dan `openpyxl` untuk membaca Excel.
- Browser: Google Chrome, mode headed.
- Login: buka https://sirs63.basangdata.com/, isi kolom `username` dan
  `password` (form memakai id `username` dan `password`, serta memuat token
  CSRF pada hidden input; isi form seperti biasa lewat Selenium, jangan
  mem-bypass form).
- Pemilihan data: pakai sheet bulanan pertama yang memiliki data, dan
  ambil 3 baris jenis pelayanan pertama yang nilainya tidak kosong.
- Penginputan: isi form RL 3.2 sesuai pemetaan kolom di bagian 5. Lewati
  kolom formula M dan N (dihitung otomatis oleh aplikasi) dan baris TOTAL.
- Jeda: `time.sleep(0.5)` setiap selesai satu input (satu baris form),
  supaya pengguna melihat prosesnya.
- Setelah script selesai dibuat dan dijalankan, berhenti dan minta
  pengguna mencoba serta memberi feedback.

### 4.3 Langkah 2: shortcut di desktop

Setelah pengguna menyetujui lanjut, tanyakan:

```
Mau dibuatkan shortcut di desktop?
```

Jika ya:

1. Buat shortcut yang menjalankan script langkah 1, perilakunya sama
   (login, input maksimal 3 data, jeda 0,5 detik).
2. Gunakan ikon web sesuai bagian 6.
3. Buat sesuai sistem operasi pengguna (Windows, macOS, atau Linux),
   deteksi dengan `platform.system()`, jangan berasumsi Windows.
4. Uji shortcut, lalu berhenti menunggu feedback.

### 4.4 Langkah 3: GUI pemilih file Excel

Setelah pengguna menyetujui lanjut, tanyakan:

```
Mau dibuatkan tampilan antarmuka (GUI) supaya Anda bisa memilih sendiri
file Excel yang dipunya?
```

Jika ya:

1. Buat GUI, disarankan `tkinter` (bawaan Python): tombol pilih file
   Excel, pilihan sheet bulanan, tombol mulai, indikator progres, dan area
   pesan status.
2. Buat file Excel uji berisi maksimal 20 data (20 baris jenis pelayanan)
   yang diambil dari data dummy, misal `RL32-latihan-20-data.xlsx`.
3. Jeda antar input hanya `time.sleep(0.1)`, dihitung antar input (antar
   baris), bukan per halaman.
4. Alihkan shortcut desktop yang dibuat pada langkah 2 agar menunjuk ke
   script GUI langkah 3 ini.
5. Uji bersama pengguna, lalu berhenti menunggu feedback.

### 4.5 Perilaku teknis umum

- Untuk locator elemen, utamakan id atau name yang stabil (misalnya
  `username`, `password`), lalu CSS class. Inspeksi halaman saat runtime;
  jangan menyalin selector rapuh tanpa fallback.
- Tangani kegagalan dengan pesan bahasa Indonesia yang sederhana, sebut
  langkah yang gagal (buka situs, login, buka form, isi data, simpan).
- Tulis log ringkas ke terminal atau area status GUI.
- Jangan menyimpan kredensial apa pun selain kredensial demo sandbox,
   yang memang publik untuk latihan.

## 5. Struktur file Excel RL 3.2

File contoh `RL32-dummy-24-bulan.xlsx` berisi:

- Sheet `Info`: keterangan data dummy.
- 24 sheet bulanan bernama `YYYY-MM`, dari `2024-09` sampai `2026-08`.
- Setiap sheet bulanan: judul di baris 1-2, header di baris 4, data di
  baris 5 sampai 40 (No 1 sampai 36), dan baris TOTAL di baris 41
  (dilewati saat input).

Pemetaan kolom:

| Kolom | Nama kolom | Keterangan saat input |
|---|---|---|
| A | No | Tidak diinput, hanya urutan |
| B | Jenis Pelayanan | Kunci pencocokan baris form |
| C | Pasien Awal Bulan | Diinput |
| D | Pasien Masuk | Diinput |
| E | Pasien Pindahan | Diinput |
| F | Pasien Dipindahkan | Diinput |
| G | Pasien Keluar Hidup | Diinput |
| H | Pasien Laki-laki Keluar Mati kurang dari 48 jam | Diinput |
| I | Pasien Laki-laki Keluar Mati 48 jam atau lebih | Diinput |
| J | Pasien Perempuan Keluar Mati kurang dari 48 jam | Diinput |
| K | Pasien Perempuan Keluar Mati 48 jam atau lebih | Diinput |
| L | Jumlah Lama Dirawat | Diinput |
| M | Pasien Akhir Bulan | Tidak diinput, formula otomatis |
| N | Jumlah Hari Perawatan | Tidak diinput, formula otomatis |
| O | Hari Perawatan Kelas VVIP | Diinput |
| P | Hari Perawatan Kelas VIP | Diinput |
| Q | Hari Perawatan Kelas I | Diinput |
| R | Hari Perawatan Kelas II | Diinput |
| S | Hari Perawatan Kelas III | Diinput |
| T | Hari Perawatan Kelas Khusus | Diinput |
| U | Jumlah Alokasi Tempat Tidur Awal Bulan | Diinput |

Validasi nilai: bilangan bulat, tidak negatif. Nilai kosong diperlakukan
sebagai 0. Cocokkan nama jenis pelayanan pada kolom B dengan label baris
di aplikasi sebelum mengisi angka.

## 6. Ikon web dan shortcut lintas sistem operasi

Ikon aplikasi memakai ikon web (ikon globe yang mewakili web), bukan logo
pihak lain. Ambil dari koleksi ikon open source lewat CDN saat proses
pembuatan berjalan, lalu simpan sebagai aset lokal, misalnya `assets/`.

Per sistem operasi:

| Sistem operasi | Shortcut | Ikon |
|---|---|---|
| Windows | File `.lnk` dibuat lewat PowerShell (WScript.Shell), diletakkan di Desktop | `.ico`, konversi dengan Pillow |
| macOS | File `.command`, atau aplikasi via `osascript` | `.icns` |
| Linux | File `.desktop` di `~/Desktop` dan `~/.local/share/applications` | `.png` |

Deteksi sistem operasi dengan `platform.system()`: `Windows`, `Darwin`,
atau `Linux`. Buat hanya untuk sistem yang dipakai pengguna. Setelah
langkah 3 selesai, target shortcut dialihkan ke script GUI.

## 7. Aturan penulisan

Berlaku untuk semua teks yang dihasilkan, termasuk README, kode, komentar,
teks antarmuka, nama file, dan pesan commit:

1. Tanpa emoji di semua tempat.
2. Tanpa em dash (karakter garis panjang) di semua tempat. Gunakan koma,
   titik, tanda kurung, atau tanda hubung biasa `-`.
3. Utamakan tanda baca ASCII.
4. Nama file tanpa spasi, gunakan tanda hubung atau garis bawah.

## 8. Keamanan dan etika

- Hanya jalankan otomasi pada sandbox demo sirs63.basangdata.com.
- Kredensial `user1` / `basangdata` adalah kredensial demo publik untuk
  latihan. Jangan pernah menyarankan pengguna memasukkan kredensial asli
  ke dalam kode.
- Seluruh angka pada file contoh adalah dummy fiktif.
- Jeda antar input yang ditentukan juga berfungsi menjaga beban server
  demo, jangan dihilangkan.
