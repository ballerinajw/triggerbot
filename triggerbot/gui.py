# vibecoded project, i take no credit for it

import tkinter as tk
from tkinter import messagebox
import threading
from bot import DMFilter
from logger import LOG_PATH
from config import load_config, save_config
from startup import enable_startup, disable_startup, is_enabled

LEVEL_DESCRIPTIONS = [
    (1, "Essentiel",     "Violence directe, suicide, pédophilie.\nLaisse passer les insultes sans contexte grave."),
    (2, "Standard",      "Ajoute insultes graves en combinaison,\nTCA, drogues, remise en question des diagnostics."),
    (3, "Intransigeant", "Bloque tout contenu dégradant,\ny compris les insultes seules."),
]

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Discord DM Filter")
        self.resizable(False, False)
        self.configure(bg="#1e1e2e")

        self.token_var    = tk.StringVar()
        self.level_var    = tk.IntVar(value=2)
        self.startup_var  = tk.BooleanVar(value=is_enabled())
        self.show_token   = False
        self.running      = False
        self.block_count  = 0
        self.filter       = None
        self.tray         = None

        # Charger config sauvegardée
        cfg = load_config()
        self.token_var.set(cfg.get("token", ""))
        self.level_var.set(cfg.get("level", 2))

        self._build()

        # Démarrer auto si token déjà enregistré
        if cfg.get("token"):
            self.after(500, self._start)

    # ── Construction UI ─────────────────────────────────────────────────────

    def _build(self):
        BG, CARD        = "#1e1e2e", "#2a2a3e"
        TXT, MUTED      = "#e0e0f0", "#888899"
        SUCCESS, DANGER = "#1D9E75", "#e24b4a"
        WARN, ACC       = "#BA7517", "#7F77DD"
        PAD = 18
        self.c = dict(bg=BG, card=CARD, txt=TXT, muted=MUTED,
                      success=SUCCESS, danger=DANGER, warn=WARN, acc=ACC)

        tk.Label(self, text="Discord DM Filter", bg=BG, fg=TXT,
                 font=("Segoe UI", 18, "bold")).pack(pady=(PAD, 2))
        tk.Label(self, text="Bloque automatiquement les DMs malveillants",
                 bg=BG, fg=MUTED, font=("Segoe UI", 10)).pack(pady=(0, PAD))

        self._card_token(CARD, TXT, MUTED, WARN, PAD)
        self._card_level(CARD, TXT, MUTED, PAD)
        self._card_options(CARD, TXT, MUTED, PAD)
        self._bottom(BG, MUTED, SUCCESS, DANGER, ACC, PAD)

    def _card_token(self, CARD, TXT, MUTED, WARN, PAD):
        c = tk.Frame(self, bg=CARD, padx=PAD, pady=PAD)
        c.pack(fill="x", padx=PAD, pady=(0, 10))

        tk.Label(c, text="Token Discord", bg=CARD, fg=TXT,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w")
        tk.Label(c, text="Paramètres Discord → Avancé → Copier mon token\n"
                         "ou colle cette commande dans la console (F12) de Discord web :",
                 bg=CARD, fg=MUTED, font=("Segoe UI", 9), justify="left").pack(anchor="w", pady=(2, 6))

        code = tk.Frame(c, bg="#13131f", padx=10, pady=8)
        code.pack(fill="x", pady=(0, 8))
        tk.Label(code,
                 text="(webpackChunkdiscord_app.push([[''],{},e=>{m=[];\nfor(let c in e.c)m.push(e.c[c])}]),m)\n"
                      ".find(m=>m?.exports?.default?.getToken!==void 0)\n.exports.default.getToken()",
                 bg="#13131f", fg="#1D9E75", font=("Courier New", 8), justify="left").pack(anchor="w")

        row = tk.Frame(c, bg=CARD)
        row.pack(fill="x")
        self.token_entry = tk.Entry(row, textvariable=self.token_var, show="•",
                                    bg="#13131f", fg=TXT, insertbackground=TXT,
                                    relief="flat", font=("Segoe UI", 10), width=50)
        self.token_entry.pack(side="left", ipady=6, padx=(0, 8))
        self.show_btn = tk.Button(row, text="Afficher", bg=CARD, fg=MUTED,
                                  relief="flat", font=("Segoe UI", 9),
                                  cursor="hand2", command=self._toggle_token)
        self.show_btn.pack(side="left")

        tk.Label(c, text="⚠  Ne partage jamais ton token — accès total à ton compte.",
                 bg=CARD, fg=WARN, font=("Segoe UI", 9)).pack(anchor="w", pady=(8, 0))

    def _card_level(self, CARD, TXT, MUTED, PAD):
        c = tk.Frame(self, bg=CARD, padx=PAD, pady=PAD)
        c.pack(fill="x", padx=PAD, pady=(0, 10))

        tk.Label(c, text="Niveau de protection", bg=CARD, fg=TXT,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 8))

        for val, label, desc in LEVEL_DESCRIPTIONS:
            f = tk.Frame(c, bg=CARD)
            f.pack(fill="x", pady=3)
            tk.Radiobutton(f, variable=self.level_var, value=val,
                           bg=CARD, fg=TXT, selectcolor="#13131f",
                           activebackground=CARD, activeforeground=TXT,
                           font=("Segoe UI", 10, "bold"),
                           text=f"Niveau {val} — {label}").pack(anchor="w")
            tk.Label(f, text=desc, bg=CARD, fg=MUTED,
                     font=("Segoe UI", 9), justify="left").pack(anchor="w", padx=(24, 0))

    def _card_options(self, CARD, TXT, MUTED, PAD):
        c = tk.Frame(self, bg=CARD, padx=PAD, pady=PAD)
        c.pack(fill="x", padx=PAD, pady=(0, 10))

        tk.Label(c, text="Options", bg=CARD, fg=TXT,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 8))

        tk.Checkbutton(c, text="Lancer au démarrage de l'ordinateur",
                       variable=self.startup_var,
                       bg=CARD, fg=TXT, selectcolor="#13131f",
                       activebackground=CARD, activeforeground=TXT,
                       font=("Segoe UI", 10),
                       command=self._toggle_startup).pack(anchor="w")
        tk.Label(c, text="Fermer la fenêtre réduit le programme dans la barre système.",
                 bg=CARD, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", padx=(24, 0))

    def _bottom(self, BG, MUTED, SUCCESS, DANGER, ACC, PAD):
        frame = tk.Frame(self, bg=BG)
        frame.pack(pady=12)

        self.start_btn = tk.Button(frame, text="▶  Démarrer le filtre",
                                   bg=SUCCESS, fg="white", relief="flat",
                                   font=("Segoe UI", 11, "bold"),
                                   padx=24, pady=10, cursor="hand2",
                                   command=self._toggle_bot)
        self.start_btn.pack(pady=(0, 8))

        stats = tk.Frame(frame, bg=BG)
        stats.pack()

        self.status_var = tk.StringVar(value="⬤  Inactif")
        self.status_lbl = tk.Label(stats, textvariable=self.status_var,
                                   bg=BG, fg=MUTED, font=("Segoe UI", 9))
        self.status_lbl.pack(side="left", padx=(0, 16))

        self.count_var = tk.StringVar(value="0 message(s) bloqué(s)")
        tk.Label(stats, textvariable=self.count_var,
                 bg=BG, fg=MUTED, font=("Segoe UI", 9)).pack(side="left")

        log_frame = tk.Frame(self, bg=BG)
        log_frame.pack(pady=(0, PAD))
        tk.Label(log_frame, text="Logs enregistrés dans :",
                 bg=BG, fg=MUTED, font=("Segoe UI", 8)).pack()
        tk.Label(log_frame, text=LOG_PATH, bg=BG, fg=ACC,
                 font=("Segoe UI", 8)).pack()

    # ── Actions ─────────────────────────────────────────────────────────────

    def _toggle_token(self):
        self.show_token = not self.show_token
        self.token_entry.config(show="" if self.show_token else "•")
        self.show_btn.config(text="Masquer" if self.show_token else "Afficher")

    def _toggle_startup(self):
        if self.startup_var.get():
            enable_startup()
        else:
            disable_startup()

    def _toggle_bot(self):
        if not self.running:
            self._start()
        else:
            self._stop()

    def _start(self):
        token = self.token_var.get().strip()
        if not token:
            messagebox.showerror("Erreur", "Entre ton token Discord.")
            return
        save_config(token, self.level_var.get())
        self.running = True
        self.start_btn.config(text="⏹  Arrêter le filtre", bg=self.c["danger"])
        self._set_status("⬤  Connexion...", self.c["warn"])

        self.filter = DMFilter(
            token=token,
            level=self.level_var.get(),
            on_ready_cb=lambda u: self.after(0, self._set_status, f"⬤  Actif — {u}", self.c["success"]),
            on_block_cb=lambda: self.after(0, self._increment_count),
            on_error_cb=lambda e: self.after(0, self._on_error, e),
        )
        threading.Thread(target=self.filter.start, daemon=True).start()

    def _stop(self):
        self.running = False
        if self.filter:
            self.filter.stop()
        self.start_btn.config(text="▶  Démarrer le filtre", bg=self.c["success"])
        self._set_status("⬤  Inactif", self.c["muted"])

    def _increment_count(self):
        self.block_count += 1
        self.count_var.set(f"{self.block_count} message(s) bloqué(s)")

    def _on_error(self, msg):
        messagebox.showerror("Erreur de connexion", msg)
        self._stop()

    def _set_status(self, text, color):
        self.status_var.set(text)
        self.status_lbl.config(fg=color)

    def set_tray(self, tray):
        self.tray = tray

    def hide_to_tray(self):
        self.withdraw()

    def show_from_tray(self):
        self.deiconify()
        self.lift()

    def on_close(self):
        """Fermer = réduire dans le tray si disponible, sinon quitter."""
        try:
            import pystray
            self.hide_to_tray()
        except ImportError:
            self._quit()

    def _quit(self):
        if self.running:
            self._stop()
        if self.tray:
            self.tray.stop()
        self.destroy()
