"""Shared library for the RL 3.2 input automation to the SIRS 6.3 sandbox.

Used by input_sirs_langkah1.py, input_sirs_langkah2.py, and
gui_sirs_langkah3.py. No emoji, no em dash.
"""

import re
import urllib.request

BASE_URL = "https://sirs63.basangdata.com"
DEFAULT_USER = "user1"
DEFAULT_PASSWORD = "basangdata"
RAW_EXCEL_URL = (
    "https://raw.githubusercontent.com/aansubarkah/ssa_agentic_input_sirs"
    "/master/RL32-dummy-24-bulan.xlsx"
)

# Excel column to web input field mapping: v[row_number][key].
# Columns M and N (Pasien Akhir Bulan, Jumlah Hari Perawatan) are skipped
# because the website computes them automatically.
FIELD_COLUMNS = [
    ("awal", 3),           # C  patients at start of month
    ("masuk", 4),          # D  admitted patients
    ("pindahan", 5),       # E  transferred in
    ("dipindahkan", 6),    # F  transferred out
    ("keluar_hidup", 7),   # G  discharged alive
    ("mati_l_lt48", 8),    # H  male deaths under 48 hours
    ("mati_l_ge48", 9),    # I  male deaths 48 hours or more
    ("mati_p_lt48", 10),   # J  female deaths under 48 hours
    ("mati_p_ge48", 11),   # K  female deaths 48 hours or more
    ("lama_dirawat", 12),  # L  total days of care
    ("vvip", 15),          # O  bed days class VVIP
    ("vip", 16),           # P  bed days class VIP
    ("k1", 17),            # Q  bed days class I
    ("k2", 18),            # R  bed days class II
    ("k3", 19),            # S  bed days class III
    ("khusus", 20),        # T  bed days special class
    ("tt", 21),            # U  allocated beds at start of month
]
DATA_ROW_START = 5   # first Excel row, jenis pelayanan No 1
DATA_ROW_END = 40    # last Excel row, No 36; the TOTAL row is skipped


def normalize_name(text):
    """Normalize a jenis pelayanan name so Excel and web labels match."""
    return re.sub(r"\s+", " ", str(text or "").strip().lower())


def download_sample_excel(destination):
    """Download the sample Excel file from this repository."""
    urllib.request.urlretrieve(RAW_EXCEL_URL, destination)


def read_excel(path):
    """Read every monthly sheet that contains data.

    Uses pandas with the openpyxl engine so each sheet is parsed once
    in a single pass (random access in openpyxl read_only mode is
    quadratic and takes minutes on the sample file). Returns a time
    sorted list of dicts: sheet, year, month, and rows (list of jenis
    pelayanan entries with values). Rows whose values are all zero are
    skipped because they do not need to be entered.
    """
    import pandas as pd

    book = pd.read_excel(path, sheet_name=None, header=None,
                         engine="openpyxl")
    result = []
    for name, frame in book.items():
        match = re.fullmatch(r"(\d{4})-(\d{2})", str(name).strip())
        if not match:
            continue  # skip the Info sheet and other non monthly sheets
        year, month = int(match.group(1)), int(match.group(2))
        data_rows = []
        for offset in range(DATA_ROW_START, DATA_ROW_END + 1):
            row = frame.iloc[offset - 1]
            values = {}
            for key, column in FIELD_COLUMNS:
                raw = row.iloc[column - 1]
                if (raw is None or pd.isna(raw)
                        or (isinstance(raw, str) and not raw.strip())):
                    number = 0
                else:
                    try:
                        number = int(float(raw))
                    except (TypeError, ValueError):
                        number = 0
                values[key] = max(number, 0)
            label = row.iloc[1]
            if any(values.values()):
                data_rows.append({
                    "no": offset - DATA_ROW_START + 1,
                    "name": normalize_name(
                        None if pd.isna(label) else label),
                    "values": values,
                })
        if data_rows:
            result.append({
                "sheet": str(name).strip(),
                "year": year,
                "month": month,
                "rows": data_rows,
            })
    result.sort(key=lambda item: (item["year"], item["month"]))
    return result


def validate_sheets(sheets):
    """Check the web rules before a browser is opened.

    The sandbox computes akhir and hari_rawat per row and refuses to
    save when akhir is negative or hari_rawat is below lama_dirawat.
    Returns a list of Indonesian problem messages, empty when fine.
    """
    problems = []
    for sheet in sheets:
        for row in sheet["rows"]:
            v = row["values"]
            akhir = (v["awal"] + v["masuk"] + v["pindahan"]
                     - (v["keluar_hidup"] + v["mati_l_lt48"]
                        + v["mati_l_ge48"] + v["mati_p_lt48"]
                        + v["mati_p_ge48"] + v["dipindahkan"]))
            hari = (v["vvip"] + v["vip"] + v["k1"] + v["k2"] + v["k3"]
                    + v["khusus"])
            label = "%s baris %d (%s)" % (sheet["sheet"], row["no"],
                                          row["name"])
            if akhir < 0:
                problems.append(label + ": pasien keluar + dipindahkan "
                                "melebihi pasien awal bulan + masuk + "
                                "pindahan")
            if hari < v["lama_dirawat"]:
                problems.append(label + ": jumlah hari perawatan kurang "
                                "dari jumlah lama dirawat")
    return problems


