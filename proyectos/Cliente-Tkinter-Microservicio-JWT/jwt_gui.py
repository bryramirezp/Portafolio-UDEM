import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
import json
import os
import threading
import time
from datetime import datetime

# Constants
DEFAULT_IP = 'localhost'
DEFAULT_PORT = '5000'
HEALTH_CHECK_INTERVAL = 5
REQUEST_TIMEOUT = 10
HEALTH_TIMEOUT = 5
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

class JWTGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("JWT Microservice GUI")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        # Configuración local
        self.config_file = "jwt_gui_config.json"
        self.config = self.load_config()

        # Variables de estado
        self.access_token = self.config.get('access_token', '')
        self.refresh_token_value = self.config.get('refresh_token', '')
        self.health_status = 'unknown'  # unknown, checking, healthy, unhealthy

        # Componentes de la GUI
        self.setup_gui()

        # Log de inicialización
        self.log_message("Configuración cargada correctamente")

        # Iniciar verificación de salud periódica cada 5 segundos
        self.start_health_check()

    def load_config(self):
        """Cargar configuración desde archivo JSON"""
        default_config = {
            'ip': DEFAULT_IP,
            'port': DEFAULT_PORT,
            'endpoints': {
                'register': '/register',
                'login': '/login',
                'refresh': '/refresh',
                'logout': '/logout',
                'protected': '/protected',
                'health': '/health',
                'users': '/users',
                'delete_user': '/users/'
            },
            'access_token': '',
            'refresh_token': ''
        }

        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                # Ensure loaded_config is a dict
                if not isinstance(loaded_config, dict):
                    loaded_config = {}
                # Merge loaded config with defaults to add missing keys
                merged_config = default_config.copy()
                merged_config.update(loaded_config)
                # Ensure endpoints dict exists and has all keys
                if 'endpoints' not in merged_config:
                    merged_config['endpoints'] = default_config['endpoints'].copy()
                else:
                    merged_config['endpoints'] = default_config['endpoints'].copy()
                    if isinstance(loaded_config.get('endpoints'), dict):
                        merged_config['endpoints'].update(loaded_config['endpoints'])
                return merged_config
            except Exception as e:
                self.log_message(f"Error loading config file: {e}. Using defaults.")
                pass
        return default_config

    def save_config(self):
        """Guardar configuración en archivo JSON"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            self.log_message(f"Error guardando configuración: {e}")

    def get_base_url(self):
        """Obtener URL base del microservicio"""
        return f"http://{self.config['ip']}:{self.config['port']}"

    def setup_gui(self):
        """Configurar la interfaz gráfica"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar expansión
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)

        # Título
        title_label = ttk.Label(main_frame, text="JWT Microservice Consumer", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Frame de configuración
        config_frame = ttk.LabelFrame(main_frame, text="Configuración del Microservicio", padding="5")
        config_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)

        ttk.Label(config_frame, text="IP:").grid(row=0, column=0, sticky=tk.W)
        self.ip_entry = ttk.Entry(config_frame)
        self.ip_entry.insert(0, self.config['ip'])
        self.ip_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))

        ttk.Label(config_frame, text="Puerto:").grid(row=1, column=0, sticky=tk.W)
        self.port_entry = ttk.Entry(config_frame)
        self.port_entry.insert(0, self.config['port'])
        self.port_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0))

        save_config_btn = ttk.Button(config_frame, text="Guardar Config", command=self.save_config_gui)
        save_config_btn.grid(row=2, column=0, columnspan=2, pady=(5, 0))

        # Semáforo de salud simplificado
        health_frame = ttk.LabelFrame(main_frame, text="Estado del Microservicio", padding="5")
        health_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        # Crear frame interno para organizar los elementos
        health_inner = ttk.Frame(health_frame)
        health_inner.pack()

        # Etiquetas de estado con colores
        self.status_label = ttk.Label(health_inner, text="Estado: Desconocido", font=("Arial", 10, "bold"))
        self.status_label.pack(pady=(0, 5))

        # Indicador visual simple con colores
        self.status_indicator = tk.Canvas(health_inner, width=30, height=30, bg='white', highlightthickness=0)
        self.status_indicator.pack()

        # Círculo de estado
        self.status_circle = self.status_indicator.create_oval(5, 5, 25, 25, fill='gray')

        # Frame de registro
        register_frame = ttk.LabelFrame(main_frame, text="Registro de Usuario", padding="5")
        register_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        register_frame.columnconfigure(1, weight=1)

        ttk.Label(register_frame, text="Usuario:").grid(row=0, column=0, sticky=tk.W)
        self.reg_username_entry = ttk.Entry(register_frame)
        self.reg_username_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))

        ttk.Label(register_frame, text="Email:").grid(row=1, column=0, sticky=tk.W)
        self.reg_email_entry = ttk.Entry(register_frame)
        self.reg_email_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0))

        ttk.Label(register_frame, text="Contraseña:").grid(row=2, column=0, sticky=tk.W)
        self.reg_password_entry = ttk.Entry(register_frame, show="*")
        self.reg_password_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 0))

        register_btn = ttk.Button(register_frame, text="Registrar Usuario", command=self.register)
        register_btn.grid(row=3, column=0, columnspan=2, pady=(5, 0))

        # Frame de login
        login_frame = ttk.LabelFrame(main_frame, text="Inicio de Sesión", padding="5")
        login_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        login_frame.columnconfigure(1, weight=1)

        ttk.Label(login_frame, text="Usuario:").grid(row=0, column=0, sticky=tk.W)
        self.username_entry = ttk.Entry(login_frame)
        self.username_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))

        ttk.Label(login_frame, text="Contraseña:").grid(row=1, column=0, sticky=tk.W)
        self.password_entry = ttk.Entry(login_frame, show="*")
        self.password_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0))

        login_btn = ttk.Button(login_frame, text="Iniciar Sesión", command=self.login)
        login_btn.grid(row=2, column=0, columnspan=2, pady=(5, 0))

        # Acciones y Gestión de Usuarios
        actions_users_frame = ttk.Frame(main_frame)
        actions_users_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        actions_users_frame.columnconfigure(0, weight=1)
        actions_users_frame.columnconfigure(1, weight=1)

        # Acciones
        actions_frame = ttk.LabelFrame(actions_users_frame, text="Acciones Autenticadas", padding="5")
        actions_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))

        protected_btn = ttk.Button(actions_frame, text="Acceder Protegido", command=self.access_protected)
        protected_btn.grid(row=0, column=0, pady=(0, 5))

        refresh_btn = ttk.Button(actions_frame, text="Refresh Token", command=self.refresh_token)
        refresh_btn.grid(row=1, column=0, pady=(0, 5))

        logout_btn = ttk.Button(actions_frame, text="Logout", command=self.logout)
        logout_btn.grid(row=2, column=0)

        # Gestión de Usuarios
        users_frame = ttk.LabelFrame(actions_users_frame, text="Gestión de Usuarios", padding="5")
        users_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        users_frame.columnconfigure(1, weight=1)

        view_users_btn = ttk.Button(users_frame, text="Ver Usuarios", command=self.get_users)
        view_users_btn.grid(row=0, column=0, pady=(0, 5))

        ttk.Label(users_frame, text="ID Usuario:").grid(row=1, column=0, sticky=tk.W)
        self.delete_user_entry = ttk.Entry(users_frame)
        self.delete_user_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0))

        delete_user_btn = ttk.Button(users_frame, text="Eliminar Usuario", command=self.delete_user)
        delete_user_btn.grid(row=2, column=0, columnspan=2, pady=(5, 0))

        # Treeview para mostrar usuarios
        self.users_tree = ttk.Treeview(users_frame, columns=("ID", "Username", "Email", "Created"), show="headings", height=6)
        self.users_tree.heading("ID", text="ID")
        self.users_tree.heading("Username", text="Usuario")
        self.users_tree.heading("Email", text="Email")
        self.users_tree.heading("Created", text="Creado")
        self.users_tree.column("ID", width=40)
        self.users_tree.column("Username", width=80)
        self.users_tree.column("Email", width=120)
        self.users_tree.column("Created", width=100)
        self.users_tree.grid(row=3, column=0, columnspan=2, pady=(10, 0), sticky=(tk.W, tk.E))

        # Log
        log_frame = ttk.LabelFrame(main_frame, text="Log de Operaciones", padding="5")
        log_frame.grid(row=3, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=15)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Información de tokens
        token_frame = ttk.LabelFrame(main_frame, text="Información de Tokens JWT", padding="5")
        token_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        token_frame.columnconfigure(1, weight=1)

        ttk.Label(token_frame, text="Access Token:").grid(row=0, column=0, sticky=tk.W)
        self.access_token_label = ttk.Label(token_frame, text=self.mask_token(self.access_token), foreground="blue", wraplength=400, justify="left")
        self.access_token_label.grid(row=0, column=1, sticky=(tk.W, tk.E))

        ttk.Label(token_frame, text="Refresh Token:").grid(row=1, column=0, sticky=tk.W)
        self.refresh_token_label = ttk.Label(token_frame, text=self.mask_token(self.refresh_token_value), foreground="green", wraplength=400, justify="left")
        self.refresh_token_label.grid(row=1, column=1, sticky=(tk.W, tk.E))

    def mask_token(self, token):
        """Mostrar token completo"""
        return token if token else ""

    def update_token_labels(self):
        """Actualizar etiquetas de tokens"""
        self.access_token_label.config(text=self.mask_token(self.access_token))
        self.refresh_token_label.config(text=self.mask_token(self.refresh_token_value))

    def log_message(self, message):
        """Agregar mensaje al log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)

    def update_semaphore(self, status):
        """Actualizar semáforo de salud simplificado"""
        self.health_status = status

        # Actualizar etiqueta de texto
        status_texts = {
            'unknown': 'Estado: Desconocido',
            'unhealthy': 'Estado: No funciona',
            'checking': 'Estado: Procesando',
            'healthy': 'Estado: Saludable'
        }

        self.status_label.config(text=status_texts.get(status, 'Estado: Desconocido'))

        # Actualizar color del círculo
        colors = {
            'unknown': 'gray',
            'unhealthy': 'red',
            'checking': 'orange',
            'healthy': 'green'
        }

        self.status_indicator.itemconfig(self.status_circle, fill=colors.get(status, 'gray'))

    def save_config_gui(self):
        """Guardar configuración desde la GUI"""
        self.config['ip'] = self.ip_entry.get()
        self.config['port'] = self.port_entry.get()
        self.save_config()
        self.log_message("Configuración guardada")

    def start_health_check(self):
        """Iniciar verificación periódica de salud cada 5 segundos"""
        def health_check_loop():
            while True:
                self.check_health()
                time.sleep(HEALTH_CHECK_INTERVAL)

        thread = threading.Thread(target=health_check_loop, daemon=True)
        thread.start()

    def check_health(self):
        """Verificar salud del microservicio"""
        try:
            self.update_semaphore('checking')
            url = f"{self.get_base_url()}{self.config['endpoints']['health']}"
            self.log_message(f"Verificando salud: GET {url}")

            response = requests.get(url, timeout=HEALTH_TIMEOUT)
            data = response.json()

            if response.status_code == 200 and data.get('status') == 'healthy':
                self.update_semaphore('healthy')
                self.log_message(f"Microservicio saludable - DB: {data.get('database')}, Redis: {data.get('redis')}")
            else:
                self.update_semaphore('unhealthy')
                self.log_message(f"Microservicio no saludable - Status: {response.status_code}")

        except requests.exceptions.RequestException as e:
            self.update_semaphore('unhealthy')
            self.log_message(f"Error conectando al microservicio: {e}")
        except Exception as e:
            self.update_semaphore('unhealthy')
            self.log_message(f"Error en verificación de salud: {e}")

    def register(self):
        """Registrar nuevo usuario"""
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        email = self.reg_email_entry.get()

        if not all([username, password, email]):
            messagebox.showerror("Error", "Todos los campos son requeridos")
            return

        try:
            url = f"{self.get_base_url()}{self.config['endpoints']['register']}"
            data = {
                "username": username,
                "email": email,
                "password": password
            }

            self.log_message(f"Registrando usuario: POST {url}")
            self.log_message(f"Datos enviados: {json.dumps(data, indent=2)}")

            response = requests.post(url, json=data, timeout=REQUEST_TIMEOUT)

            if response.status_code == 201:
                result = response.json()
                self.log_message(f"Usuario registrado exitosamente - ID: {result.get('user_id')}")
                messagebox.showinfo("Éxito", "Usuario registrado exitosamente")
            else:
                error_data = response.json()
                self.log_message(f"Error en registro: {error_data.get('message')}")
                messagebox.showerror("Error", f"Error en registro: {error_data.get('message')}")

        except requests.exceptions.RequestException as e:
            self.log_message(f"Error de conexión: {e}")
            messagebox.showerror("Error", f"Error de conexión: {e}")

    def login(self):
        """Iniciar sesión"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not all([username, password]):
            messagebox.showerror("Error", "Usuario y contraseña son requeridos")
            return

        try:
            url = f"{self.get_base_url()}{self.config['endpoints']['login']}"
            data = {
                "username": username,
                "password": password
            }

            self.log_message(f"Iniciando sesión: POST {url}")
            self.log_message(f"Datos enviados: {json.dumps(data, indent=2)}")

            response = requests.post(url, json=data, timeout=REQUEST_TIMEOUT)

            if response.status_code == 200:
                result = response.json()
                self.access_token = result.get('access_token', '')
                self.refresh_token_value = result.get('refresh_token', '')

                # Guardar tokens en config
                self.config['access_token'] = self.access_token
                self.config['refresh_token'] = self.refresh_token_value
                self.save_config()

                self.update_token_labels()
                self.log_message("Login exitoso")
                self.log_message(f"Access Token: {self.mask_token(self.access_token)}")
                self.log_message(f"Refresh Token: {self.mask_token(self.refresh_token)}")
                messagebox.showinfo("Éxito", "Login exitoso")
            else:
                error_data = response.json()
                self.log_message(f"Error en login: {error_data.get('message')}")
                messagebox.showerror("Error", f"Error en login: {error_data.get('message')}")

        except requests.exceptions.RequestException as e:
            self.log_message(f"Error de conexión: {e}")
            messagebox.showerror("Error", f"Error de conexión: {e}")

    def access_protected(self):
        """Acceder a endpoint protegido"""
        if not self.access_token:
            messagebox.showerror("Error", "No hay token de acceso disponible")
            return

        try:
            url = f"{self.get_base_url()}{self.config['endpoints']['protected']}"
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }

            self.log_message(f"Accediendo endpoint protegido: GET {url}")
            self.log_message(f"Headers: Authorization: Bearer {self.mask_token(self.access_token)}")

            response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)

            if response.status_code == 200:
                result = response.json()
                self.log_message("Acceso exitoso al endpoint protegido")
                self.log_message(f"Respuesta: {json.dumps(result, indent=2)}")
                messagebox.showinfo("Éxito", f"Acceso protegido: {result.get('message')}")
            else:
                error_data = response.json()
                self.log_message(f"Error accediendo protegido: {error_data.get('message')}")
                messagebox.showerror("Error", f"Error: {error_data.get('message')}")

        except requests.exceptions.RequestException as e:
            self.log_message(f"Error de conexión: {e}")
            messagebox.showerror("Error", f"Error de conexión: {e}")

    def refresh_token(self):
        """Refrescar token de acceso"""
        self.log_message("Botón Refresh Token presionado")

        if not self.refresh_token_value:
            self.log_message("ERROR: No hay refresh token disponible")
            messagebox.showerror("Error", "No hay refresh token disponible")
            return

        self.log_message(f"Refresh token disponible: {self.mask_token(self.refresh_token_value)[:20]}...")

        try:
            url = f"{self.get_base_url()}{self.config['endpoints']['refresh']}"

            # El cuerpo de la solicitud debe contener directamente el refresh_token
            json_payload = {
                "refresh_token": self.refresh_token_value
            }

            self.log_message(f"Enviando solicitud: POST {url}")
            self.log_message(f"Datos enviados: {json.dumps(json_payload)}")

            response = requests.post(url, json=json_payload, timeout=REQUEST_TIMEOUT)
            self.log_message(f"Respuesta recibida - Status: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                self.access_token = result.get('access_token', '')

                # Actualizar tokens en config
                self.config['access_token'] = self.access_token
                self.config['refresh_token'] = self.refresh_token_value
                self.save_config()

                self.update_token_labels()
                self.log_message("Token refrescado exitosamente")
                self.log_message(f"Nuevo Access Token: {self.mask_token(self.access_token)[:20]}...")
                messagebox.showinfo("Éxito", "Token refrescado exitosamente")
            else:
                try:
                    error_data = response.json()
                    self.log_message(f"Error del servidor: {error_data.get('message', 'Unknown error')}")
                    messagebox.showerror("Error", f"Error: {error_data.get('message', 'Unknown error')}")
                except json.JSONDecodeError:
                    self.log_message(f"Error HTTP: {response.status_code} - {response.text}")
                    messagebox.showerror("Error", f"Error HTTP: {response.status_code}. Respuesta no es JSON.")

        except requests.exceptions.Timeout:
            self.log_message("ERROR: Timeout conectando al microservicio")
            messagebox.showerror("Error", "Timeout: El microservicio no responde")
        except requests.exceptions.ConnectionError:
            self.log_message("ERROR: No se puede conectar al microservicio")
            messagebox.showerror("Error", "Error de conexión: Verifica que el microservicio esté ejecutándose")
        except Exception as e:
            self.log_message(f"ERROR inesperado: {str(e)}")
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

    def logout(self):
        """Cerrar sesión"""
        if not self.access_token:
            messagebox.showerror("Error", "No hay token de acceso disponible")
            return

        try:
            url = f"{self.get_base_url()}{self.config['endpoints']['logout']}"
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }

            self.log_message(f"Cerrando sesión: POST {url}")
            self.log_message(f"Headers: Authorization: Bearer {self.mask_token(self.access_token)}")

            response = requests.post(url, headers=headers, timeout=REQUEST_TIMEOUT)

            if response.status_code == 200:
                # Limpiar tokens
                self.access_token = ''
                self.refresh_token_value = ''
                self.config['access_token'] = ''
                self.config['refresh_token'] = ''
                self.save_config()
                self.update_token_labels()

                self.log_message("Sesión cerrada exitosamente")
                messagebox.showinfo("Éxito", "Sesión cerrada exitosamente")
            else:
                error_data = response.json()
                self.log_message(f"Error en logout: {error_data.get('message')}")
                messagebox.showerror("Error", f"Error: {error_data.get('message')}")

        except requests.exceptions.RequestException as e:
            self.log_message(f"Error de conexión: {e}")
            messagebox.showerror("Error", f"Error de conexión: {e}")

    def get_users(self):
        """Obtener lista de usuarios"""
        if not self.access_token:
            messagebox.showerror("Error", "Debes estar autenticado para ver usuarios")
            return

        try:
            url = f"{self.get_base_url()}{self.config['endpoints']['users']}"
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }

            self.log_message(f"Obteniendo lista de usuarios: GET {url}")

            response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)

            if response.status_code == 200:
                result = response.json()
                users = result.get('users', [])

                # Limpiar treeview
                for item in self.users_tree.get_children():
                    self.users_tree.delete(item)

                # Agregar usuarios al treeview
                for user in users:
                    self.users_tree.insert("", tk.END, values=(
                        user.get('id', ''),
                        user.get('username', ''),
                        user.get('email', ''),
                        user.get('created_at', '')
                    ))

                self.log_message(f"Usuarios obtenidos: {len(users)} usuarios")
                messagebox.showinfo("Éxito", f"Usuarios obtenidos: {len(users)}")
            else:
                error_data = response.json()
                self.log_message(f"Error obteniendo usuarios: {error_data.get('message')}")
                messagebox.showerror("Error", f"Error: {error_data.get('message')}")

        except requests.exceptions.RequestException as e:
            self.log_message(f"Error de conexión: {e}")
            messagebox.showerror("Error", f"Error de conexión: {e}")

    def delete_user(self):
        """Eliminar usuario"""
        if not self.access_token:
            messagebox.showerror("Error", "Debes estar autenticado para eliminar usuarios")
            return

        user_id = self.delete_user_entry.get()
        if not user_id:
            messagebox.showerror("Error", "Ingresa el ID del usuario a eliminar")
            return

        try:
            url = f"{self.get_base_url()}{self.config['endpoints']['delete_user']}{user_id}"
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }

            self.log_message(f"Eliminando usuario {user_id}: DELETE {url}")

            response = requests.delete(url, headers=headers, timeout=REQUEST_TIMEOUT)

            if response.status_code == 200:
                result = response.json()
                self.log_message(f"Usuario {user_id} eliminado exitosamente")
                messagebox.showinfo("Éxito", "Usuario eliminado exitosamente")
                # Limpiar campo
                self.delete_user_entry.delete(0, tk.END)
                # Actualizar lista de usuarios
                self.get_users()
            else:
                error_data = response.json()
                self.log_message(f"Error eliminando usuario: {error_data.get('message')}")
                messagebox.showerror("Error", f"Error: {error_data.get('message')}")

        except requests.exceptions.RequestException as e:
            self.log_message(f"Error de conexión: {e}")
            messagebox.showerror("Error", f"Error de conexión: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = JWTGUI(root)
    root.mainloop()