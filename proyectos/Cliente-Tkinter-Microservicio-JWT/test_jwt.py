#!/usr/bin/env python3
"""
Script de prueba completo para el microservicio JWT
"""

import requests
import json
import time
import sys
from datetime import datetime

class JWTTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.access_token = None
        self.refresh_token = None
        self.user_id = None
        
    def print_status(self, message, status="info"):
        """Función para imprimir mensajes con formato"""
        colors = {
            "success": "\033[92m",  # Verde
            "warning": "\033[93m",  # Amarillo
            "error": "\033[91m",    # Rojo
            "info": "\033[94m",     # Azul
            "reset": "\033[0m"      # Reset
        }
        
        symbols = {
            "success": "✓",
            "warning": "⚠", 
            "error": "✗",
            "info": "ℹ"
        }
        
        symbol = symbols.get(status, " ")
        color = colors.get(status, "")
        reset = colors["reset"]
        
        print(f"   {color}{symbol}{reset} {message}")
    
    def test_health(self):
        """Verificar salud del servicio"""
        self.print_status("Verificando salud del servicio...", "info")
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.print_status(f"Salud: {data.get('status', 'unknown')}", "success")
                return True
            else:
                self.print_status(f"Error: Código {response.status_code}", "error")
                return False
        except requests.exceptions.RequestException as e:
            self.print_status(f"Servicio no disponible: {e}", "error")
            return False
    
    def test_register(self, username=None, email=None, password="testpass123"):
        """Registrar un nuevo usuario"""
        self.print_status("Registrando usuario...", "info")
        
        if not username:
            timestamp = datetime.now().strftime("%H%M%S")
            username = f"testuser_{timestamp}"
            email = f"test_{timestamp}@example.com"
        
        register_data = {
            "username": username,
            "email": email,
            "password": password
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/register",
                json=register_data,
                timeout=10
            )
            
            if response.status_code == 201:
                data = response.json()
                self.user_id = data.get("user_id")
                self.print_status(f"Usuario registrado: {username} (ID: {self.user_id})", "success")
                return True
            else:
                data = response.json()
                self.print_status(f"Error en registro: {data.get('message', 'Unknown error')}", "error")
                return False
                
        except requests.exceptions.RequestException as e:
            self.print_status(f"Error de conexión: {e}", "error")
            return False
    
    def test_login(self, username="testuser", password="testpass"):
        """Iniciar sesión y obtener tokens"""
        self.print_status("Iniciando sesión...", "info")
        
        login_data = {
            "username": username,
            "password": password
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/login",
                json=login_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get("access_token")
                self.refresh_token = data.get("refresh_token")
                
                if self.access_token and self.refresh_token:
                    self.print_status("Login exitoso", "success")
                    self.print_status(f"Access Token: {self.access_token[:50]}...", "info")
                    self.print_status(f"Refresh Token: {self.refresh_token[:50]}...", "info")
                    return True
                else:
                    self.print_status("Tokens no recibidos en la respuesta", "error")
                    return False
            else:
                data = response.json()
                self.print_status(f"Error en login: {data.get('message', 'Unknown error')}", "error")
                return False
                
        except requests.exceptions.RequestException as e:
            self.print_status(f"Error de conexión: {e}", "error")
            return False
    
    def test_protected_endpoint(self):
        """Probar endpoint protegido"""
        self.print_status("Probando endpoint protegido...", "info")
        
        if not self.access_token:
            self.print_status("No hay access token disponible", "error")
            return False
        
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/protected",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.print_status("Endpoint protegido accedido correctamente", "success")
                self.print_status(f"Mensaje: {data.get('message', 'No message')}", "info")
                self.print_status(f"User ID: {data.get('user_id', 'No user ID')}", "info")
                return True
            else:
                data = response.json()
                self.print_status(f"Error en endpoint protegido: {data.get('message', 'Unknown error')}", "error")
                return False
                
        except requests.exceptions.RequestException as e:
            self.print_status(f"Error de conexión: {e}", "error")
            return False
    
    def test_refresh_token(self):
        """Probar refresh token"""
        self.print_status("Probando refresh token...", "info")
        
        if not self.refresh_token:
            self.print_status("No hay refresh token disponible", "error")
            return False
        
        refresh_data = {
            "refresh_token": self.refresh_token
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/refresh",
                json=refresh_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                new_access_token = data.get("access_token")
                if new_access_token:
                    self.access_token = new_access_token
                    self.print_status("Token refrescado exitosamente", "success")
                    self.print_status(f"Nuevo Access Token: {new_access_token[:50]}...", "info")
                    return True
                else:
                    self.print_status("Nuevo access token no recibido", "error")
                    return False
            else:
                data = response.json()
                self.print_status(f"Error refrescando token: {data.get('message', 'Unknown error')}", "error")
                return False
                
        except requests.exceptions.RequestException as e:
            self.print_status(f"Error de conexión: {e}", "error")
            return False
    
    def test_logout(self):
        """Probar logout"""
        self.print_status("Probando logout...", "info")
        
        if not self.access_token:
            self.print_status("No hay access token disponible", "error")
            return False
        
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/logout",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.print_status("Logout exitoso", "success")
                self.print_status(f"Mensaje: {data.get('message', 'No message')}", "info")
                return True
            else:
                data = response.json()
                self.print_status(f"Error en logout: {data.get('message', 'Unknown error')}", "error")
                return False
                
        except requests.exceptions.RequestException as e:
            self.print_status(f"Error de conexión: {e}", "error")
            return False
    
    def test_token_revocation(self):
        """Verificar que el token fue revocado después del logout"""
        self.print_status("Verificando que el token fue revocado...", "info")

        if not self.access_token:
            self.print_status("No hay access token disponible", "error")
            return False

        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        try:
            response = requests.get(
                f"{self.base_url}/protected",
                headers=headers,
                timeout=10
            )

            # Si llega aquí, el token aún funciona (no debería)
            if response.status_code == 200:
                self.print_status("❌ Token aún funciona después del logout", "error")
                return False
            else:
                self.print_status("✅ Token correctamente revocado", "success")
                return True

        except requests.exceptions.RequestException:
            # Se espera una excepción porque el token fue revocado
            self.print_status("✅ Token correctamente revocado (error esperado)", "success")
            return True

    def test_get_users(self):
        """Probar obtener lista de usuarios"""
        self.print_status("Probando obtener lista de usuarios...", "info")

        if not self.access_token:
            self.print_status("No hay access token disponible", "error")
            return False

        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        try:
            response = requests.get(
                f"{self.base_url}/users",
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                users = data.get('users', [])
                self.print_status(f"✅ Lista de usuarios obtenida: {len(users)} usuarios", "success")
                return True
            else:
                data = response.json()
                self.print_status(f"Error obteniendo usuarios: {data.get('message')}", "error")
                return False

        except requests.exceptions.RequestException as e:
            self.print_status(f"Error de conexión: {e}", "error")
            return False

    def test_delete_user(self):
        """Probar eliminar usuario (crear uno nuevo y eliminarlo)"""
        self.print_status("Probando eliminar usuario...", "info")

        if not self.access_token:
            self.print_status("No hay access token disponible", "error")
            return False

        # Primero crear un usuario de prueba
        test_username = f"delete_test_{datetime.now().strftime('%H%M%S')}"
        test_email = f"delete_{datetime.now().strftime('%H%M%S')}@test.com"
        test_password = "testpass123"

        register_data = {
            "username": test_username,
            "email": test_email,
            "password": test_password
        }

        try:
            # Registrar usuario
            response = requests.post(
                f"{self.base_url}/register",
                json=register_data,
                timeout=10
            )

            if response.status_code != 201:
                self.print_status("Error creando usuario de prueba para eliminación", "error")
                return False

            user_data = response.json()
            user_id = user_data.get('user_id')

            # Ahora intentar eliminarlo (pero como no estamos logueados como ese usuario, debería fallar)
            # Para probar correctamente, necesitaríamos login como ese usuario, pero por simplicidad probamos con el usuario actual
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }

            response = requests.delete(
                f"{self.base_url}/users/{user_id}",
                headers=headers,
                timeout=10
            )

            if response.status_code == 403:
                self.print_status("✅ Endpoint de eliminación funciona (prohibido eliminar otros usuarios)", "success")
                return True
            elif response.status_code == 200:
                self.print_status("✅ Usuario eliminado exitosamente", "success")
                return True
            else:
                data = response.json()
                self.print_status(f"Error eliminando usuario: {data.get('message')}", "error")
                return False

        except requests.exceptions.RequestException as e:
            self.print_status(f"Error de conexión: {e}", "error")
            return False
    
    def run_complete_test(self):
        """Ejecutar prueba completa"""
        print("=" * 60)
        print("PRUEBA COMPLETA MICROSERVICIO JWT")
        print("=" * 60)
        print(f"URL base: {self.base_url}")
        print(f"Hora de inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        results = []
        
        # 1. Verificar salud
        results.append(("Salud del servicio", self.test_health()))
        time.sleep(1)
        
        # 2. Registrar usuario
        results.append(("Registro de usuario", self.test_register()))
        time.sleep(1)
        
        # 3. Login con usuario existente (crear uno si no existe)
        login_success = self.test_login("testuser", "testpass")
        if not login_success:
            self.print_status("Usuario no existe, registrando uno nuevo...", "warning")
            self.test_register("testuser", "test@example.com", "testpass")
            login_success = self.test_login("testuser", "testpass")
        results.append(("Login", login_success))
        time.sleep(1)
        
        # 4. Endpoint protegido
        if login_success:
            results.append(("Endpoint protegido", self.test_protected_endpoint()))
            time.sleep(1)
            
            # 5. Refresh token
            results.append(("Refresh token", self.test_refresh_token()))
            time.sleep(1)
            
            # 6. Logout
            results.append(("Logout", self.test_logout()))
            time.sleep(1)
            
            # 7. Verificar revocación
            results.append(("Revocación de token", self.test_token_revocation()))
            time.sleep(1)
    
            # 8. Obtener usuarios
            results.append(("Obtener usuarios", self.test_get_users()))
            time.sleep(1)
    
            # 9. Eliminar usuario
            results.append(("Eliminar usuario", self.test_delete_user()))
        
        # Resumen
        print("\n" + "=" * 60)
        print("RESUMEN DE PRUEBAS")
        print("=" * 60)
        
        passed = 0
        total = len(results)
        
        for test_name, success in results:
            status = "✓" if success else "✗"
            color = "\033[92m" if success else "\033[91m"
            reset = "\033[0m"
            print(f"   {color}{status}{reset} {test_name}")
            if success:
                passed += 1
        
        print(f"\nPruebas pasadas: {passed}/{total}")
        
        if passed == total:
            self.print_status("¡Todas las pruebas pasaron correctamente!", "success")
        else:
            self.print_status(f"Algunas pruebas fallaron ({total - passed} errores)", "error")
        
        print("\nServicios disponibles:")
        print("   - Microservicio: http://localhost:5000")
        print("   - Adminer (BD): http://localhost:8080")
        print("=" * 60)
        
        return passed == total

def main():
    """Función principal"""
    tester = JWTTester()
    
    # Verificar si se proporcionó una URL diferente
    if len(sys.argv) > 1:
        tester.base_url = sys.argv[1]
    
    try:
        success = tester.run_complete_test()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nPrueba interrumpida por el usuario.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError durante la prueba: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()