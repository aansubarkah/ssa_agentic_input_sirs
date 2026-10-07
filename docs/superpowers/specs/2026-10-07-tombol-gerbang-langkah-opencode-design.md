# Desain: tombol gerbang antar langkah di OpenCode Desktop

Tanggal: 2026-10-07
Status: disetujui pengguna, menunggu rencana implementasi

## 1. Latar belakang dan tujuan

Repo ini adalah playbook yang dibaca AI agent ketika pengguna memberi
prompt generik. Alur kerjanya 3 langkah dan agent harus berhenti di
akhir setiap langkah menunggu feedback sebelum lanjut. Saat ini
pemberhentian itu hanya berupa pertanyaan biasa di chat.

Target utama pemakaian repo ini adalah OpenCode Desktop. OpenCode punya
built-in `question` tool: ketika agent memanggil tool itu, UI OpenCode
Desktop menampilkan panel berisi header, teks pertanyaan, dan daftar
opsi yang bisa dipilih seperti tombol. Pengguna juga bisa mengetik
jawaban bebas.

Tujuan: di akhir setiap langkah, agent memanggil `question` tool sehingga
di OpenCode Desktop muncul tombol pilihan langkah berikutnya, menggantikan
pertanyaan chat.

## 2. Keputusan yang sudah disetujui pengguna

1. Setiap set tombol selalu memuat opsi `Ide lain`.
2. Tombol tipe verifikasi: ada opsi yang menyatakan hasil sudah dicek di
   web dan cocok dengan Excel (selaras aturan wajib periksa hasil di
   README bagian 3).
3. Satu gerbang per langkah: tombol di akhir langkah N sekaligus menjadi
   izin untuk langkah N+1. Pertanyaan izin terpisah di chat dihapus.
4. Fallback untuk harness tanpa `question` tool: agent bertanya versi
   chat dengan opsi bernomor.
5. Langkah 3 juga mendapat tombol penutup.

## 3. Pendekatan

Dipilih: instruksi prompt lewat `AGENTS.md` + README + `opencode.json`.

- OpenCode otomatis memuat `AGENTS.md` di root repo ke konteks LLM.
- `AGENTS.md` mewajibkan agent memanggil `question` tool di akhir setiap
  langkah dengan set tombol tetap.
- `opencode.json` menyetel `permission.question = "allow"` supaya tool
  berjalan tanpa approval tambahan.
- README diperbarui agar konsisten untuk agent OpenCode maupun agent
  lain (fallback chat).

Alternatif yang ditolak:

- Plugin OpenCode dengan hook JS: deterministik tapi berat, tiap
  pengguna harus memasang plugin sendiri, overkill untuk playbook
  3 langkah.
- Permission gate `bash: ask`: memunculkan dialog approve/deny untuk
  menjalankan script, semantiknya salah (bukan memilih langkah
  berikutnya, tidak ada opsi lanjutan).

Keterbatasan pendekatan terpilih: bergantung kepatuhan model. Diredam
dengan instruksi tegas bernomor plus contoh set tombol konkret yang
tinggal disalin.

## 4. Perubahan file

Tanpa perubahan kode Python. Tiga file:

### 4.1 `AGENTS.md` (baru, root)

Bahasa Indonesia, ringkas (target di bawah 60 baris), isi:

- Peran: agent menjalankan playbook 3 langkah, detail di README.
- Aturan gerbang: di akhir setiap langkah WAJIB panggil `question` tool,
  tunggu jawaban, jangan lanjut sebelum jawaban diterima.
- Satu gerbang: memilih opsi lanjut berarti izin menjalankan langkah
  berikutnya.
- Selalu sertakan opsi `Ide lain`.
- Set tombol per langkah (salin mentah dari README bagian 4).
- Fallback: bila `question` tool tidak tersedia, tanya di chat dengan
  opsi bernomor.
- Mengacu aturan umum (sandbox, batas data, bahasa, tanpa emoji, tanpa
  em dash) ke README.

### 4.2 `README.md` (ubah)

- Bagian 2: kolom tabel "Berhenti setelah" diganti "Tombol setelah
  langkah" berisi ringkasan pilihan tombol.
