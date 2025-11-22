# 📦 S3 File Manager Lab

![Flask](https://img.shields.io/badge/Flask-2.2.5-blue) ![Python](https://img.shields.io/badge/Python-3.11%2B-yellow) ![AWS%20S3](https://img.shields.io/badge/AWS%20S3-1.28.0-orange) ![JWT](https://img.shields.io/badge/JWT-Auth-green)

---

## Introducción
Este laboratorio muestra cómo crear una aplicación web sencilla con **Flask** que permite a un usuario autenticado subir y visualizar su foto de perfil usando **Amazon S3**.  Se emplea **JWT** para la autenticación y se persiste la referencia del archivo en un archivo JSON (`user_profiles.json`).  El objetivo es comprender la generación de URLs firmadas (presigned URLs), la gestión de CORS y la interacción cliente‑servidor mediante **fetch API**.

![User Profile](./fotos/User_Profile.png)

---

## Desarrollo del ejercicio
1. **Configuración del entorno**
   - `python -m venv venv && .\venv\Scripts\activate`
   - `pip install -r requirements.txt`
   - Variables de entorno en `.env` (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `BUCKET_NAME`, `SECRET_KEY`).
2. **Backend** (`app.py`)
   - Ruta `/login` genera un **JWT** y lo devuelve al cliente.
   - Ruta `/api/upload-url` crea una URL presigned **PUT** para subir la foto a `user-profile-images/<user>/<filename>`.
   - Ruta `/api/read-url` genera una URL presigned **GET** para leer la foto.
   - Ruta `/api/save-profile` guarda la clave del archivo en `user_profiles.json`.
   - Ruta `/api/me` devuelve el `fileKey` asociado al usuario.
   - Al iniciar la aplicación se aplica la política **CORS** al bucket.
3. **Frontend** (`static/script.js`)
   - Al cargar la página se verifica el token en `localStorage`.
   - Se llama a `/api/me` para obtener la `fileKey` y, si existe, se solicita la URL de lectura y se muestra la foto.
   - El proceso de subida incluye:
     1. Obtener la URL presigned.
     2. Subir el archivo a S3.
     3. Obtener la URL de lectura.
     4. Guardar la clave en el backend.
     5. Actualizar la UI.
   - El token se almacena en **LocalStorage**:

![JWT in LocalStorage](./fotos/JWT_LocalStorage.png)

4. **Persistencia**
   - `user_profiles.json` mantiene la relación `username → fileKey`.
   - Al recargar la página la foto se recupera automáticamente.

![User profile updated](./fotos/User_profile_update.png)

5. **Resultado en S3**
   - La foto se almacena en el bucket bajo la ruta `user-profile-images/...` y se puede verificar en la consola de AWS.

![S3 update](./fotos/S3_update.png)

---

## Conclusión
- **Presigned URLs** permiten que el cliente suba y descargue archivos directamente a S3 sin exponer credenciales.
- **JWT + LocalStorage** brinda una autenticación sin estado que el frontend puede reutilizar en cada petición.
- Persistir la referencia del archivo en un JSON sencillo es suficiente para un laboratorio, pero en producción se usaría una base de datos.
- Configurar **CORS** en el bucket es esencial para evitar bloqueos del navegador.
- La arquitectura separa claramente la lógica de negocio (Flask) de la UI (HTML/JS), facilitando pruebas y mantenimiento.

---

*Este proyecto es una base para ampliar funcionalidades como manejo de múltiples usuarios, versiones de imágenes o integración con bases de datos reales.*
