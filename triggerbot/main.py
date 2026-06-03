# vibecoded project, i take no credit for it

from gui import App
from tray import TrayIcon, TRAY_AVAILABLE

if __name__ == "__main__":
    app = App()

    if TRAY_AVAILABLE:
        tray = TrayIcon(
            on_show=lambda: app.after(0, app.show_from_tray),
            on_quit=lambda: app.after(0, app._quit),
        )
        app.set_tray(tray)
        tray.start()

    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
