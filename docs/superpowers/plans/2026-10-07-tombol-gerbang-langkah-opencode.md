# Tombol Gerbang Antar Langkah OpenCode Desktop, Rencana Implementasi

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Di akhir setiap langkah playbook, agent memanggil `question` tool OpenCode sehingga di OpenCode Desktop muncul tombol pilihan langkah berikutnya.

**Architecture:** Instruksi prompt lewat 3 file: `AGENTS.md` baru (auto dimuat OpenCode ke konteks LLM), update `README.md` (bagian 2, 3, 4), dan `opencode.json` baru (permission `question: allow`). Tanpa perubahan kode Python.

**Tech Stack:** Markdown, JSON config OpenCode. Schema `question` tool terverifikasi dari kode sumber OpenCode: `questions[]` berisi `question` (string, pertanyaan lengkap), `header` (string, maksimal 30 karakter), `options[]` berisi `{label: string 1-5 kata, description: string}`, opsional `multiple: boolean`. Jawaban kembali sebagai daftar label terpilih, dan pengguna bisa mengetik jawaban bebas.

**Spec:** `docs/superpowers/specs/2026-10-07-tombol-gerbang-langkah-opencode-design.md`

**Aturan penulisan wajib (README bagian 7):** bahasa Indonesia sederhana untuk teks tampil, tanpa emoji, tanpa em dash, tanda baca ASCII, nama file tanpa spasi.

**Catatan deviasi dari spec (disetujui spec bagian 10):** label tombol dipecah jadi `label` pendek plus `description` karena schema OpenCode mewajibkan label 1-5 kata. Isi makna sama dengan spec bagian 5.

---

### Task 1: `opencode.json`

**Files:**
- Create: `opencode.json`

- [ ] **Step 1: Tulis file**

Isi lengkap:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "question": "allow"
  }
}
```

- [ ] **Step 2: Verifikasi JSON valid**

Run: `python -c "import json; print(json.load(open('opencode.json', encoding='utf-8'))['permission']['question'])"`
Expected: `allow`

- [ ] **Step 3: Commit**

```bash
git add opencode.json
git commit -m "feat: add opencode.json allowing question tool"
```

---

### Task 2: `AGENTS.md`

**Files:**
- Create: `AGENTS.md`

- [ ] **Step 1: Tulis file**

Isi lengkap:

```markdown
# AGENTS.md

Instruksi untuk AI agent yang membuka repo ini di OpenCode.

Repo ini playbook 3 langkah input RL 3.2 ke sandbox SIRS 6.3. Baca
README.md sampai tuntas sebelum bekerja, terutama bagian 4. Semua
aturan di README berlaku juga di sini.

## Gerbang tombol antar langkah

1. Kerjakan satu langkah sesuai README, lalu WAJIB memanggil `question`
   tool sebelum melakukan hal lain.
2. Pakai set tombol persis seperti README bagian 4.6. Selalu sertakan
   opsi `Ide lain`.
3. Tunggu jawaban. Memilih opsi lanjut berarti izin menjalankan langkah
   berikutnya, jangan tanya izin lagi di chat.
4. Bila `question` tool tidak tersedia, ajukan versi chat dengan opsi
   bernomor yang sama.
