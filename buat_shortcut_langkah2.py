"""Step 2: create a desktop shortcut for the step 2 script.

Usage:
    python buat_shortcut_langkah2.py [target_script.py]

Without an argument the shortcut points to input_sirs_langkah2.py (0.05
second delay per input box). After step 3, run it again with the argument
gui_sirs_langkah3.py to repoint the shortcut to the GUI. The icon comes
from favicon.ico in the repository root: Windows uses it directly, while
Linux and macOS get one time converted copies in the assets folder.
"""

import os
import platform
import subprocess
import sys

SHORTCUT_NAME = "Input SIRS RL32"
ICON_FILE = "favicon.ico"


def icon_ico_path(folder):
    """Return the favicon.ico path, exiting with a message when missing."""
    path = os.path.join(folder, ICON_FILE)
    if not os.path.exists(path):
        print("File ikon tidak ditemukan:", path)
        sys.exit(1)
    return path


def icon_png_path(folder):
    """Convert favicon.ico to a PNG in assets once, for Linux."""
    from PIL import Image
    assets_dir = os.path.join(folder, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    png_path = os.path.join(assets_dir, "ikon_aplikasi.png")
    if not os.path.exists(png_path):
        image = Image.open(icon_ico_path(folder)).convert("RGBA")
        image.save(png_path)
    return png_path


def icon_icns_path(folder):
    """Convert the PNG to ICNS in assets once, for macOS."""
    from PIL import Image
    png_path = icon_png_path(folder)
    icns_path = os.path.join(folder, "assets", "ikon_aplikasi.icns")
    if not os.path.exists(icns_path):
        try:
            Image.open(png_path).save(icns_path)
        except Exception:
            return None  # older Pillow may not support writing icns
    return icns_path


def escape_single_quotes(text):
    """Make a value safe inside a single quoted PowerShell string."""
    return str(text).replace("'", "''")


def windows_desktop():
    output = subprocess.check_output(
        ["powershell", "-NoProfile", "-Command",
         "[Environment]::GetFolderPath('Desktop')"],
        text=True,
    ).strip()
    return output


def create_windows_shortcut(folder, target_script, ico_path):
    lnk_path = os.path.join(windows_desktop(), SHORTCUT_NAME + ".lnk")
    powershell = (
        "$s = (New-Object -ComObject WScript.Shell).CreateShortcut('%s'); "
        "$s.TargetPath = '%s'; "
        "$s.Arguments = '%s'; "
        "$s.WorkingDirectory = '%s'; "
        "$s.IconLocation = '%s'; "
        "$s.Save()" % (
            escape_single_quotes(lnk_path),
            escape_single_quotes(sys.executable),
            escape_single_quotes(target_script),
            escape_single_quotes(folder),
            escape_single_quotes(ico_path),
        )
    )
    subprocess.check_call(["powershell", "-NoProfile", "-Command", powershell])
    return lnk_path


def create_macos_shortcut(folder, target_script, icns_path):
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    command_path = os.path.join(desktop, "Input-SIRS-RL32.command")
    content = "#!/bin/bash\ncd '%s'\nexec '%s' '%s'\n" % (
        folder, sys.executable, target_script)
    with open(command_path, "w", newline="\n") as handle:
        handle.write(content)
    os.chmod(command_path, 0o755)
    if icns_path:
        print("Catatan: ikon .command mengikuti tema sistem. Berkas ikon:",
              icns_path)
    return command_path


def create_linux_shortcut(folder, target_script, png_path):
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    desktop_entry = os.path.join(desktop, "input-sirs-rl32.desktop")
    content = (
        "[Desktop Entry]\n"
        "Type=Application\n"
        "Name=%s\n"
        "Exec=%s %s\n"
        "Path=%s\n"
        "Icon=%s\n"
        "Terminal=true\n"
        "Categories=Utility;\n" % (
            SHORTCUT_NAME, sys.executable, target_script, folder, png_path)
    )
    destinations = [
        desktop_entry,
        os.path.join(os.path.expanduser("~"),
                     ".local/share/applications",
                     "input-sirs-rl32.desktop"),
    ]
    for path in destinations:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", newline="\n") as handle:
            handle.write(content)
        os.chmod(path, 0o755)
    return desktop_entry


def main():
    folder = os.path.dirname(os.path.abspath(__file__))
    target_name = sys.argv[1] if len(sys.argv) > 1 else "input_sirs_langkah2.py"
    target_script = os.path.join(folder, target_name)
    if not os.path.exists(target_script):
        print("Script target tidak ditemukan:", target_script)
        sys.exit(1)

    system = platform.system()
    if system == "Windows":
        result = create_windows_shortcut(
            folder, target_script, icon_ico_path(folder))
    elif system == "Darwin":
        result = create_macos_shortcut(
            folder, target_script, icon_icns_path(folder))
    elif system == "Linux":
        result = create_linux_shortcut(
            folder, target_script, icon_png_path(folder))
    else:
        print("Sistem operasi tidak dikenal:", system)
        sys.exit(1)

    print("Shortcut dibuat:", result)
    print("Shortcut menjalankan:", target_script)


if __name__ == "__main__":
    main()