def create_driver():
    """Chrome in headed mode. Selenium Manager downloads the driver."""
    from selenium import webdriver
    return webdriver.Chrome()


def login(driver, username, password, timeout=20):
    """Log in to the sandbox. Raises on timeout when credentials fail."""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait

    if "/beranda" in driver.current_url:
        return
    driver.get(BASE_URL + "/")
    wait = WebDriverWait(driver, timeout)
    wait.until(lambda d: d.find_element(By.ID, "username").is_displayed())
    driver.find_element(By.ID, "username").clear()
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    wait.until(lambda d: "/beranda" in d.current_url)


def available_years(driver):
    """List of years selectable on the RL 3.2 add form."""
    from selenium.webdriver.common.by import By

    driver.get(BASE_URL + "/rl32/tambah")
    options = driver.find_elements(By.CSS_SELECTOR, "select#tahun option")
    return sorted(option.get_attribute("value") for option in options)


def web_row_map(driver):
    """Map jenis pelayanan name to its web input row number (1 based)."""
    from selenium.webdriver.common.by import By

    mapping = {}
    checkboxes = driver.find_elements(By.CSS_SELECTOR, "input.cek-baris")
    for index, checkbox in enumerate(checkboxes, start=1):
        label = checkbox.get_attribute("aria-label") or ""
        name = normalize_name(label.replace("Isi baris", "", 1))
        mapping[name] = index
    return mapping


def select_value(driver, select_id, value):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select
    Select(driver.find_element(By.ID, select_id)).select_by_value(str(value))


def read_alert(driver):
    from selenium.webdriver.common.by import By
    elements = driver.find_elements(By.CSS_SELECTOR, ".alert")
    return elements[0].text.strip() if elements else ""


def scroll_and_click(driver, element):
    """Scroll an element into view then click, so it stays visible."""
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", element)
    try:
        element.click()
    except Exception:
        driver.execute_script("arguments[0].click();", element)


def input_sheet(driver, year, month, data_rows, log=print):
    """Enter one monthly RL 3.2 sheet.

    There is no delay between input boxes. When the period already exists
    on the website the edit page is used automatically, otherwise the add
    page is used. Returns True when saved.
    """
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait

    driver.get(BASE_URL + "/rl32?tahun=%d&bulan=%d" % (year, month))
    edit_links = driver.find_elements(
        By.CSS_SELECTOR, 'a[href*="/rl32/ubah/"]')
    if edit_links:
        edit_links[0].click()
        mode = "ubah"
    else:
        driver.get(BASE_URL + "/rl32/tambah")
        select_value(driver, "bulan", month)
        select_value(driver, "tahun", year)
        mode = "tambah"

    mapping = web_row_map(driver)
    for row in data_rows:
        index = mapping.get(row["name"])
        if index is None:
            log("    Lewati, tidak ada barisnya di web: " + row["name"])
            continue
        checkbox = driver.find_elements(
            By.CSS_SELECTOR, "input.cek-baris")[index - 1]
        if not checkbox.is_selected():
            scroll_and_click(driver, checkbox)
        for key, _column in FIELD_COLUMNS:
            field = driver.find_element(
                By.NAME, "v[%d][%s]" % (index, key))
            field.clear()
            field.send_keys(str(row["values"][key]))

    save_button = driver.find_element(
        By.XPATH, "//main//button[normalize-space()='Simpan']")
    scroll_and_click(driver, save_button)

    def settled(d):
        url = d.current_url
        left_form = ("/rl32/tambah" not in url) and ("/rl32/ubah/" not in url)
        on_form = bool(d.find_elements(
            By.XPATH, "//main//button[normalize-space()='Simpan']"))
        has_alert = bool(d.find_elements(By.CSS_SELECTOR, ".alert"))
        return (left_form and not on_form) or (on_form and has_alert)

    try:
        WebDriverWait(driver, 30).until(settled)
    except Exception:
        pass  # read whatever state is available below
    message = " ".join(
        element.text.strip()
        for element in driver.find_elements(By.CSS_SELECTOR, ".alert")
    ).strip()
    saved = ("berhasil" in message.lower()) or (not message and settled(driver))
    if saved:
        log("    Tersimpan (mode %s). Pesan web: %s"
            % (mode, message or "halaman daftar terbuka"))
        return True
    log("    GAGAL. Pesan web: %s" % (message or "tidak ada pesan"))
    return False