```

- [ ] **Step 2: Verifikasi aturan penulisan**

Run: `grep -nP '\x{2014}|[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}]' AGENTS.md; echo "exit=$?"`
Expected: `exit=1` (tidak ada em dash atau emoji)

Run: `wc -l AGENTS.md`
Expected: di bawah 25 baris (target ringkas terpenuhi)

- [ ] **Step 3: Commit**

```bash
git add AGENTS.md
git commit -m "feat: add AGENTS.md with step gate protocol"
```

---

### Task 3: README, tabel isi repo, bagian 2, dan bagian 3

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Tambah 2 baris di tabel isi repo**

Ganti baris:

```markdown
| `README.md` | Dokumen ini, playbook utama |
```

Menjadi:

```markdown
| `README.md` | Dokumen ini, playbook utama |
| `AGENTS.md` | Instruksi gerbang tombol antar langkah untuk OpenCode |
| `opencode.json` | Konfigurasi OpenCode: izinkan `question` tool |
```

- [ ] **Step 2: Ubah paragraf pembuka bagian 2**

Ganti:

```markdown
Agent bekerja bertahap dan selalu berhenti di akhir setiap langkah untuk
menunggu pengguna mencoba hasilnya dan memberi feedback sebelum lanjut.
Semua langkah memakai browser headed (terlihat) dan mengisi kotak input
tanpa jeda waktu.
```

Menjadi:

```markdown
Agent bekerja bertahap. Di akhir setiap langkah agent menampilkan
gerbang tombol (bagian 4.6) dan menunggu pengguna memilih sebelum
lanjut. Semua langkah memakai browser headed (terlihat) dan mengisi
kotak input tanpa jeda waktu.
```

- [ ] **Step 3: Ubah tabel alur bagian 2**

Ganti:

```markdown
| Langkah | Yang dikerjakan agent | Batas data | Berhenti setelah |
|---|---|---|---|
| 1 | Menjalankan `input_sirs_langkah1.py`: login lalu input data | Maksimal 2 data (2 sheet bulanan) | User mencoba dan memberi feedback |
| 2 | Menanyakan ijin, lalu menjalankan `buat_shortcut_langkah2.py` | Shortcut menjalankan `input_sirs_langkah2.py`, batas sama (2 data) | User mencoba shortcut |
| 3 | Menanyakan ijin, lalu menjalankan `gui_sirs_langkah3.py` | Excel uji maksimal 20 data (20 sheet), sheet dipilih user di GUI | User mencoba GUI |
```

Menjadi:

```markdown
| Langkah | Yang dikerjakan agent | Batas data | Tombol setelah langkah |
|---|---|---|---|
| 1 | Menjalankan `input_sirs_langkah1.py`: login lalu input data | Maksimal 2 data (2 sheet bulanan) | Lanjut, ulangi, coba data lain, berhenti, atau ide lain |
| 2 | Menjalankan `buat_shortcut_langkah2.py` setelah opsi lanjut dipilih | Shortcut menjalankan `input_sirs_langkah2.py`, batas sama (2 data) | Lanjut, ulangi, berhenti, atau ide lain |
| 3 | Menjalankan `gui_sirs_langkah3.py` setelah opsi lanjut dipilih | Excel uji maksimal 20 data (20 sheet), sheet dipilih user di GUI | Selesai, ulangi, atau ide lain |
```

- [ ] **Step 4: Ubah kalimat penutup bagian 3 cara memakai**

Ganti:

```markdown
Di akhir setiap langkah, agent berhenti dan bertanya. Coba dulu hasilnya,
baru lanjut.
```

Menjadi:

```markdown
Di akhir setiap langkah, agent berhenti dan menampilkan tombol pilihan
langkah berikutnya. Coba dulu hasilnya, baru pilih.
```

- [ ] **Step 5: Tambah kalimat di akhir bagian "Apa yang akan Anda lihat"**

Ganti:

```markdown
Anda tidak perlu mengetiknya lagi.
```

Menjadi:

```markdown
Anda tidak perlu mengetiknya lagi.

Bila Anda memakai OpenCode Desktop, tombol pilihan itu muncul sebagai
panel pilihan di aplikasi, dan Anda juga bisa mengetik jawaban sendiri
bila tidak ada pilihan yang cocok.
```

- [ ] **Step 6: Verifikasi**

Run: `grep -c "Menanyakan ijin" README.md`
Expected: `0`

Run: `grep -n "gerbang tombol" README.md`
Expected: minimal 1 baris (paragraf bagian 2)

- [ ] **Step 7: Commit**

```bash
git add README.md
git commit -m "docs: readme flow tables use gate buttons"
```

---

### Task 4: README, bagian 4 langkah demi langkah

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Ubah butir 6 di bagian 4.1**

Ganti:

```markdown
6. Berhenti di akhir setiap langkah. Jangan lanjut ke langkah berikutnya
   sebelum pengguna menyatakan sudah mencoba dan memberi feedback.
```

Menjadi:

```markdown
6. Berhenti di akhir setiap langkah dengan memanggil `question` tool
   sesuai bagian 4.6. Jangan lanjut ke langkah berikutnya sebelum
   pengguna memilih opsi lanjut atau menulis jawaban lain.
```

- [ ] **Step 2: Ubah butir penutup bagian 4.2**

Ganti:

```markdown
- Setelah selesai: tampilkan pengingat memeriksa hasil di web versus
  Excel, lalu berhenti menunggu feedback.
```

Menjadi:

```markdown
- Setelah selesai: tampilkan pengingat memeriksa hasil di web versus
  Excel, lalu panggil gerbang tombol akhir langkah 1 sesuai bagian 4.6.
```

- [ ] **Step 3: Ubah pembuka bagian 4.3**

Ganti:

````markdown
Setelah pengguna menyetujui lanjut, tanyakan:

```
Mau dibuatkan shortcut di desktop?
```

Jika ya:

1. Jalankan `python buat_shortcut_langkah2.py`.
````

Menjadi:

```markdown
Setelah pengguna memilih opsi `Lanjut ke langkah 2` pada gerbang tombol
akhir langkah 1:

