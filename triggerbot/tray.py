# vibecoded project, i take no credit for it

import threading
import sys

try:
    import pystray
    from PIL import Image, ImageDraw
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False

def _make_icon():
    """Génère une icône simple (cercle violet)."""
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([4, 4, 60, 60], fill="#7F77DD")
    return img

class TrayIcon:
    def __init__(self, on_show, on_quit):
        self.on_show = on_show
        self.on_quit = on_quit
        self.icon = None

    def start(self):
        if not TRAY_AVAILABLE:
            return
        menu = pystray.Menu(
            pystray.MenuItem("Afficher", lambda: self.on_show(), default=True),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quitter", lambda: self._quit()),
        )
        self.icon = pystray.Icon(
            "DMFilter",
            _make_icon(),
            "Discord DM Filter",
            menu
        )
        threading.Thread(target=self.icon.run, daemon=True).start()

    def _quit(self):
        self.on_quit()
        if self.icon:
            self.icon.stop()

    def stop(self):
        if self.icon:
            self.icon.stop()
