"""Step 1: enter at most 2 monthly RL 3.2 sheets from Excel to the sandbox.

Usage:
    python input_sirs_langkah1.py [file.xlsx]

Without an argument it uses RL32-dummy-24-bulan.xlsx in this folder; when
that file is missing it is downloaded from the repository (prompt variant
B). Login uses the sandbox demo credentials. Input boxes are filled
without any delay.
"""

import os
import sys

import sirs_lib as lib

MAX_SHEETS = 2  # step 1 limit: 2 data means 2 months / 2 sheets


def main():
    excel_path = sys.argv[1] if len(sys.argv) > 1 else "RL32-dummy-24-bulan.xlsx"
    if not os.path.exists(excel_path):
        print("File tidak ditemukan:", excel_path)
        print("Mengunduh file contoh dari repo...")
        lib.download_sample_excel(excel_path)
        print("Terunduh:", excel_path)

    print("Membaca:", excel_path)
    sheets = lib.read_excel(excel_path)
    if not sheets:
        print("Tidak ada sheet bulanan berisi data pada file itu.")
        return
    print("Sheet berisi data:", len(sheets))

    driver = lib.create_driver()
    try:
        print("Membuka sandbox dan login...")
        try:
            lib.login(driver, lib.DEFAULT_USER, lib.DEFAULT_PASSWORD)
        except Exception:
            print("Login gagal. Periksa koneksi dan kredensial demo, lalu coba lagi.")
            return
        print("Login berhasil.")

        available = set(lib.available_years(driver))
        if not available:
            print("Tidak bisa membaca pilihan tahun pada web.")
            return
        print("Tahun yang tersedia di web:", ", ".join(sorted(available)))

        for sheet in sheets:
            if str(sheet["year"]) not in available:
                print("Lewati sheet %s: tahun %d tidak tersedia di web."
                      % (sheet["sheet"], sheet["year"]))
        selected = [s for s in sheets if str(s["year"]) in available][:MAX_SHEETS]
        if not selected:
            print("Tidak ada sheet yang bisa diinput dengan tahun tersebut.")
            return
        print("Akan menginput %d sheet (batas langkah 1): %s"
              % (len(selected), ", ".join(s["sheet"] for s in selected)))

        saved_count = 0
        for sheet in selected:
            print("Input sheet %s, %d jenis pelayanan..."
                  % (sheet["sheet"], len(sheet["rows"])))
            if lib.input_sheet(driver, sheet["year"], sheet["month"],
                               sheet["rows"]):
                saved_count += 1

        print("Selesai: %d dari %d sheet tersimpan." % (saved_count, len(selected)))
        print("PENGINGAT: buka web dan cocokkan hasil input dengan file Excel.")
        try:
            input("Tekan Enter untuk menutup browser...")
        except EOFError:
            pass
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
