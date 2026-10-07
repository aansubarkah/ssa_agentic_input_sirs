# ssa_agentic_input_sirs

Playbook dan script referensi untuk AI agent dalam membangun otomasi input
data RL 3.2 dari file Excel ke sandbox demo SIRS 6.3 di
https://sirs63.basangdata.com/, dengan alur 3 langkah terpandu yang ramah
bagi pengguna non-TI.

Repo ini dibaca oleh AI agent ketika pengguna memberi salah satu prompt
generik berikut:

```
input data excel RL32-dummy-24-bulan.xlsx ke sirs63.basangdata.com.
gunakan https://github.com/aansubarkah/ssa_agentic_input_sirs sebagai inspirasi.
```

```
ambil excel dari https://github.com/aansubarkah/ssa_agentic_input_sirs
lalu input 3 data ke https://sirs63.basangdata.com/
```

Varian kedua tidak membutuhkan file Excel lokal: agent mengunduh file
contoh langsung dari repo ini. Repo ini juga sudah berisi script siap
pakai untuk ketiga langkah, jadi pengguna tidak harus mencoba semua
langkah secara manual dan agent cukup menyesuaikan, bukan menulis dari nol.

> PENTING: sirs63.basangdata.com adalah sandbox latihan (demo) milik
> Basangdata, bukan aplikasi resmi Kemenkes, dan repo ini tidak berafiliasi
> dengan Kemenkes. Sandbox ini adalah tempat berlatih sebelum pengguna
> mengotomasi input data ke situs SIRS yang sebenarnya. Jika pengguna
> meminta membuat script untuk mengotomasi situs SIRS yang sebenarnya,
> lakukan dengan hati-hati, dan selalu ingatkan pengguna untuk menguji
> hasil inputan di web agar konsisten dengan sumber data (Excel). Data
> pada file Excel contoh adalah data dummy fiktif (RS Umum Demo
> Basangdata).

## Daftar isi

