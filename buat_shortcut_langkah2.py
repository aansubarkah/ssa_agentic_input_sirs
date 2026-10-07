"""Step 2: create a desktop shortcut for the step 2 script.

Usage:
    python buat_shortcut_langkah2.py [target_script.py]

Without an argument the shortcut points to input_sirs_langkah2.py (0.05
second delay per input box). After step 3, run it again with the argument
gui_sirs_langkah3.py to repoint the shortcut to the GUI. The shortcut uses
a web icon (globe) from an open source icon set, stored in the assets
folder, and is created for the operating system of the user.
"""

import os
import platform
import subprocess
import sys

SHORTCUT_NAME = "Input SIRS RL32"
ICON_URLS = [
    "https://cdn.jsdelivr.net/gh/hfg-gmuend/openmoji@15.0.0/color/618x618/1F310.png",
    "https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.1.0/assets/72x72/1f310.png",
    "https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f310.png",
]


def download_icon(png_path):
    import urllib.request
    for url in ICON_URLS:
        try:
            urllib.request.urlretrieve(url, png_path)
            print("Ikon web terunduh dari:", url)
            return True
        except Exception:
            continue
    return False


def draw_local_globe(png_path):
    """Fallback when the download fails: draw a simple globe."""
    from PIL import Image, ImageDraw
    image = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    white = (255, 255, 255, 255)
    draw.ellipse([12, 12, 244, 244], fill=(28, 100, 178, 255),
                 outline=white, width=8)
    draw.line([128, 12, 128, 244], fill=white, width=5)
    draw.ellipse([46, 12, 210, 244], outline=white, width=5)
    draw.ellipse([12, 46, 244, 210], outline=white, width=5)
    image.save(png_path)
    print("Unduhan gagal, ikon bola dibuat lokal.")


def prepare_icon(assets_dir):
    from PIL import Image
    os.makedirs(assets_dir, exist_ok=True)
    png_path = os.path.join(assets_dir, "ikon_web.png")
    if not os.path.exists(png_path):
        if not download_icon(png_path):
            draw_local_globe(png_path)
    image = Image.open(png_path).convert("RGBA")
    resized = image.resize((256, 256), Image.LANCZOS)
    ico_path = os.path.join(assets_dir, "ikon_web.ico")
    resized.save(ico_path, sizes=[(256, 256), (128, 128), (64, 64),
                                  (48, 48), (32, 32), (16, 16)])
    icns_path = os.path.join(assets_dir, "ikon_web.icns")
    try:
        resized.save(icns_path)
    except Exception:
        icns_path = None  # older Pillow may not support writing icns
    return png_path, ico_path, icns_path


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

    icon_png, icon_ico, icon_icns = prepare_icon(
        os.path.join(folder, "assets"))
    system = platform.system()
    if system == "Windows":
        result = create_windows_shortcut(folder, target_script, icon_ico)
    elif system == "Darwin":
        result = create_macos_shortcut(folder, target_script, icon_icns)
    elif system == "Linux":
        result = create_linux_shortcut(folder, target_script, icon_png)
    else:
        print("Sistem operasi tidak dikenal:", system)
        sys.exit(1)

    print("Shortcut dibuat:", result)
    print("Shortcut menjalankan:", target_script)


if __name__ == "__main__":
    main()
