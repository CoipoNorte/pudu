# 🗂️ File Structure Reader v2.0

Genera árboles ASCII de la estructura de archivos de cualquier proyecto.

## ✨ Características

- 📂 Escaneo recursivo de directorios
- 🎨 Iconos emoji por tipo de archivo
- ⚙️ Configuración JSON flexible
- 🚫 Ignorar carpetas, archivos y extensiones
- ✅ Excepciones para anular ignorados
- 🖼️ Opción para omitir imágenes
- 👁️ Mostrar/ocultar archivos ocultos
- 📋 Copiar al portapapeles
- 📁 Historial de lecturas en /logs
- 🗑️ Limpiar logs desde la app
- 📏 Profundidad máxima configurable
- 🎯 Interfaz moderna con tema oscuro

## 📁 Estructura del proyecto

File-Structure-Reader/
├── 📁 assets/
│   ├── icon.ico
│   ├── icon.png
│   └── favicon.ico
├── 📁 config/
│   └── settings.json
├── 📁 core/
│   ├── __init__.py
│   ├── scanner.py
│   ├── config_manager.py
│   └── file_manager.py
├── 📁 ui/
│   ├── __init__.py
│   ├── main_window.py
│   ├── styles.py
│   └── widgets.py
├── 📁 logs/
├── main.py
├── requirements.txt
└── README.md

## 🚀 Instalación

pip install -r requirements.txt

## ▶️ Ejecutar

python main.py

## ⚙️ Configuración

Edita `config/settings.json` para personalizar:

- `ignored_folders` — Carpetas a ignorar
- `ignored_files` — Archivos específicos a ignorar
- `ignored_extensions` — Extensiones a ignorar
- `image_extensions` — Extensiones consideradas imagen
- `exceptions` — Anular cualquier ignorado
- `max_depth` — Profundidad máxima (-1 = sin límite)
- `show_hidden_files` — Mostrar archivos ocultos
- `log_format` — Formato del nombre de los logs

## 📜 Licencia

MIT
