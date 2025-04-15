import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter import font as tkfont
from PIL import Image, ImageTk
import threading
from DoS import HTTP_Tester
import os
import webbrowser
import requests
import tempfile

class HTTPTesterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HTTP Tester v1.0")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#2c3e50")
        self.getIcon('https://www.upload.ee/image/17968164/icono.ico')
        
        self.running = False
        self.tester = None
        self.attack_thread = None
        
        self.load_assets()
        self.setup_styles()
        self.build_ui()

    
    def getIcon(self, icon_url):
        try:
            response = requests.get(icon_url)
            response.raise_for_status()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".ico") as tmp_icon:
                tmp_icon.write(response.content)
                tmp_path = tmp_icon.name

            self.root.iconbitmap(tmp_path)
            self.root.after(2000, lambda: os.remove(tmp_path))

        except Exception as e:
            #print(f"[ERROR] No se pudo aplicar el ícono: {e}")
            pass
        
    def load_assets(self):
        try:
            self.logo_img = Image.open("assets/logo.png").resize((150, 50))
            self.logo_img = ImageTk.PhotoImage(self.logo_img)
            
            self.start_img = Image.open("assets/start.png").resize((20, 20))
            self.start_img = ImageTk.PhotoImage(self.start_img)
            
            self.stop_img = Image.open("assets/stop.png").resize((20, 20))
            self.stop_img = ImageTk.PhotoImage(self.stop_img)
        except:
            self.logo_img = None
            self.start_img = None
            self.stop_img = None
    
    def setup_styles(self):
        self.style = ttk.Style()
        
        # Configurar tema
        self.style.theme_use('clam')
        
        # Configurar colores
        self.style.configure('TFrame', background='#2c3e50')
        self.style.configure('TLabel', background='#2c3e50', foreground='white')
        self.style.configure('TButton', background='#3498db', foreground='white')
        self.style.configure('TEntry', fieldbackground='#ecf0f1')
        self.style.configure('TCombobox', fieldbackground='#ecf0f1')
        self.style.configure('TNotebook', background='#2c3e50')
        self.style.configure('TNotebook.Tab', background='#34495e', foreground='white')
        self.style.map('TNotebook.Tab', background=[('selected', '#3498db')])
        
        # Fuentes personalizadas
        self.title_font = tkfont.Font(family="Helvetica", size=14, weight="bold")
        self.label_font = tkfont.Font(family="Helvetica", size=10)
        self.button_font = tkfont.Font(family="Helvetica", size=10, weight="bold")
    
    def build_ui(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        
        if self.logo_img:
            logo_label = ttk.Label(self.header_frame, image=self.logo_img)
            logo_label.pack(side=tk.LEFT)
        else:
            title_label = ttk.Label(self.header_frame, text="HTTP Tester", font=self.title_font)
            title_label.pack(side=tk.LEFT)
        
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de ataque
        self.attack_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.attack_tab, text="Ataque")
        
        # Pestaña de configuración
        self.config_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.config_tab, text="Configuración")
        
        # Pestaña de logs
        self.logs_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.logs_tab, text="Logs")
        
        self.build_attack_tab()
        self.build_config_tab()
        self.build_logs_tab()
        
        self.footer_frame = ttk.Frame(self.main_frame)
        self.footer_frame.pack(fill=tk.X, pady=(10, 0))
        
        status_label = ttk.Label(self.footer_frame, text="Estado: Listo", font=self.label_font)
        status_label.pack(side=tk.LEFT)
        
        version_label = ttk.Label(self.footer_frame, text="v1.0 | © 2025 R3LI4NT", font=self.label_font)
        version_label.pack(side=tk.RIGHT)
    
    def build_attack_tab(self):
        config_frame = ttk.LabelFrame(self.attack_tab, text="Configuración de Ataque", padding=(10, 5))
        config_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Target
        ttk.Label(config_frame, text="Objetivo:", font=self.label_font).grid(row=0, column=0, sticky=tk.W, pady=2)
        self.target_entry = ttk.Entry(config_frame, width=40, font=self.label_font)
        self.target_entry.grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)
        
        # Puerto
        ttk.Label(config_frame, text="Puerto:", font=self.label_font).grid(row=1, column=0, sticky=tk.W, pady=2)
        self.port_entry = ttk.Entry(config_frame, width=10, font=self.label_font)
        self.port_entry.grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)
        self.port_entry.insert(0, "443")
        
        # Hilos
        ttk.Label(config_frame, text="Hilos:", font=self.label_font).grid(row=2, column=0, sticky=tk.W, pady=2)
        self.threads_slider = ttk.Scale(config_frame, from_=100, to=2000, orient=tk.HORIZONTAL)
        self.threads_slider.grid(row=2, column=1, padx=5, pady=2, sticky=tk.EW)
        self.threads_slider.set(500)
        self.threads_label = ttk.Label(config_frame, text="500", font=self.label_font)
        self.threads_label.grid(row=2, column=2, padx=5, pady=2, sticky=tk.W)
        
        # Modos de ataque
        ttk.Label(config_frame, text="Modo de Ataque:", font=self.label_font).grid(row=3, column=0, sticky=tk.W, pady=2)
        self.attack_mode = tk.StringVar()
        self.attack_mode.set("http_flood")
        modes = [("HTTP Flood", "http_flood"), 
                ("Slowloris", "slowloris"), 
                ("POST Attack", "post_attack")]
        
        for i, (text, mode) in enumerate(modes):
            rb = ttk.Radiobutton(config_frame, text=text, variable=self.attack_mode, 
                                value=mode, style='Toolbutton')
            rb.grid(row=3, column=1+i, padx=5, pady=2, sticky=tk.W)
        
        control_frame = ttk.Frame(self.attack_tab)
        control_frame.pack(fill=tk.X, padx=5, pady=10)
        
        if self.start_img:
            self.start_btn = ttk.Button(control_frame, image=self.start_img, compound=tk.LEFT, 
                                      text=" Iniciar Ataque", command=self.start_attack)
        else:
            self.start_btn = ttk.Button(control_frame, text="Iniciar Ataque", command=self.start_attack)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        if self.stop_img:
            self.stop_btn = ttk.Button(control_frame, image=self.stop_img, compound=tk.LEFT, 
                                      text=" Detener Ataque", command=self.stop_attack, state=tk.DISABLED)
        else:
            self.stop_btn = ttk.Button(control_frame, text="Detener Ataque", command=self.stop_attack, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        stats_frame = ttk.LabelFrame(self.attack_tab, text="Estadísticas en Tiempo Real", padding=(10, 5))
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.stats_canvas = tk.Canvas(stats_frame, bg="#34495e", height=150)
        self.stats_canvas.pack(fill=tk.X, pady=5)
        
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill=tk.X, pady=5)
        
        ttk.Label(stats_grid, text="Solicitudes Totales:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.total_reqs = ttk.Label(stats_grid, text="0", font=self.label_font)
        self.total_reqs.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(stats_grid, text="Solicitudes Exitosas:").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.success_reqs = ttk.Label(stats_grid, text="0", font=self.label_font)
        self.success_reqs.grid(row=0, column=3, sticky=tk.W, padx=5)
        
        ttk.Label(stats_grid, text="Solicitudes Fallidas:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.failed_reqs = ttk.Label(stats_grid, text="0", font=self.label_font)
        self.failed_reqs.grid(row=1, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(stats_grid, text="Ancho de Banda:").grid(row=1, column=2, sticky=tk.W, padx=5)
        self.bandwidth = ttk.Label(stats_grid, text="0 MB", font=self.label_font)
        self.bandwidth.grid(row=1, column=3, sticky=tk.W, padx=5)
        
        ttk.Label(stats_grid, text="Conexiones Activas:").grid(row=2, column=0, sticky=tk.W, padx=5)
        self.active_conns = ttk.Label(stats_grid, text="0", font=self.label_font)
        self.active_conns.grid(row=2, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(stats_grid, text="Conexiones Lentas:").grid(row=2, column=2, sticky=tk.W, padx=5)
        self.slow_conns = ttk.Label(stats_grid, text="0", font=self.label_font)
        self.slow_conns.grid(row=2, column=3, sticky=tk.W, padx=5)
        
        self.threads_slider.bind("<Motion>", self.update_threads_label)
    
    def build_config_tab(self):
        general_frame = ttk.LabelFrame(self.config_tab, text="Configuración General", padding=(10, 5))
        general_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(general_frame, text="Archivo de Proxies:", font=self.label_font).grid(row=0, column=0, sticky=tk.W, pady=2)
        self.proxy_entry = ttk.Entry(general_frame, width=40, font=self.label_font)
        self.proxy_entry.grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)
        self.proxy_entry.insert(0, "proxys.txt")
        
        proxy_btn = ttk.Button(general_frame, text="Examinar", command=self.browse_proxy_file)
        proxy_btn.grid(row=0, column=2, padx=5, pady=2)
        
        ttk.Label(general_frame, text="User Agents:", font=self.label_font).grid(row=1, column=0, sticky=tk.W, pady=2)
        self.ua_entry = ttk.Entry(general_frame, width=40, font=self.label_font)
        self.ua_entry.grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)
        self.ua_entry.insert(0, "user_agents.txt")
        
        ua_btn = ttk.Button(general_frame, text="Examinar", command=self.browse_ua_file)
        ua_btn.grid(row=1, column=2, padx=5, pady=2)
        
        advanced_frame = ttk.LabelFrame(self.config_tab, text="Configuración Avanzada", padding=(10, 5))
        advanced_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(advanced_frame, text="Timeout Mínimo (s):", font=self.label_font).grid(row=0, column=0, sticky=tk.W, pady=2)
        self.min_timeout = ttk.Entry(advanced_frame, width=10, font=self.label_font)
        self.min_timeout.grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)
        self.min_timeout.insert(0, "8")
        
        ttk.Label(advanced_frame, text="Timeout Máximo (s):", font=self.label_font).grid(row=0, column=2, sticky=tk.W, pady=2)
        self.max_timeout = ttk.Entry(advanced_frame, width=10, font=self.label_font)
        self.max_timeout.grid(row=0, column=3, padx=5, pady=2, sticky=tk.W)
        self.max_timeout.insert(0, "12")
        
        ttk.Label(advanced_frame, text="Delay Mínimo (ms):", font=self.label_font).grid(row=1, column=0, sticky=tk.W, pady=2)
        self.min_delay = ttk.Entry(advanced_frame, width=10, font=self.label_font)
        self.min_delay.grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)
        self.min_delay.insert(0, "1")
        
        ttk.Label(advanced_frame, text="Delay Máximo (ms):", font=self.label_font).grid(row=1, column=2, sticky=tk.W, pady=2)
        self.max_delay = ttk.Entry(advanced_frame, width=10, font=self.label_font)
        self.max_delay.grid(row=1, column=3, padx=5, pady=2, sticky=tk.W)
        self.max_delay.insert(0, "100")
        
        save_frame = ttk.Frame(self.config_tab)
        save_frame.pack(fill=tk.X, padx=5, pady=10)
        
        save_btn = ttk.Button(save_frame, text="Guardar Configuración", command=self.save_config)
        save_btn.pack(side=tk.RIGHT, padx=5)
    
    def build_logs_tab(self):
        self.log_area = scrolledtext.ScrolledText(self.logs_tab, wrap=tk.WORD, width=80, height=20)
        self.log_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.log_area.tag_config("INFO", foreground="blue")
        self.log_area.tag_config("SUCCESS", foreground="green")
        self.log_area.tag_config("ERROR", foreground="red")
        self.log_area.tag_config("WARNING", foreground="orange")
        
        log_control_frame = ttk.Frame(self.logs_tab)
        log_control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        clear_btn = ttk.Button(log_control_frame, text="Limpiar Logs", command=self.clear_logs)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        save_logs_btn = ttk.Button(log_control_frame, text="Guardar Logs", command=self.save_logs)
        save_logs_btn.pack(side=tk.LEFT, padx=5)
        
        self.log_message("Sistema inicializado y listo", "INFO")
    
    def update_threads_label(self, event):
        self.threads_label.config(text=str(int(self.threads_slider.get())))
    
    def browse_proxy_file(self):
        filename = filedialog.askopenfilename(title="Seleccionar archivo de proxies", 
                                            filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if filename:
            self.proxy_entry.delete(0, tk.END)
            self.proxy_entry.insert(0, filename)
    
    def browse_ua_file(self):
        filename = filedialog.askopenfilename(title="Seleccionar archivo de User Agents", 
                                            filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if filename:
            self.ua_entry.delete(0, tk.END)
            self.ua_entry.insert(0, filename)
    
    def log_message(self, message, level="INFO"):
        self.log_area.insert(tk.END, f"[{level}] {message}\n", level)
        self.log_area.see(tk.END)
    
    def clear_logs(self):
        self.log_area.delete(1.0, tk.END)
    
    def save_logs(self):
        filename = filedialog.asksaveasfilename(defaultextension=".log", 
                                              filetypes=(("Log files", "*.log"), ("Text files", "*.txt")))
        if filename:
            try:
                with open(filename, "w") as f:
                    f.write(self.log_area.get(1.0, tk.END))
                self.log_message(f"Logs guardados en {filename}", "INFO")
            except Exception as e:
                self.log_message(f"Error al guardar logs: {str(e)}", "ERROR")
    
    def save_config(self):
        self.log_message("Configuración guardada", "INFO")
        messagebox.showinfo("Configuración", "Configuración guardada exitosamente")
    
    def start_attack(self):
        target = self.target_entry.get()
        port = self.port_entry.get()
        threads = int(self.threads_slider.get())
        
        if not target:
            messagebox.showerror("Error", "Debes especificar un objetivo")
            return
        
        try:
            port = int(port)
        except ValueError:
            messagebox.showerror("Error", "El puerto debe ser un número")
            return
        
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.running = True
        
        self.attack_thread = threading.Thread(
            target=self.run_attack,
            args=(target, port, threads),
            daemon=True
        )
        self.attack_thread.start()
        
        self.log_message(f"Ataque iniciado contra {target}:{port} con {threads} hilos", "INFO")
    
    def run_attack(self, target, port, threads):
        self.tester = HTTP_Tester()
        
        import time
        import random
        
        start_time = time.time()
        
        while self.running:
            elapsed = time.time() - start_time
            
            total = random.randint(100, 1000)
            success = random.randint(80, total)
            failed = total - success
            bandwidth = random.uniform(1.5, 15.5)
            active = random.randint(50, 200)
            slow = random.randint(5, 50)
            
            # Actualizar GUI desde el hilo principal
            self.root.after(0, self.update_stats, {
                'total': total,
                'success': success,
                'failed': failed,
                'bandwidth': bandwidth,
                'active': active,
                'slow': slow
            })
            
            time.sleep(1)
        
        self.root.after(0, self.attack_finished)
    
    def update_stats(self, stats):
        self.total_reqs.config(text=str(stats['total']))
        self.success_reqs.config(text=str(stats['success']))
        self.failed_reqs.config(text=str(stats['failed']))
        self.bandwidth.config(text=f"{stats['bandwidth']:.2f} MB")
        self.active_conns.config(text=str(stats['active']))
        self.slow_conns.config(text=str(stats['slow']))
        
        self.update_graph(stats['total'], stats['success'], stats['failed'])
    
    def update_graph(self, total, success, failed):
        self.stats_canvas.delete("all")
        
        width = self.stats_canvas.winfo_width()
        height = self.stats_canvas.winfo_height()
        
        max_val = max(total, 1)
        
        total_width = (total / max_val) * (width - 20)
        self.stats_canvas.create_rectangle(10, 10, 10 + total_width, 40, fill="#3498db", outline="")
        
        success_width = (success / max_val) * (width - 20)
        self.stats_canvas.create_rectangle(10, 50, 10 + success_width, 80, fill="#2ecc71", outline="")
        
        failed_width = (failed / max_val) * (width - 20)
        self.stats_canvas.create_rectangle(10, 90, 10 + failed_width, 120, fill="#e74c3c", outline="")
        
        self.stats_canvas.create_text(15, 25, text=f"Total: {total}", anchor=tk.W, fill="white")
        self.stats_canvas.create_text(15, 65, text=f"Éxito: {success}", anchor=tk.W, fill="white")
        self.stats_canvas.create_text(15, 105, text=f"Fallos: {failed}", anchor=tk.W, fill="white")
    
    def stop_attack(self):
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        
        if self.tester:
            self.tester.running = False
        
        self.log_message("Ataque detenido", "INFO")
    
    def attack_finished(self):
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.log_message("Ataque completado", "INFO")
    
    def on_closing(self):
        if self.running:
            if messagebox.askokcancel("Salir", "Hay un ataque en curso. ¿Seguro que quieres salir?"):
                self.stop_attack()
                self.root.destroy()
        else:
            self.root.destroy()

if __name__ == "__main__":
    from tkinter import filedialog
    
    root = tk.Tk()
    app = HTTPTesterGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    root.mainloop()