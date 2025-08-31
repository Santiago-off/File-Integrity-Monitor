import os
import hashlib
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
import ctypes
import sys
try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None
    print("Error: Pillow no está instalado. Instala con 'pip install pillow'.")

HISTORIAL_FILE = "historial.json"
LOG_FILE = "logs.json"
STATE_FILE = "file_hashes.json"
WATCHED_DIRS_FILE = "watched_dirs.json"
USERS_FILE = "users.json"

def calculate_hash(filepath):
    """Calcula el hash SHA256 de un archivo."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def scan_directory(directory):
    """Escanea todos los archivos en un directorio y calcula sus hashes."""
    file_hashes = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            path = os.path.join(root, filename)
            try:
                file_hashes[path] = calculate_hash(path)
            except Exception as e:
                print(f"Error leyendo {path}: {e}")
    return file_hashes

def save_state(state, filename="file_hashes.json"):
    """Guarda el estado de los hashes en un archivo JSON."""
    with open(filename, "w") as f:
        json.dump(state, f, indent=2)

def load_state(filename="file_hashes.json"):
    """Carga el estado de los hashes desde un archivo JSON."""
    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as f:
        return json.load(f)

def compare_states(old_state, new_state):
    """Compara dos estados y reporta cambios."""
    added = set(new_state) - set(old_state)
    removed = set(old_state) - set(new_state)
    modified = {f for f in new_state if f in old_state and new_state[f] != old_state[f]}
    return added, removed, modified

def load_json(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as f:
        return json.load(f)

def save_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

def load_users():
    if not os.path.exists(USERS_FILE):
        # Crear usuario administrador por defecto
        users = [{"username": "admin", "password": "admin123", "role": "admin"}]
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=2)
        return users
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def authenticate(username, password):
    users = load_users()
    for user in users:
        if user["username"] == username and user["password"] == password:
            return user["role"]
    return None

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def relaunch_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1)
        sys.exit()

class LoginWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Inicio de sesión")
        self.geometry("300x180")
        self.resizable(False, False)
        tk.Label(self, text="Usuario:").pack(pady=5)
        self.entry_user = tk.Entry(self)
        self.entry_user.pack()
        tk.Label(self, text="Contraseña:").pack(pady=5)
        self.entry_pass = tk.Entry(self, show="*")
        self.entry_pass.pack()
        self.btn_login = tk.Button(self, text="Entrar", command=self.try_login)
        self.btn_login.pack(pady=10)
        self.role = None
        self.username = None

    def try_login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()
        role = authenticate(username, password)
        if role:
            self.role = role
            self.username = username
            self.destroy()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

class TrayIcon(tk.Toplevel):
    def __init__(self, master, on_restore):
        super().__init__()
        self.on_restore = on_restore
        self.overrideredirect(True)
        self.geometry(f"50x50+{self.winfo_screenwidth()-60}+{self.winfo_screenheight()-70}")
        self.attributes("-topmost", True)
        # Emoticono simple (puedes cambiar por una imagen personalizada)
        self.icon_img = ImageTk.PhotoImage(Image.new("RGBA", (40, 40), (255, 255, 0, 255)))
        self.label = tk.Label(self, image=self.icon_img, cursor="hand2")
        self.label.pack()
        self.label.bind("<Button-1>", self.restore_app)

    def restore_app(self, event=None):
        self.on_restore()
        self.destroy()

class FileIntegrityMonitorApp(tk.Tk):
    def __init__(self, username, role):
        super().__init__()
        self.username = username
        self.role = role
        self.title("Monitor de Integridad de Archivos")
        self.geometry("900x600")
        self.resizable(False, False)
        self.watched_dirs = load_json(WATCHED_DIRS_FILE)
        self.historial = load_json(HISTORIAL_FILE)
        self.logs = load_json(LOG_FILE)
        self.state = load_state(STATE_FILE)
        self.session_active = True
        self.tray_icon = None
        self.create_widgets()
        self.refresh_all()
        self.style_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.attributes("-toolwindow", False)  # No minimizar

    def style_widgets(self):
        self.configure(bg="#f0f4f8")
        # ...puedes añadir más estilos visuales aquí...

    def create_widgets(self):
        # Panel lateral
        self.sidebar = tk.Frame(self, bg="#dbeafe", width=120, height=600)
        self.sidebar.place(x=0, y=0)
        btn_logout = tk.Button(self.sidebar, text="Cerrar sesión", command=self.logout, bg="#f87171", fg="white")
        btn_logout.place(x=10, y=30, width=100, height=40)
        btn_hide = tk.Button(self.sidebar, text="Ocultar programa", command=self.hide_app, bg="#38bdf8", fg="white")
        btn_hide.place(x=10, y=80, width=100, height=40)

        # Reubicar el resto de paneles
        x_offset = 130
        frame_dirs = tk.LabelFrame(self, text="Directorios Vigilados", padx=5, pady=5, bg="#e3eaf2")
        frame_dirs.place(x=x_offset, y=10, width=250, height=250)
        self.listbox_dirs = tk.Listbox(frame_dirs)
        self.listbox_dirs.pack(fill=tk.BOTH, expand=True)
        btn_add_dir = tk.Button(frame_dirs, text="Añadir Directorio", command=self.add_directory, state=tk.NORMAL if self.role == "admin" else tk.DISABLED)
        btn_add_dir.pack(fill=tk.X)
        btn_remove_dir = tk.Button(frame_dirs, text="Quitar Directorio", command=self.remove_directory, state=tk.NORMAL if self.role == "admin" else tk.DISABLED)
        btn_remove_dir.pack(fill=tk.X)

        frame_files = tk.LabelFrame(self, text="Archivos Vigilados", padx=5, pady=5)
        frame_files.place(x=x_offset+260, y=10, width=300, height=250)
        self.tree_files = ttk.Treeview(frame_files, columns=("hash"), show="headings")
        self.tree_files.heading("hash", text="Hash")
        self.tree_files.pack(fill=tk.BOTH, expand=True)

        frame_historial = tk.LabelFrame(self, text="Historial de Cambios", padx=5, pady=5)
        frame_historial.place(x=x_offset+570, y=10, width=310, height=250)
        self.listbox_historial = tk.Listbox(frame_historial)
        self.listbox_historial.pack(fill=tk.BOTH, expand=True)

        frame_logs = tk.LabelFrame(self, text="Logs", padx=5, pady=5)
        frame_logs.place(x=x_offset, y=270, width=880-x_offset, height=320)
        self.text_logs = tk.Text(frame_logs, state="disabled")
        self.text_logs.pack(fill=tk.BOTH, expand=True)

        btn_scan = tk.Button(self, text="Escanear Cambios", command=self.scan_all)
        btn_scan.place(x=x_offset, y=600-40, width=880-x_offset, height=30)
        if self.role != "admin":
            btn_scan.config(state=tk.DISABLED)

    def refresh_all(self):
        self.refresh_dirs()
        self.refresh_files()
        self.refresh_historial()
        self.refresh_logs()

    def refresh_dirs(self):
        self.listbox_dirs.delete(0, tk.END)
        for d in self.watched_dirs:
            self.listbox_dirs.insert(tk.END, d)

    def refresh_files(self):
        self.tree_files.delete(*self.tree_files.get_children())
        for d in self.watched_dirs:
            files = scan_directory(d)
            for f, h in files.items():
                self.tree_files.insert("", tk.END, values=(f, h))

    def refresh_historial(self):
        self.listbox_historial.delete(0, tk.END)
        for entry in self.historial[-20:]:
            self.listbox_historial.insert(tk.END, entry)

    def refresh_logs(self):
        self.text_logs.config(state="normal")
        self.text_logs.delete(1.0, tk.END)
        for log in self.logs[-50:]:
            self.text_logs.insert(tk.END, log + "\n")
        self.text_logs.config(state="disabled")

    def add_directory(self):
        if self.role != "admin":
            messagebox.showwarning("Permiso denegado", "Solo el administrador puede añadir directorios.")
            return
        dirpath = filedialog.askdirectory()
        if dirpath and dirpath not in self.watched_dirs:
            self.watched_dirs.append(dirpath)
            save_json(self.watched_dirs, WATCHED_DIRS_FILE)
            self.historial.append(f"[{self.username}] Directorio añadido: {dirpath}")
            save_json(self.historial, HISTORIAL_FILE)
            self.refresh_all()

    def remove_directory(self):
        if self.role != "admin":
            messagebox.showwarning("Permiso denegado", "Solo el administrador puede quitar directorios.")
            return
        selection = self.listbox_dirs.curselection()
        if selection:
            dirpath = self.listbox_dirs.get(selection[0])
            self.watched_dirs.remove(dirpath)
            save_json(self.watched_dirs, WATCHED_DIRS_FILE)
            self.historial.append(f"[{self.username}] Directorio eliminado: {dirpath}")
            save_json(self.historial, HISTORIAL_FILE)
            self.refresh_all()

    def scan_all(self):
        try:
            old_state = self.state
            new_state = {}
            for d in self.watched_dirs:
                new_state.update(scan_directory(d))
            added, removed, modified = compare_states(old_state, new_state)
            log_entry = f"[{self.username}] Escaneo realizado. Añadidos: {len(added)}, Eliminados: {len(removed)}, Modificados: {len(modified)}"
            self.logs.append(log_entry)
            for f in added:
                self.logs.append(f"[{self.username}] Archivo añadido: {f}")
            for f in removed:
                self.logs.append(f"[{self.username}] Archivo eliminado: {f}")
            for f in modified:
                self.logs.append(f"[{self.username}] Archivo modificado: {f}")
            save_json(self.logs, LOG_FILE)
            self.historial.append(log_entry)
            save_json(self.historial, HISTORIAL_FILE)
            save_state(new_state, STATE_FILE)
            self.state = new_state
            self.refresh_all()
            messagebox.showinfo("Escanear", log_entry)
        except Exception as e:
            messagebox.showerror("Error", f"Error durante el escaneo: {e}")

    def hide_app(self):
        self.session_active = False
        self.withdraw()
        self.logout()
        self.tray_icon = TrayIcon(self, self.restore_app)

    def restore_app(self):
        # Solicita credenciales antes de mostrar
        username = simpledialog.askstring("Restaurar", "Usuario administrador:")
        password = simpledialog.askstring("Restaurar", "Contraseña:", show="*")
        role = authenticate(username, password)
        if role == "admin":
            self.session_active = True
            self.deiconify()
            self.tray_icon = None
            self.attributes("-toolwindow", False)  # No minimizar
        else:
            messagebox.showerror("Permiso denegado", "Credenciales incorrectas. No se puede restaurar el programa.")

    def logout(self):
        self.session_active = False
        messagebox.showinfo("Cerrar sesión", "Sesión cerrada. Debe iniciar sesión nuevamente.")
        self.withdraw()
        self.tray_icon = TrayIcon(self, self.restore_app)

    def on_close(self):
        # Solicita credenciales de administrador antes de cerrar
        username = simpledialog.askstring("Cerrar", "Usuario administrador:")
        password = simpledialog.askstring("Cerrar", "Contraseña:", show="*")
        role = authenticate(username, password)
        if role == "admin":
            self.destroy()
        else:
            messagebox.showerror("Permiso denegado", "Credenciales incorrectas. No se puede cerrar el programa.")

if __name__ == "__main__":
    # Ejecutar como administrador
    relaunch_as_admin()
    # Ocultar consola: ejecuta con pythonw.exe en vez de python.exe
    root = tk.Tk()
    root.withdraw()
    login = LoginWindow(root)
    root.wait_window(login)
    if login.role:
        app = FileIntegrityMonitorApp(login.username, login.role)
        app.mainloop()
    else:
        messagebox.showinfo("Salir", "No se inició sesión correctamente.")
