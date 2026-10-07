# Rencana: perbaikan Excel contoh dan performa baca

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax.

**Goal:** File Excel contoh lolos aturan web dan terbaca cepat; keluaran script langsung terlihat agent.

**Spec:** `docs/superpowers/specs/2026-10-07-perbaikan-excel-performa-design.md`

**Aturan penulisan:** tanpa emoji, tanpa em dash, tanda baca ASCII, komentar kode bahasa Inggris, teks tampil bahasa Indonesia.

### Task 1: perbaiki kedua file Excel

- [ ] Tulis `scripts/perbaiki_excel.py` (openpyxl normal mode):
      per sheet bulanan, baris 5-40: hitung akhir; bila negatif tambah
      defisit ke kolom D; tulis M=akhir dan N=sum(O..T) statis; baris
      41 TOTAL ditulis ulang sebagai jumlah kolom C..U. Statistik
      perbaikan dicetak.
- [ ] Jalankan pada kedua file, catat statistik.
- [ ] Verifikasi pandas: M==akhir, N==sum(O:T), akhir>=0, N>=L,
      TOTAL==jumlah, nama baris sesuai web, semua nol pelanggaran.
- [ ] Commit: `fix: repair sample excel columns to match web algorithm`

### Task 2: pembaca pandas + validasi + buffering

- [ ] `sirs_lib.py`: `read_excel` pakai pandas, keluaran identik;
      tambah `validate_sheets(sheets)` mengembalikan daftar masalah
      aturan web (akhir<0, N<L) dengan pesan Indonesia.
- [ ] `input_sirs_langkah1.py`: `sys.stdout.reconfigure(line_buffering=True)`
      di awal main; setelah baca Excel panggil validate_sheets, cetak
      ringkasan masalah (maksimal 10 baris) bila ada.
- [ ] `input_sirs_langkah2.py`: pastikan warisan langkah 1 tanpa ubah.
- [ ] Verifikasi: waktu read_excel < 15 detik; ekuivalensi keluaran
      vs oracle openpyxl mode normal pada kedua file; validate_sheets
      mengembalikan list kosong pada file contoh dan menangkap kasus
      rakitan negatif.
- [ ] Commit: `perf: pandas excel reader with pre validation and line buffering`

### Task 3: dependensi dan dokumentasi

- [ ] `pyproject.toml`: tambah `pandas>=2.2`.
- [ ] README: prasyarat dan bagian 9 tambah pandas; bagian 4.5 tambah
      butir `python -u` + durasi + jangan hentikan + validasi dini;
      bagian 5 tambah paragraf rumus M/N statis dan aturan web; tabel
      isi repo tambah baris scripts/perbaiki_excel.py.
- [ ] Verifikasi: grep aturan penulisan bersih, tidak ada frasa lama.
- [ ] Commit: `docs: excel rules and unbuffered run guidance`

### Task 4: sapuan akhir

- [ ] Semua verifikasi Task 1-3 masih hijau, worktree bersih.
- [ ] Selesai: finishing-a-development-branch.
