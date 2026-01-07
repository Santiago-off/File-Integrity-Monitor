import os
import hashlib
import json
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import ctypes
import sys
import threading
from datetime import datetime
from PIL import Image, ImageDraw
import pystray 

# --- Configuración de Rutas ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_path(filename):
    return os.path.join(BASE_DIR, filename)

# --- Configuración Estética ---
COLOR_BG = "#0f172a"
COLOR_SIDEBAR = "#1e293b"
COLOR_CARD = "#1e293b"
COLOR_ACCENT = "#38bdf8"
COLOR_TEXT = "#f8fafc"
COLOR_TEXT_DIM = "#94a3b8"
COLOR_SUCCESS = "#22c55e"
COLOR_DANGER = "#ef4444"

HISTORIAL_FILE = get_path("historial.json")
LOG_FILE = get_path("logs.json")
STATE_FILE = get_path("file_hashes.json")
WATCHED_DIRS_FILE = get_path("watched_dirs.json")
USERS_FILE = get_path("users.json")

# --- Lógica de Seguridad ---
def calculate_hash(filepath):
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except:
        return None

def load_json(filename, default=[]):
    if not os.path.exists(filename):
        with open(filename, "w") as f: json.dump(default, f)
        return default
    with open(filename, "r") as f:
        try: return json.load(f)
        except: return default

def save_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

def authenticate(username, password):
    users = load_json(USERS_FILE, [{"username": "admin", "password": "admin123", "role": "admin"}])
    for user in users:
        if user["username"] == username and user["password"] == password:
            return user["role"]
    return None