1. Jalankan `python buat_shortcut_langkah2.py`.
```

- [ ] **Step 4: Ubah butir 3 bagian 4.3**

Ganti:

```markdown
3. Uji shortcut, lalu berhenti menunggu feedback.
```

Menjadi:

```markdown
3. Uji shortcut, lalu panggil gerbang tombol akhir langkah 2 sesuai
   bagian 4.6.
```

- [ ] **Step 5: Ubah pembuka bagian 4.4**

Ganti:

````markdown
Setelah pengguna menyetujui lanjut, tanyakan:

```
Mau dibuatkan tampilan antarmuka (GUI) supaya Anda bisa memilih sendiri
file Excel yang dipunya?
```

Jika ya:

1. Jalankan `python gui_sirs_langkah3.py`.
````

Menjadi:

```markdown
Setelah pengguna memilih opsi `Lanjut ke langkah 3` pada gerbang tombol
akhir langkah 2:

1. Jalankan `python gui_sirs_langkah3.py`.
```

- [ ] **Step 6: Ubah butir 6 bagian 4.4**

Ganti:

```markdown
6. Uji bersama pengguna, lalu berhenti menunggu feedback.
```

Menjadi:

```markdown
6. Uji bersama pengguna, lalu panggil gerbang tombol akhir langkah 3
   sesuai bagian 4.6.
```

- [ ] **Step 7: Verifikasi**

Run: `grep -c "berhenti menunggu feedback" README.md`
Expected: `0`

Run: `grep -c "Mau dibuatkan" README.md`
Expected: `0`

- [ ] **Step 8: Commit**

```bash
git add README.md
git commit -m "docs: readme agent steps use gate buttons"
```

---

### Task 5: README, subbab baru 4.6

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Sisipkan subbab 4.6 sebelum heading `## 5.`**

Sisipkan teks berikut tepat sebelum baris `## 5. Struktur file Excel RL 3.2` (setelah butir terakhir bagian 4.5 tentang kredensial):

````markdown
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
````

- [ ] **Step 2: Verifikasi**

Run: `grep -n "### 4.6 Gerbang tombol antar langkah" README.md`
Expected: 1 baris

Run: `grep -c "Ide lain" README.md`
Expected: minimal `7` (intro 1, contoh JSON 1, tiga tabel 3, makna tindakan 1, fallback 1)

Run: `python -c "import json,re; t=open('README.md',encoding='utf-8').read(); m=re.search(r'\x60\x60\x60json\n(.*?)\n\x60\x60\x60', t, re.S); json.loads(m.group(1)); print('json ok')"`
Expected: `json ok`

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: readme add gate button section 4.6"
```

---

### Task 6: Verifikasi akhir menyeluruh

**Files:**
- Verify only: `AGENTS.md`, `opencode.json`, `README.md`

- [ ] **Step 1: Aturan penulisan di semua file yang diubah**

Run: `grep -nP '\x{2014}|[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}]' AGENTS.md opencode.json README.md; echo "exit=$?"`
Expected: `exit=1`

- [ ] **Step 2: Tidak ada frasa lama yang tersisa**

Run: `grep -c "Menanyakan ijin\|berhenti menunggu feedback\|Mau dibuatkan" README.md`
Expected: `0`

- [ ] **Step 3: Semua rujukan bagian 4.6 konsisten**

Run: `grep -n "bagian 4.6" README.md AGENTS.md`
Expected: muncul di bagian 2 (1x), 4.1 (1x), 4.2 (1x), 4.3 (1x), 4.4 (1x), heading 4.6 (1x, tulis `4.6 Gerbang`), AGENTS.md (1x)

- [ ] **Step 4: JSON valid**

Run: `python -c "import json; json.load(open('opencode.json', encoding='utf-8')); print('ok')"`
Expected: `ok`

- [ ] **Step 5: Pastikan worktree bersih**

Run: `git status --short`
Expected: kosong

Bila semua lolos, implementasi selesai. Verifikasi manual di OpenCode Desktop (buka repo, beri prompt generik, pastikan AGENTS.md termuat dan tombol muncul di akhir langkah 1) dilakukan pengguna setelahnya.

---

## Catatan eksekutor

- Semua string Ganti di atas harus cocok persis dengan teks README saat ini. Bila tidak cocok, baca file dan sesuaikan, jangan ubah makna.
- README memakai line ending LF, jaga jangan berubah jadi CRLF.
- Jangan tambahkan fitur lain (YAGNI): tidak ada perubahan script Python, tidak ada plugin, tidak ada permission tambahan.
