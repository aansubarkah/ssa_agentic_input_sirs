# Desain: perbaikan file Excel contoh dan performa baca

Tanggal: 2026-10-07
Status: disetujui pengguna (arah pandas + perbaiki Excel, dikonfirmasi
error web nyata "pasiet keluar + dipindahkan melebihi pasien awal bulan")

## Masalah

1. `sirs_lib.read_excel` memakai openpyxl read_only dengan akses cell
   acak; tiap akses mem-parsing ulang XML sheet, kuadratik. Terukur
   lebih dari 150 detik (timeout) untuk 73 sheet.
2. Keluaran script tidak terlihat agent (buffer blok stdout saat non
   TTY), agent menganggap hang, membunuh proses, mengulang.
3. File Excel contoh salah kolom hitung:
   - dummy: M dan N berformula benar tapi tanpa nilai cache, pembaca
     data (pandas, openpyxl data_only) melihat kosong;
   - latihan: M dan N kosong total;
   - 266 baris di dummy punya akhir negatif, algoritma web menolak
     menyimpan (terkonfirmasi error nyata di web).

## Algoritma web (sumber: clone src/forms/rl32.php)

- akhir (M) = awal + masuk + pindahan - (keluar_hidup + mati_l_lt48 +
  mati_l_ge48 + mati_p_lt48 + mati_p_ge48 + dipindahkan), dalam kolom
  Excel: M = C+D+E-(F+G+H+I+J+K).
- hari_rawat (N) = vvip + vip + k1 + k2 + k3 + khusus, dalam kolom:
  N = O+P+Q+R+S+T.
- Aturan: akhir tidak boleh negatif; hari_rawat tidak boleh kurang
  dari lama_dirawat (L).

## Solusi

1. `scripts/perbaiki_excel.py`: perbaiki kedua file Excel secara
   deterministik. Baris dengan akhir negatif: tambah defisit ke kolom D
   (masuk). Tulis M dan N sebagai nilai statis sesuai rumus web. Baris
   TOTAL ditulis ulang sebagai jumlah kolom. Verifikasi pasca-repair:
   nol pelanggaran semua aturan.
2. `sirs_lib.read_excel` ditulis ulang dengan pandas
   (`sheet_name=None, header=None, engine="openpyxl"`), keluaran dan
   tanda tangan identik. Tambah `validate_sheets` untuk aturan web.
3. `input_sirs_langkah1.py`: aktifkan line buffering, panggil
   validasi sebelum browser, laporkan baris yang akan ditolak web.
4. Dependensi `pandas>=2.2` di pyproject dan README; panduan agent:
   jalankan dengan `python -u`, jangan hentikan script yang berjalan.

## Di luar cakupan

Perilaku GUI, perubahan situs sandbox, pembuatan ulang pola data dummy.
