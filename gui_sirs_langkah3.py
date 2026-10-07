"""Step 3: GUI to pick an Excel file and sheets, then enter them to the
sandbox.

The user fills in the username and password. Credentials are saved as
kredensial.json in the same folder as this script and reused automatically
in the future. Input boxes are filled without any delay.
"""

import json
import os
import threading
import tkinter as tk
from tkinter import filedialog, ttk

import sirs_lib as lib

CREDENTIALS_FILENAME = "kredensial.json"


def script_dir():
    return os.path.dirname(os.path.abspath(__file__))


def load_credentials():
    path = os.path.join(script_dir(), CREDENTIALS_FILENAME)
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return data.get("username", ""), data.get("password", "")
    except Exception:
        return lib.DEFAULT_USER, lib.DEFAULT_PASSWORD


def save_credentials(username, password):
    path = os.path.join(script_dir(), CREDENTIALS_FILENAME)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump({"username": username, "password": password},
                  handle, indent=2)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Input RL 3.2 ke SIRS Sandbox")
        self.active_sheets = []
        self.running = False

        box = ttk.Frame(self, padding=10)
        box.grid(sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        initial_user, initial_password = load_credentials()
        ttk.Label(box, text="Username:").grid(column=0, row=0, sticky="w")
        self.username_entry = ttk.Entry(box, width=32)
        self.username_entry.insert(0, initial_user)
        self.username_entry.grid(column=1, row=0, pady=2, sticky="w")

        ttk.Label(box, text="Password:").grid(column=0, row=1, sticky="w")
        self.password_entry = ttk.Entry(box, width=32, show="*")
        self.password_entry.insert(0, initial_password)
        self.password_entry.grid(column=1, row=1, pady=2, sticky="w")

        ttk.Label(box, text="File Excel:").grid(column=0, row=2, sticky="w")
        file_frame = ttk.Frame(box)
        file_frame.grid(column=1, row=2, pady=2, sticky="we")
        self.file_entry = ttk.Entry(file_frame, width=40)
        self.file_entry.pack(side="left")
        ttk.Button(file_frame, text="Pilih...",
                   command=self.choose_file).pack(side="left", padx=4)

        ttk.Label(box, text="Sheet bulanan:").grid(
            column=0, row=3, sticky="nw")
        list_frame = ttk.Frame(box)
        list_frame.grid(column=1, row=3, pady=2, sticky="w")
        self.sheet_list = tk.Listbox(list_frame, selectmode="extended",
                                     width=30, height=8)
        self.sheet_list.pack(side="left")
        scrollbar = ttk.Scrollbar(list_frame, command=self.sheet_list.yview)
        scrollbar.pack(side="left", fill="y")
        self.sheet_list.config(yscrollcommand=scrollbar.set)
        ttk.Button(box, text="Semua", width=8,
                   command=lambda: self.sheet_list.select_set(0, "end")
                   ).grid(column=1, row=4, sticky="w")

        self.progress = ttk.Progressbar(box, mode="determinate")
        self.progress.grid(column=1, row=5, pady=(8, 2), sticky="we")
        self.start_button = ttk.Button(box, text="Mulai Input",
                                       command=self.start)
        self.start_button.grid(column=1, row=6, sticky="w")

        self.log_text = tk.Text(box, width=64, height=12, state="disabled")
        self.log_text.grid(column=0, row=7, columnspan=2, pady=(8, 0),
                           sticky="we")
        self.log("Pilih file Excel RL 3.2, pilih sheet, lalu tekan Mulai Input.")
        self.log("Kredensial tersimpan di " + CREDENTIALS_FILENAME
                 + " di folder script ini.")

    def log(self, message):
        def write():
            self.log_text.config(state="normal")
            self.log_text.insert("end", message + "\n")
            self.log_text.see("end")
            self.log_text.config(state="disabled")
        self.after(0, write)

    def choose_file(self):
        name = filedialog.askopenfilename(
            title="Pilih file Excel RL 3.2",
            filetypes=[("Berkas Excel", "*.xlsx"), ("Semua berkas", "*.*")],
        )
        if not name:
            return
        self.file_entry.delete(0, "end")
        self.file_entry.insert(0, name)
        try:
            self.active_sheets = lib.read_excel(name)
        except Exception as error:
            self.log("Gagal membaca Excel: %s" % error)
            return
        self.sheet_list.delete(0, "end")
        for sheet in self.active_sheets:
            self.sheet_list.insert(
                "end", "%s (%d jenis pelayanan)"
                % (sheet["sheet"], len(sheet["rows"])))
        self.sheet_list.select_set(0, "end")
        self.log("File dibaca. Sheet berisi data: %d."
                 % len(self.active_sheets))

    def start(self):
        if self.running:
            return
        excel_path = self.file_entry.get().strip()
        if not excel_path or not os.path.exists(excel_path):
            self.log("Pilih file Excel dulu.")
            return
        selected_indices = self.sheet_list.curselection()
        if not selected_indices:
            self.log("Pilih minimal satu sheet.")
            return
        if not self.active_sheets:
            try:
                self.active_sheets = lib.read_excel(excel_path)
            except Exception as error:
                self.log("Gagal membaca Excel: %s" % error)
                return
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        if not username or not password:
            self.log("Isi username dan password.")
            return
        try:
            save_credentials(username, password)
            self.log("Kredensial disimpan ke " + CREDENTIALS_FILENAME + ".")
        except Exception as error:
            self.log("Peringatan: gagal menyimpan kredensial: %s" % error)

        selected_sheets = [self.active_sheets[i] for i in selected_indices]
        self.progress.config(maximum=len(selected_sheets), value=0)
        self.running = True
        self.start_button.config(state="disabled")
        worker = threading.Thread(
            target=self.run_input,
            args=(username, password, selected_sheets),
            daemon=True)
        worker.start()

    def run_input(self, username, password, selected_sheets):
        try:
            driver = lib.create_driver()
        except Exception as error:
            self.log("Gagal membuka Chrome: %s" % error)
            self.finish()
            return
        try:
            self.log("Membuka sandbox dan login...")
            try:
                lib.login(driver, username, password)
            except Exception:
                self.log("Login gagal. Periksa username dan password.")
                return
            self.log("Login berhasil.")
            available = set(lib.available_years(driver))
            self.log("Tahun tersedia di web: " + ", ".join(sorted(available)))
            saved_count = 0
            for sheet in selected_sheets:
                if str(sheet["year"]) not in available:
                    self.log(
                        "Lewati sheet %s: tahun %d tidak tersedia di web."
                        % (sheet["sheet"], sheet["year"]))
                    self.progress.step(1)
                    continue
                self.log("Input sheet %s, %d jenis pelayanan..."
                         % (sheet["sheet"], len(sheet["rows"])))
                if lib.input_sheet(driver, sheet["year"], sheet["month"],
                                   sheet["rows"], log=self.log):
                    saved_count += 1
                self.progress.step(1)
            self.log("Selesai: %d dari %d sheet tersimpan."
                     % (saved_count, len(selected_sheets)))
            self.log("PENGINGAT: buka web dan cocokkan hasil input dengan Excel.")
        finally:
            try:
                driver.quit()
            except Exception:
                pass
            self.finish()

    def finish(self):
        def restore():
            self.running = False
            self.start_button.config(state="normal")
        self.after(0, restore)


if __name__ == "__main__":
    app = App()
    app.mainloop()
