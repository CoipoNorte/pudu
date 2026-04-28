import json
import os
import sys


def _get_base_dir():
    """Retorna la ruta base, compatible con PyInstaller."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _get_resource_dir():
    """Retorna la ruta de recursos empaquetados."""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DEFAULT_CONFIG_PATH = os.path.join(_get_base_dir(), 'config', 'settings.json')
BUNDLED_CONFIG_PATH = os.path.join(_get_resource_dir(), 'config', 'settings.json')


class ConfigManager:
    """Gestiona la carga, guardado y acceso a la configuración JSON."""

    def __init__(self, config_path=None):
        self.config_path = config_path or DEFAULT_CONFIG_PATH
        self.config = {}
        self.load()

    def load(self):
        """Carga la configuración desde el archivo JSON."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            # Intentar desde recursos empaquetados
            try:
                with open(BUNDLED_CONFIG_PATH, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                # Copiar al destino editable
                self.save()
            except FileNotFoundError:
                print(f"[ConfigManager] Archivo no encontrado, usando defaults")
                self.config = self._default_config()
                self.save()
        except json.JSONDecodeError as e:
            print(f"[ConfigManager] Error al parsear JSON: {e}")
            self.config = self._default_config()

    def save(self):
        """Guarda la configuración actual en el archivo JSON."""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save()

    @property
    def ignored_folders(self):
        base = set(self.config.get('ignored_folders', []))
        exceptions = set(self.config.get('exceptions', {}).get('folders', []))
        return base - exceptions

    @property
    def ignored_files(self):
        base = set(self.config.get('ignored_files', []))
        exceptions = set(self.config.get('exceptions', {}).get('files', []))
        return base - exceptions

    @property
    def ignored_extensions(self):
        base = set(self.config.get('ignored_extensions', []))
        exceptions = set(self.config.get('exceptions', {}).get('extensions', []))
        return base - exceptions

    @property
    def image_extensions(self):
        return set(self.config.get('image_extensions', []))

    @property
    def max_depth(self):
        return self.config.get('max_depth', -1)

    @property
    def show_hidden(self):
        return self.config.get('show_hidden_files', False)

    @property
    def log_format(self):
        return self.config.get('log_format', 'log_{date}_{root}.txt')

    def _default_config(self):
        return {
            "ignored_folders": ["node_modules", "__pycache__", ".git"],
            "ignored_files": [".DS_Store"],
            "ignored_extensions": [".pyc"],
            "image_extensions": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"],
            "exceptions": {"folders": [], "files": [], "extensions": []},
            "max_depth": -1,
            "show_hidden_files": False,
            "log_format": "log_{date}_{root}.txt"
        }