- Bagian 3: paragraf cara memakai diperbarui, disebutkan bahwa di
  OpenCode muncul tombol pilihan dan pengguna juga bisa mengetik
  jawaban lain.
- Bagian 4: subbab baru "Gerbang tombol antar langkah" berisi:
  kewajiban memanggil `question` tool, set tombol final per langkah,
  contoh bentuk pemanggilan, dan aturan fallback.
- Bagian 4: pertanyaan izin terpisah di subbab 4.3 dan 4.4 dihapus
  karena sudah digantikan gerbang tombol.
- Bagian 4.1 butir 6 diperbarui: berhenti di akhir langkah dengan
  memanggil `question` tool.
- Daftar isi dan tabel isi repo ditambahkan `AGENTS.md` dan
  `opencode.json`.

### 4.3 `opencode.json` (baru, root)

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "question": "allow"
  }
}
```

## 5. Set tombol final

Semua teks bahasa Indonesia sederhana, tanpa emoji, tanpa em dash,
tanda baca ASCII. Header `Langkah N selesai`.

### Akhir langkah 1

Pertanyaan: ingatkan memeriksa hasil di web versus Excel, lalu tanya
lanjut atau tidak.

1. Sudah saya cek di web, cocok, lanjut ke langkah 2
2. Ada masalah, ulangi langkah 1
3. Coba dengan data lain
4. Berhenti dulu
5. Ide lain

### Akhir langkah 2

1. Sudah saya coba shortcut, lanjut ke langkah 3
2. Ada masalah, ulangi langkah 2
3. Berhenti dulu
4. Ide lain

### Akhir langkah 3

1. Selesai, hasil sudah sesuai
2. Ada masalah, ulangi langkah 3
3. Ide lain

Makna tiap opsi dijelaskan di README (misal `Coba dengan data lain`
berarti agent menanyakan file atau sheet mana, lalu mengulang input
masih dalam batas langkah yang sama).

## 6. Alur

1. Pengguna buka repo ini di OpenCode Desktop, beri prompt generik.
2. Agent membaca AGENTS.md (otomatis dimuat) dan README.
3. Agent menjalankan script langkah 1.
4. Script selesai, mencetak pengingat periksa hasil.
5. Agent memanggil `question` tool dengan set tombol langkah 1.
6. Desktop menampilkan tombol. Pengguna memilih atau mengetik bebas.
7. Pilihan menentukan aksi berikutnya. `Ide lain` atau jawaban bebas
   dibaca agent sebagai instruksi baru dari pengguna.
8. Ulang untuk langkah 2 dan 3.

## 7. Error handling

- `question` tool tidak tersedia atau di-deny konfigurasi pengguna:
  agent bertanya versi chat dengan opsi bernomor yang sama.
- Script langkah gagal: agent tetap memanggil gerbang tombol, opsi
  ulangi tetap tersedia, dan agent menjelaskan kegagalan di chat
  sebelum tombol.
- Jawaban bebas di luar opsi: agent menafsirkan sebagai instruksi
  pengguna, bila ambigu agent bertanya klarifikasi singkat.

## 8. Testing

Tanpa unit test karena tanpa kode baru. Verifikasi manual:

1. Buka repo di OpenCode Desktop, cek AGENTS.md termuat di konteks
   (misal lewat pertanyaan ringkas ke agent).
2. Jalankan alur dengan prompt generik, pastikan tombol muncul di
   akhir langkah 1.
3. Pilih tiap opsi, pastikan aksi sesuai maknanya.
4. Uji fallback dengan men-deny `question` di konfigurasi, pastikan
   agent bertanya versi chat.

## 9. Di luar cakupan

- Perubahan perilaku script Python (termasuk pola `input()` penutup
  yang sudah aman dijalankan tanpa TTY karena EOFError tertangani).
- Otomasi situs SIRS selain sandbox.
- Widget atau plugin terpisah di luar mekanisme bawaan OpenCode.

## 10. Catatan verifikasi implementasi

Nama parameter persis `question` tool (misal bentuk header, teks
pertanyaan, dan daftar opsi) diverifikasi saat implementasi dari
dokumentasi OpenCode https://opencode.ai/docs/tools/ atau kode sumber
OpenCode di GitHub, supaya contoh di README akurat.
