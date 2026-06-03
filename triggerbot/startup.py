# vibecoded project, i take no credit for it

import sys
import os

APP_NAME = "DiscordDMFilter"

def get_script_path() -> str:
    """Retourne le chemin absolu de main.py."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "main.py"))

def enable_startup():
    if sys.platform == "win32":
        _enable_windows()
    elif sys.platform == "darwin":
        _enable_mac()

def disable_startup():
    if sys.platform == "win32":
        _disable_windows()
    elif sys.platform == "darwin":
        _disable_mac()

def is_enabled() -> bool:
    if sys.platform == "win32":
        return _check_windows()
    elif sys.platform == "darwin":
        return _check_mac()
    return False

# ── Windows — registre ───────────────────────────────────────────────────────

def _reg_key():
    import winreg
    return winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0, winreg.KEY_ALL_ACCESS
    )

def _enable_windows():
    import winreg
    cmd = f'pythonw "{get_script_path()}"'
    with _reg_key() as key:
        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, cmd)

def _disable_windows():
    import winreg
    try:
        with _reg_key() as key:
            winreg.DeleteValue(key, APP_NAME)
    except FileNotFoundError:
        pass

def _check_windows() -> bool:
    import winreg
    try:
        with _reg_key() as key:
            winreg.QueryValueEx(key, APP_NAME)
            return True
    except FileNotFoundError:
        return False

# ── Mac — LaunchAgent plist ───────────────────────────────────────────────────

def _plist_path() -> str:
    return os.path.expanduser(f"~/Library/LaunchAgents/com.dmfilter.plist")

def _enable_mac():
    python = sys.executable
    script = get_script_path()
    plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.dmfilter</string>
    <key>ProgramArguments</key>
    <array>
        <string>{python}</string>
        <string>{script}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
</dict>
</plist>"""
    os.makedirs(os.path.dirname(_plist_path()), exist_ok=True)
    with open(_plist_path(), "w") as f:
        f.write(plist)
    os.system(f"launchctl load {_plist_path()}")

def _disable_mac():
    path = _plist_path()
    if os.path.exists(path):
        os.system(f"launchctl unload {path}")
        os.remove(path)

def _check_mac() -> bool:
    return os.path.exists(_plist_path())