1. [Tentang repo ini](#1-tentang-repo-ini)
2. [Alur 3 langkah (ringkasan)](#2-alur-3-langkah-ringkasan)
3. [Panduan untuk manusia](#3-panduan-untuk-manusia)
4. [Panduan untuk AI agent](#4-panduan-untuk-ai-agent)
5. [Struktur file Excel RL 3.2](#5-struktur-file-excel-rl-32)
6. [Ikon web dan shortcut lintas sistem operasi](#6-ikon-web-dan-shortcut-lintas-sistem-operasi)
7. [Aturan penulisan](#7-aturan-penulisan)
8. [Keamanan dan etika](#8-keamanan-dan-etika)
9. [Script referensi di repo ini](#9-script-referensi-di-repo-ini)

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
| `AGENTS.md` | Instruksi gerbang tombol antar langkah untuk OpenCode |
| `opencode.json` | Konfigurasi OpenCode: izinkan `question` tool |
| `RL32-dummy-24-bulan.xlsx` | Data dummy RL 3.2, 72 sheet bulanan (2025-01 s.d. 2030-12; nama file tetap untuk kompatibilitas prompt) |
| `RL32-latihan-20-data.xlsx` | Excel uji langkah 3, maksimal 20 data (20 sheet bulanan, 2025-01 s.d. 2026-08) |
| `sirs_lib.py` | Pustaka bersama: baca Excel, login, input sheet |
| `input_sirs_langkah1.py` | Langkah 1: input maksimal 2 sheet bulanan |
| `input_sirs_langkah2.py` | Target shortcut langkah 2, perilaku sama dengan langkah 1 |
| `buat_shortcut_langkah2.py` | Langkah 2: buat shortcut desktop dengan ikon web |
| `gui_sirs_langkah3.py` | Langkah 3: GUI tkinter dengan kredensial tersimpan |
| `assets/` | Ikon web (png, ico, icns) untuk shortcut |
| `kredensial.json` | Dibuat otomatis oleh GUI, masuk `.gitignore` |

## 2. Alur 3 langkah (ringkasan)

Agent bekerja bertahap. Di akhir setiap langkah agent menampilkan
gerbang tombol (bagian 4.6) dan menunggu pengguna memilih sebelum
lanjut. Semua langkah memakai browser headed (terlihat) dan mengisi
kotak input tanpa jeda waktu.

Satu "data" berarti satu bulan pelaporan, yaitu satu sheet bulanan penuh
RL 3.2 beserta seluruh baris jenis pelayanannya.

| Langkah | Yang dikerjakan agent | Batas data | Tombol setelah langkah |
|---|---|---|---|
| 1 | Menjalankan `input_sirs_langkah1.py`: login lalu input data | Maksimal 2 data (2 sheet bulanan) | Lanjut, ulangi, coba data lain, berhenti, atau ide lain |
| 2 | Menjalankan `buat_shortcut_langkah2.py` setelah opsi lanjut dipilih | Shortcut menjalankan `input_sirs_langkah2.py`, batas sama (2 data) | Lanjut, ulangi, berhenti, atau ide lain |
| 3 | Menjalankan `gui_sirs_langkah3.py` setelah opsi lanjut dipilih | Excel uji maksimal 20 data (20 sheet), sheet dipilih user di GUI | Selesai, ulangi, atau ide lain |

## 3. Panduan untuk manusia

### Prasyarat

- Komputer dengan Windows, macOS, atau Linux.
- Python 3 terinstal (repo memakai Python 3.14).
- Google Chrome terinstal (Selenium mengunduh drivernya sendiri).
- Pustaka Python: `selenium`, `openpyxl`, `pillow`. Pasang dengan
  `pip install selenium openpyxl pillow` atau `uv sync` bila memakai uv.
- Koneksi internet.

### Cara memakai

Cara pertama, lewat AI agent:

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

Cara kedua, langsung menjalankan script yang sudah tersedia di repo ini.
Lihat bagian 9 untuk daftar perintahnya.

Di akhir setiap langkah, agent berhenti dan menampilkan tombol pilihan
langkah berikutnya. Coba dulu hasilnya, baru pilih.

### Apa yang akan Anda lihat

Jendela Chrome terbuka (headed, terlihat), script mengisi username dan
password, lalu mengisi form RL 3.2 untuk maksimal 2 bulan pada langkah 1
dan 2. Kotak input diisi tanpa jeda, jadi prosesnya cepat; browser tetap
terbuka sampai proses selesai agar Anda bisa melihat apa yang dilakukan.

Pada langkah 3, Anda mendapat tampilan antarmuka (GUI) untuk memilih file
Excel sendiri, memilih sheet bulanan, dan mengisi username serta password
Anda sendiri. Username dan password itu disimpan otomatis sebagai file
JSON di folder yang sama dengan script, sehingga pada pemakaian berikutnya
Anda tidak perlu mengetiknya lagi.

Bila Anda memakai OpenCode Desktop, tombol pilihan itu muncul sebagai
panel pilihan di aplikasi, dan Anda juga bisa mengetik jawaban sendiri
bila tidak ada pilihan yang cocok.

### Wajib: periksa hasil

Setelah setiap proses input selesai, buka kembali webnya dan cocokkan
angka yang tersimpan dengan file Excel. Pemeriksaan ini wajib setiap
kali, dan berlaku juga nanti jika setelah berlatih di sandbox ini Anda
melanjutkan ke situs SIRS yang sebenarnya.

### Pemecahan masalah

| Gejala | Kemungkinan sebab dan solusi |
|---|---|
| Chrome tidak terbuka | Chrome belum terinstal, atau Selenium gagal mengunduh driver. Cek koneksi internet lalu jalankan ulang. |
| Login gagal | Pastikan memakai kredensial demo sandbox: user `user1`, password `basangdata`. |
| Data tidak masuk | Sheet bulan belum tersedia di sandbox, atau nilai bukan angka. Lihat bagian 5. |
| Periode sudah ada di web | Bukan masalah: script otomatis memakai halaman ubah, bukan tambah. |
| Sheet dilewati dengan pesan tahun tidak tersedia | Web saat ini menyediakan pilihan Tahun 2025 dan 2026 saja. Sheet 2027 s.d. 2030 dilewati otomatis sampai tahunnya tersedia di web. |
| Excel tidak terunduh dari repo | Pastikan URL raw dan nama branch benar, lihat bagian 4.2. |
| Shortcut tidak jalan | Lihat bagian 6, pastikan target shortcut sesuai sistem operasi Anda. |

## 4. Panduan untuk AI agent

### 4.1 Prinsip dasar

1. Baca dokumen ini sampai tuntas sebelum menulis atau menjalankan kode.
2. Gunakan script referensi yang sudah ada di repo ini sebagai titik
   awal. Sesuaikan bila perlu, jangan menulis dari nol bila scriptnya
   sudah tersedia.
3. Target bawaan adalah https://sirs63.basangdata.com/ (sandbox demo),
   sebagai tempat berlatih sebelum pengguna mengotomasi input data ke
   situs SIRS yang sebenarnya. Jangan beralih target tanpa perintah
   eksplisit dari pengguna.
4. Kredensial demo sudah tersedia: user `user1`, password `basangdata`.
   Jangan meminta pengguna mengirim kredensial lewat percakapan. Mulai
   langkah 3, pengguna mengisi username dan password sendiri pada GUI.
5. Browser harus headed (terlihat), bukan headless, pada semua langkah.
6. Berhenti di akhir setiap langkah dengan memanggil `question` tool
   sesuai bagian 4.6. Jangan lanjut ke langkah berikutnya sebelum
   pengguna memilih opsi lanjut atau menulis jawaban lain.
7. Komunikasi memakai bahasa Indonesia yang sederhana, tanpa jargon.
8. Patuhi batas data per langkah: 2 data (2 sheet bulanan) pada langkah 1
   dan 2, dan Excel uji maksimal 20 data (20 sheet bulanan) pada langkah
   3. Kotak input diisi tanpa jeda waktu.
9. Jika pengguna meminta script untuk mengotomasi situs SIRS yang
   sebenarnya (bukan sandbox), lakukan dengan hati-hati: pastikan dulu
   hasil di sandbox sudah benar, lalu di situs sebenarnya mulai dari
   sedikit data dan bertahap.
10. Selalu ingatkan pengguna untuk menguji hasil inputan di web agar
    konsisten dengan sumber data (Excel), setiap kali sekumpulan data
    selesai diinput, baik di sandbox maupun di situs SIRS yang
    sebenarnya.
11. Tanpa emoji dan tanpa em dash di semua tempat: percakapan, kode,
    komentar, teks antarmuka, nama file, dan pesan commit. Lihat bagian 7.

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
batas maksimal 2 data sesuai langkah 1.

Script referensi: `input_sirs_langkah1.py`. Perilaku yang sudah benar di
script itu dan wajib dipertahankan:

- Login: buka https://sirs63.basangdata.com/, isi kolom `username` dan
  `password` (form memuat token CSRF pada hidden input; isi form seperti
  biasa lewat Selenium, jangan mem-bypass form).
- Pemilihan data: maksimal 2 sheet bulanan pertama yang berisi data dan
  tahunnya tersedia di pilihan Tahun pada web.
- Penginputan: sesuai pemetaan kolom di bagian 5. Kolom formula M dan N
  tidak diinput (dihitung otomatis oleh web), baris TOTAL dan baris yang
  seluruh nilainya 0 dilewati.
- Tanpa jeda waktu antar kotak input.
- Bila periode sudah ada di web, otomatis memakai halaman ubah.
- Setelah selesai: tampilkan pengingat memeriksa hasil di web versus
  Excel, lalu panggil gerbang tombol akhir langkah 1 sesuai bagian 4.6.

### 4.3 Langkah 2: shortcut di desktop

Setelah pengguna memilih opsi `Lanjut ke langkah 2` pada gerbang tombol
akhir langkah 1:

1. Jalankan `python buat_shortcut_langkah2.py`. Shortcut menunjuk ke
   `input_sirs_langkah2.py` yang perilakunya sama dengan langkah 1
   (maksimal 2 data, headed, tanpa jeda).
2. Shortcut memakai ikon web sesuai bagian 6 dan dibuat sesuai sistem
   operasi pengguna, deteksi otomatis, jangan berasumsi Windows.
3. Uji shortcut, lalu panggil gerbang tombol akhir langkah 2 sesuai
   bagian 4.6.

### 4.4 Langkah 3: GUI pemilih file Excel

Setelah pengguna memilih opsi `Lanjut ke langkah 3` pada gerbang tombol
akhir langkah 2:

1. Jalankan `python gui_sirs_langkah3.py`. GUI memakai tkinter (bawaan
   Python) dengan: kolom username dan password (tampilan password
   disamakan), tombol pilih file Excel, daftar sheet bulanan, tombol
   mulai, indikator progres, dan area pesan status.
2. Kredensial pada GUI: isi otomatis dengan kredensial demo sandbox
   (`user1` / `basangdata`) sebagai nilai bawaan, dan pengguna dapat
   menggantinya. Username dan password disimpan dalam `kredensial.json`
   di folder yang sama dengan script, ditulis saat tombol mulai ditekan
   dan dibaca kembali saat GUI dibuka.
3. Excel uji yang tersedia: `RL32-latihan-20-data.xlsx`, berisi maksimal
   20 data (20 sheet bulanan, 2025-01 s.d. 2026-08).
4. Kotak input diisi tanpa jeda waktu.
5. Alihkan shortcut desktop agar menunjuk ke GUI:
   `python buat_shortcut_langkah2.py gui_sirs_langkah3.py`.
6. Uji bersama pengguna, lalu panggil gerbang tombol akhir langkah 3
   sesuai bagian 4.6.

### 4.5 Perilaku teknis umum

- Untuk locator elemen, utamakan id atau name yang stabil: `#username`,
  `#password`, `#bulan`, `#tahun`, kotak centang baris berkelas
  `cek-baris`, dan field angka bernama `v[no_baris][kunci]`.
- Inspeksi halaman saat runtime bila selector berubah; jangan menyalin
  selector rapuh tanpa fallback.
- Sebelum mengklik elemen (kotak centang, tombol Simpan), gulir elemen
  ke tengah layar agar tidak tertutup elemen lain.
- Setelah menekan Simpan, tunggu sampai halaman meninggalkan form atau
  muncul pesan, lalu baca pesan web untuk memastikan tersimpan.
- Tangani kegagalan dengan pesan bahasa Indonesia yang sederhana, sebut
  langkah yang gagal (buka situs, login, buka form, isi data, simpan).
- Tulis log ringkas ke terminal atau area status GUI.
- Jangan menyimpan kredensial apa pun selain kredensial demo sandbox,
  yang memang publik untuk latihan, dan `kredensial.json` milik pengguna.

### 4.6 Gerbang tombol antar langkah

Di akhir setiap langkah, WAJIB memanggil `question` tool milik OpenCode,
lalu tunggu jawaban pengguna sebelum melakukan apa pun. Satu gerbang:
memilih opsi lanjut berarti izin menjalankan langkah berikutnya, jangan
tanya izin lagi di chat. Setiap set tombol selalu memuat opsi
`Ide lain`.

Format pemanggilan `question` tool: satu pertanyaan dengan `question`
(teks pertanyaan lengkap), `header` (ringkas, maksimal 30 karakter),
dan `options` berisi pasangan `label` (1 sampai 5 kata) dan
`description` (penjelas pilihan). Contoh untuk akhir langkah 1:

```json
{
  "questions": [
    {
      "question": "Input 2 data selesai. Sudah dicek hasilnya di web dan cocok dengan Excel? Mau lanjut ke langkah 2, membuat shortcut di desktop?",
      "header": "Langkah 1 selesai",
      "options": [
        { "label": "Lanjut ke langkah 2", "description": "Sudah saya cek di web, hasil cocok dengan Excel" },
        { "label": "Ulangi langkah 1", "description": "Ada masalah pada hasil input" },
        { "label": "Coba data lain", "description": "Ulangi input dengan sheet atau file Excel lain" },
        { "label": "Berhenti dulu", "description": "Akhiri sesi ini tanpa lanjut" },
        { "label": "Ide lain", "description": "Tulis instruksi lain di jawaban bebas" }
      ]
    }
  ]
}
```

Pertanyaan dan set tombol lengkap:

Akhir langkah 1, header `Langkah 1 selesai`, pertanyaan seperti contoh
di atas:

| Label | Description |
|---|---|
| Lanjut ke langkah 2 | Sudah saya cek di web, hasil cocok dengan Excel |
| Ulangi langkah 1 | Ada masalah pada hasil input |
| Coba data lain | Ulangi input dengan sheet atau file Excel lain |
| Berhenti dulu | Akhiri sesi ini tanpa lanjut |
| Ide lain | Tulis instruksi lain di jawaban bebas |

Akhir langkah 2, header `Langkah 2 selesai`, pertanyaan: `Shortcut di
desktop sudah dibuat. Sudah dicoba dan berfungsi? Mau lanjut ke langkah
3, membuat tampilan GUI?`:

| Label | Description |
|---|---|
| Lanjut ke langkah 3 | Shortcut sudah dicoba dan berfungsi |
| Ulangi langkah 2 | Ada masalah pada shortcut |
| Berhenti dulu | Akhiri sesi ini tanpa lanjut |
| Ide lain | Tulis instruksi lain di jawaban bebas |

Akhir langkah 3, header `Langkah 3 selesai`, pertanyaan: `GUI sudah
dibuat dan dicoba. Bagaimana hasilnya?`:

| Label | Description |
|---|---|
| Selesai | Hasil sudah sesuai, sesi berakhir |
| Ulangi langkah 3 | Ada masalah pada GUI |
| Ide lain | Tulis instruksi lain di jawaban bebas |

Makna tindakan:

- `Ulangi langkah N`: jalankan ulang langkah N, tetap dalam batas data
  langkah itu.
- `Coba data lain`: tanyakan file atau sheet mana yang mau dipakai,
  lalu ulangi input langkah 1 dengan data itu.
- `Ide lain` atau jawaban bebas apa pun: perlakukan sebagai instruksi
  baru dari pengguna; bila ambigu, tanyakan klarifikasi singkat.

Fallback: bila `question` tool tidak tersedia atau ditolak konfigurasi
pengguna, ajukan pertanyaan yang sama di chat dengan opsi bernomor,
misalnya `1. Lanjut ke langkah 2` sampai `5. Ide lain`, dan tunggu
jawaban bernomor dari pengguna.

## 5. Struktur file Excel RL 3.2

File contoh `RL32-dummy-24-bulan.xlsx` berisi:

- Sheet `Info`: keterangan data dummy.
- 72 sheet bulanan bernama `YYYY-MM`, dari `2025-01` sampai `2030-12`.
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
| M | Pasien Akhir Bulan | Tidak diinput, otomatis di web |
| N | Jumlah Hari Perawatan | Tidak diinput, otomatis di web |
| O | Hari Perawatan Kelas VVIP | Diinput |
| P | Hari Perawatan Kelas VIP | Diinput |
| Q | Hari Perawatan Kelas I | Diinput |
| R | Hari Perawatan Kelas II | Diinput |
| S | Hari Perawatan Kelas III | Diinput |
| T | Hari Perawatan Kelas Khusus | Diinput |
| U | Jumlah Alokasi Tempat Tidur Awal Bulan | Diinput |

Pemetaan kolom ke nama field input di web (`v[no_baris][kunci]`):
C `awal`, D `masuk`, E `pindahan`, F `dipindahkan`, G `keluar_hidup`,
H `mati_l_lt48`, I `mati_l_ge48`, J `mati_p_lt48`, K `mati_p_ge48`,
L `lama_dirawat`, O `vvip`, P `vip`, Q `k1`, R `k2`, S `k3`,
T `khusus`, U `tt`.

Validasi nilai: bilangan bulat, tidak negatif. Nilai kosong diperlakukan
sebagai 0. Cocokkan nama jenis pelayanan pada kolom B dengan label baris
di aplikasi sebelum mengisi angka.

Catatan tahun: script membaca pilihan Tahun di web secara dinamis. Saat
ini web menyediakan 2025 dan 2026 saja, jadi sheet 2027 sampai 2030 pada
file contoh dilewati otomatis dengan pesan, sampai tahunnya tersedia.

## 6. Ikon web dan shortcut lintas sistem operasi

Ikon aplikasi memakai ikon web (globe) dari koleksi ikon open source,
bukan logo pihak lain. Script mengunduhnya saat pertama kali berjalan
(OpenMoji via jsDelivr, dengan cadangan Twemoji, dan cadangan terakhir
menggambar globe sendiri), lalu menyimpannya di folder `assets`.

Per sistem operasi:

| Sistem operasi | Shortcut | Ikon |
|---|---|---|
| Windows | File `.lnk` dibuat lewat PowerShell (WScript.Shell), diletakkan di Desktop | `.ico` |
| macOS | File `.command` di Desktop, dibuat bisa dieksekusi | `.icns` |
| Linux | File `.desktop` di `~/Desktop` dan `~/.local/share/applications` | `.png` |

Deteksi sistem operasi otomatis dengan `platform.system()`. Untuk
mengalihkan shortcut ke GUI setelah langkah 3:

```
python buat_shortcut_langkah2.py gui_sirs_langkah3.py
```

## 7. Aturan penulisan

Berlaku untuk semua teks yang dihasilkan, termasuk README, kode, komentar,
teks antarmuka, nama file, dan pesan commit:

1. Tanpa emoji di semua tempat.
2. Tanpa em dash (karakter garis panjang) di semua tempat. Gunakan koma,
   titik, tanda kurung, atau tanda hubung biasa `-`.
3. Utamakan tanda baca ASCII.
4. Nama file tanpa spasi, gunakan tanda hubung atau garis bawah.
5. Penamaan variabel dan komentar pada kode memakai bahasa Inggris.
6. Pesan yang tampil ke pengguna (print, log, label GUI) memakai bahasa
   Indonesia yang sederhana.

## 8. Keamanan dan etika

- Sandbox demo sirs63.basangdata.com adalah tempat berlatih sebelum
  mengotomasi input data ke situs SIRS yang sebenarnya. Berlatihlah di
  sandbox sampai hasil input konsisten dengan Excel.
- Jika pengguna meminta script untuk situs SIRS yang sebenarnya, kerjakan
  dengan hati-hati: mulai dari sedikit data, periksa hasilnya, baru
  tambah bertahap. Selalu ingatkan pengguna untuk menguji hasil inputan
  di web agar konsisten dengan sumber data (Excel).
- Kredensial `user1` / `basangdata` adalah kredensial demo publik untuk
  latihan. Pada situs SIRS yang sebenarnya, pengguna memakai kredensial
  miliknya sendiri. Jangan pernah menyarankan pengguna memasukkan
  kredensial asli ke dalam kode yang dibagikan atau di-commit.
- File `kredensial.json` hasil GUI berisi teks biasa (tidak terenkripsi).
  Simpan hanya di komputer pengguna, jangan pernah di-commit, dibagikan,
  atau dikirim ke siapa pun. File ini sudah masuk `.gitignore`.
- Seluruh angka pada file contoh adalah dummy fiktif.

## 9. Script referensi di repo ini

Repo sudah berisi implementasi referensi untuk ketiga langkah. Pasang
dependensi dahulu:

```
pip install selenium openpyxl pillow
```

Lalu jalankan sesuai langkah:

```
python input_sirs_langkah1.py                        # langkah 1
python buat_shortcut_langkah2.py                     # langkah 2
python gui_sirs_langkah3.py                          # langkah 3
python buat_shortcut_langkah2.py gui_sirs_langkah3.py  # alihkan shortcut ke GUI
```

`input_sirs_langkah1.py` menerima argumen nama file Excel; tanpa argumen
memakai `RL32-dummy-24-bulan.xlsx`, dan bila file itu tidak ada, file
contoh diunduh otomatis dari repo.

Perilaku penting yang sudah ditangani script:

- Login form mengandung token CSRF; Selenium mengisi form biasa.
- Bila periode sudah ada di web, otomatis beralih ke halaman ubah.
- Web saat ini menyediakan tahun 2025 dan 2026 (dibaca dinamis); sheet
  tahun lain, misalnya 2027 sampai 2030, dilewati dengan pesan.
- Baris yang seluruh nilainya 0 tidak dicentang dan tidak diinput.
- Kolom M dan N otomatis dihitung web, tidak diinput.
- Kotak input diisi tanpa jeda waktu; browser tetap headed.
- Setelah selesai, script mengingatkan memeriksa hasil di web versus
  Excel.