# --- Ventana de Alerta Intuitiva ---
class ModernAlert(tk.Toplevel):
    def __init__(self, master, title, message):
        super().__init__(master)
        self.overrideredirect(True)
        self.geometry("450x220")
        self.configure(bg=COLOR_SIDEBAR)
        
        x = master.winfo_x() + (master.winfo_width() // 2) - 225
        y = master.winfo_y() + (master.winfo_height() // 2) - 110
        self.geometry(f"+{x}+{y}")

        main_frame = tk.Frame(self, bg=COLOR_SIDEBAR, highlightthickness=2, highlightbackground=COLOR_ACCENT)
        main_frame.pack(fill="both", expand=True)

        tk.Label(main_frame, text="⚠️ ALERTA DE SEGURIDAD", font=("Arial", 11, "bold"), bg=COLOR_SIDEBAR, fg=COLOR_ACCENT).pack(pady=(25, 10))
        tk.Label(main_frame, text=message, font=("Segoe UI", 10), bg=COLOR_SIDEBAR, fg=COLOR_TEXT, justify="center").pack(pady=10, padx=20)
        
        tk.Button(main_frame, text="ENTENDIDO", command=self.destroy, bg=COLOR_ACCENT, fg=COLOR_BG, 
                  font=("Arial", 9, "bold"), relief="flat", padx=30, pady=8, cursor="hand2").pack(pady=15)

# --- Ventana de Login ---
class ModernLogin:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FIM - Acceso")
        self.root.geometry("350x450")
        self.root.configure(bg=COLOR_BG)
        self.root.resizable(False, False)
        
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - 175
        y = (self.root.winfo_screenheight() // 2) - 225
        self.root.geometry(f'+{x}+{y}')

        self.auth_data = None

        tk.Label(self.root, text="🛡️", font=("Arial", 50), bg=COLOR_BG, fg=COLOR_ACCENT).pack(pady=(40, 10))
        tk.Label(self.root, text="SECURITY MONITOR", font=("Impact", 20), bg=COLOR_BG, fg=COLOR_TEXT).pack()
        
        tk.Label(self.root, text="Usuario", bg=COLOR_BG, fg=COLOR_TEXT_DIM, font=("Arial", 9, "bold")).pack(anchor="w", padx=50, pady=(30,0))
        self.ent_user = tk.Entry(self.root, font=("Arial", 11), bg=COLOR_SIDEBAR, fg="white", relief="flat", bd=8, insertbackground="white")
        self.ent_user.pack(fill="x", padx=50, pady=5)

        tk.Label(self.root, text="Contraseña", bg=COLOR_BG, fg=COLOR_TEXT_DIM, font=("Arial", 9, "bold")).pack(anchor="w", padx=50, pady=(15, 0))
        self.ent_pass = tk.Entry(self.root, font=("Arial", 11), bg=COLOR_SIDEBAR, fg="white", relief="flat", bd=8, show="*", insertbackground="white")
        self.ent_pass.pack(fill="x", padx=50, pady=5)

        tk.Button(self.root, text="ACCEDER", command=self.try_login, 
                  bg=COLOR_ACCENT, fg=COLOR_BG, font=("Arial", 10, "bold"), 
                  relief="flat", cursor="hand2", height=2).pack(fill="x", padx=50, pady=40)

    def try_login(self):
        u, p = self.ent_user.get(), self.ent_pass.get()
        role = authenticate(u, p)
        if role:
            self.auth_data = (u, role)
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Credenciales Incorrectas")

    def run(self):
        self.root.mainloop()
        return self.auth_data

# --- Aplicación Principal ---
class FileIntegrityMonitorApp(tk.Tk):
    def __init__(self, username, role):
        super().__init__()
        self.username = username
        self.role = role
        self.title(f"FIM Console - {self.username}")
        self.geometry("1200x750") # Tamaño incrementado
        self.configure(bg=COLOR_BG)
        self.resizable(False, False)
        
        self.watched_dirs = load_json(WATCHED_DIRS_FILE)
        self.historial = load_json(HISTORIAL_FILE)
        self.state = load_json(STATE_FILE, {})
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=COLOR_CARD, foreground=COLOR_TEXT, fieldbackground=COLOR_CARD, borderwidth=0, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", background=COLOR_SIDEBAR, foreground=COLOR_ACCENT, borderwidth=0, font=("Segoe UI", 9, "bold"))

        self.protocol("WM_DELETE_WINDOW", self.hide_app)
        self.setup_ui()
        self.refresh_all()
        self.create_tray_icon()

    def setup_ui(self):
        # Sidebar
        self.sidebar = tk.Frame(self, bg=COLOR_SIDEBAR, width=180)
        self.sidebar.place(x=0, y=0, relheight=1)
        tk.Label(self.sidebar, text="SYSTEM", font=("Impact", 22), bg=COLOR_SIDEBAR, fg=COLOR_ACCENT).pack(pady=40)
        
        btn_opts = {"bg": COLOR_SIDEBAR, "fg": COLOR_TEXT, "relief": "flat", "activebackground": COLOR_ACCENT, "font": ("Arial", 10, "bold"), "anchor": "w", "padx": 25}
        tk.Button(self.sidebar, text="▣ PANEL", command=self.deiconify, **btn_opts).pack(fill="x", pady=5)
        tk.Button(self.sidebar, text="▢ OCULTAR", command=self.hide_app, **btn_opts).pack(fill="x", pady=5)
        tk.Button(self.sidebar, text="⏻ SALIR", command=self.exit_total, bg=COLOR_SIDEBAR, fg=COLOR_DANGER, relief="flat", font=("Arial", 10, "bold")).pack(side="bottom", fill="x", pady=30)

        x_start = 200
        # 1. Rutas Protegidas (Tarjeta Superior Izquierda)
        self.create_card_label(x_start, 20, 350, 280, "RUTAS PROTEGIDAS")
        self.listbox_dirs = tk.Listbox(self, bg=COLOR_CARD, fg=COLOR_TEXT, borderwidth=0, highlightthickness=1, highlightbackground=COLOR_SIDEBAR, font=("Segoe UI", 10))
        self.listbox_dirs.place(x=x_start+10, y=55, width=330, height=180)
        
        tk.Button(self, text="+ AÑADIR RUTA", command=self.add_directory, bg=COLOR_ACCENT, fg=COLOR_BG, font=("Arial", 9, "bold"), relief="flat").place(x=x_start+10, y=245, width=160)
        tk.Button(self, text="- QUITAR", command=self.remove_directory, bg=COLOR_SIDEBAR, fg=COLOR_DANGER, font=("Arial", 9, "bold"), relief="flat").place(x=x_start+180, y=245, width=160)

        # 2. Base de Datos (Tarjeta Superior Derecha - Más ancha)
        self.create_card_label(x_start+370, 20, 610, 280, "BASE DE DATOS DE INTEGRIDAD")
        self.tree_files = ttk.Treeview(self, columns=("file", "hash"), show="headings")
        self.tree_files.heading("file", text="ARCHIVO / CARPETA")
        self.tree_files.heading("hash", text="FIRMA DIGITAL SHA-256")
        self.tree_files.column("file", width=200)
        self.tree_files.column("hash", width=380)
        self.tree_files.place(x=x_start+380, y=55, width=590, height=230)

        # 3. Historial (Tarjeta Inferior Derecha - Expandida para evitar cortes)
        self.create_card_label(x_start+650, 320, 330, 340, "EVENTOS RECIENTES")
        self.listbox_historial = tk.Listbox(self, bg=COLOR_CARD, fg=COLOR_SUCCESS, borderwidth=0, font=("Consolas", 9))
        self.listbox_historial.place(x=x_start+660, y=355, width=310, height=290)

        # 4. Logs (Tarjeta Inferior Izquierda)
        self.create_card_label(x_start, 320, 630, 340, "CONSOLA DE SISTEMA")
        self.text_logs = tk.Text(self, state="disabled", bg="#000000", fg=COLOR_SUCCESS, font=("Consolas", 10), borderwidth=0)
        self.text_logs.place(x=x_start+10, y=355, width=610, height=290)

        # Botón Escaneo Inferior
        self.btn_scan = tk.Button(self, text="⚡ EJECUTAR ESCANEO DE INTEGRIDAD DEL SISTEMA", command=self.scan_all, 
                                  bg=COLOR_SUCCESS, fg=COLOR_BG, font=("Arial", 11, "bold"), relief="flat", cursor="hand2")
        self.btn_scan.place(x=x_start, y=685, width=980, height=45)

    def create_card_label(self, x, y, w, h, title):
        f = tk.Frame(self, bg=COLOR_SIDEBAR)
        f.place(x=x, y=y, width=w, height=h)
        tk.Label(f, text=title, bg=COLOR_SIDEBAR, fg=COLOR_ACCENT, font=("Arial", 9, "bold")).pack(anchor="w", padx=15, pady=8)

    def write_log(self, message):
        self.text_logs.config(state="normal")
        self.text_logs.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] > {message}\n")
        self.text_logs.see(tk.END)
        self.text_logs.config(state="disabled")

    def refresh_all(self):
        self.listbox_dirs.delete(0, tk.END)
        for d in self.watched_dirs: self.listbox_dirs.insert(tk.END, d)
        
        self.tree_files.delete(*self.tree_files.get_children())
        for f, h in self.state.items():
            nombre_archivo = os.path.basename(f)
            self.tree_files.insert("", tk.END, values=(nombre_archivo, h))
            
        self.listbox_historial.delete(0, tk.END)
        for entry in self.historial[-20:]: self.listbox_historial.insert(tk.END, entry)

    def add_directory(self):
        path = filedialog.askdirectory()
        if path:
            self.watched_dirs.append(path)
            save_json(self.watched_dirs, WATCHED_DIRS_FILE)
            self.refresh_all()

    def remove_directory(self):
        sel = self.listbox_dirs.curselection()
        if sel:
            path = self.listbox_dirs.get(sel[0])
            self.watched_dirs.remove(path)
            save_json(self.watched_dirs, WATCHED_DIRS_FILE)
            self.refresh_all()

    def scan_all(self):
        self.write_log("Iniciando análisis profundo...")
        new_state = {}
        for d in self.watched_dirs:
            if not os.path.exists(d): continue
            for root, _, files in os.walk(d):
                for f in files:
                    p = os.path.normpath(os.path.join(root, f))
                    h = calculate_hash(p)
                    if h: new_state[p] = h
        
        added = set(new_state) - set(self.state)
        removed = set(self.state) - set(new_state)
        modified = {f for f in new_state if f in self.state and new_state[f] != self.state[f]}

        if added or removed or modified:
            msg_historial = f"Cambios: {len(added)} Añadidos, {len(removed)} Eliminados, {len(modified)} Modificados"
            self.historial.append(f"ALERTA: {msg_historial}")
            save_json(self.historial, HISTORIAL_FILE)
            
            res_alerta = f"Se han detectado cambios en las zonas vigiladas:\n\n"
            res_alerta += f"• Archivos Añadidos: {len(added)}\n"
            res_alerta += f"• Archivos Eliminados: {len(removed)}\n"
            res_alerta += f"• Archivos Modificados: {len(modified)}"
            
            ModernAlert(self, "Brecha de Integridad", res_alerta)
        
        self.state = new_state
        save_json(self.state, STATE_FILE)
        self.refresh_all()
        self.write_log("Análisis finalizado.")

    def hide_app(self): self.withdraw()
    def exit_total(self):
        self.tray.stop()
        self.destroy()
        sys.exit()

    def create_tray_icon(self):
        img = Image.new('RGB', (64, 64), color=(15, 23, 42))
        d = ImageDraw.Draw(img)
        d.polygon([(32,10), (52,20), (52,40), (32,54), (12,40), (12,20)], fill=(56, 189, 248))
        menu = pystray.Menu(pystray.MenuItem('Abrir Consola', lambda: self.after(0, self.deiconify)),
                            pystray.MenuItem('Cerrar Monitor', lambda: self.after(0, self.exit_total)))
        self.tray = pystray.Icon("FIM", img, "FIM Protección Activa", menu)
        threading.Thread(target=self.tray.run, daemon=True).start()

if __name__ == "__main__":
    login_app = ModernLogin()
    user_info = login_app.run()
    if user_info:
        app = FileIntegrityMonitorApp(user_info[0], user_info[1])
        app.mainloop()