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

Set tombol per langkah (label, salinan dari README bagian 4.6):

- Akhir langkah 1: `Lanjut ke langkah 2`, `Ulangi langkah 1`,
  `Coba data lain`, `Berhenti dulu`, `Ide lain`.
- Akhir langkah 2: `Lanjut ke langkah 3`, `Ulangi langkah 2`,
  `Berhenti dulu`, `Ide lain`.
- Akhir langkah 3: `Selesai`, `Ulangi langkah 3`, `Ide lain`.

Bila script langkah gagal: jelaskan kegagalan di chat, lalu tetap
panggil gerbang tombol; opsi ulangi tetap tersedia.
