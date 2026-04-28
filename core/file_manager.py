import os
import sys
import subprocess
import platform
from datetime import datetime


class FileManager:
    """Gestiona guardado de lecturas, apertura de carpetas y portapapeles."""

    def __init__(self, config_manager):
        self.config = config_manager

        if getattr(sys, 'frozen', False):
            base = os.path.dirname(sys.executable)
        else:
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self.logs_dir = os.path.join(base, 'logs')
        self.last_file = None

    def ensure_logs_dir(self):
        """Crea la carpeta de logs si no existe."""
        os.makedirs(self.logs_dir, exist_ok=True)
        return self.logs_dir

    def generate_filename(self, root_dir):
        """Genera nombre de archivo basado en el formato de configuración."""
        self.ensure_logs_dir()

        log_format = self.config.log_format
        root_name = os.path.basename(os.path.normpath(root_dir))
        root_name = self._sanitize_filename(root_name)
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = log_format.format(date=date_str, root=root_name)
        return os.path.join(self.logs_dir, filename)

    def save_reading(self, tree_text, root_dir):
        """
        Guarda la lectura del árbol en un archivo .txt.

        Args:
            tree_text: Texto del árbol ASCII.
            root_dir: Ruta del directorio escaneado.

        Returns:
            Ruta completa del archivo guardado.
        """
        filepath = self.generate_filename(root_dir)
        project_name = os.path.basename(os.path.normpath(root_dir))
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        separator = '═' * 50

        content = (
            f"{separator}\n"
            f"  Proyecto : {project_name}\n"
            f"  Ruta     : {root_dir}\n"
            f"  Fecha    : {timestamp}\n"
            f"{separator}\n\n"
            f"{tree_text}\n"
            f"{separator}\n"
            f"  Generado por File Structure Reader\n"
            f"{separator}\n"
        )

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        self.last_file = filepath
        return filepath

    def get_last_content(self):
        """Lee y retorna el contenido del último archivo generado."""
        if not self.last_file or not os.path.exists(self.last_file):
            return None

        with open(self.last_file, 'r', encoding='utf-8') as f:
            return f.read()

    def open_logs_folder(self):
        """Abre la carpeta de logs en el explorador del sistema."""
        logs_dir = self.ensure_logs_dir()
        system = platform.system()

        try:
            if system == 'Windows':
                os.startfile(logs_dir)
            elif system == 'Darwin':
                subprocess.run(['open', logs_dir])
            elif system == 'Linux':
                subprocess.run(['xdg-open', logs_dir])
            else:
                raise OSError(f"Sistema no soportado: {system}")
        except Exception as e:
            raise RuntimeError(f"No se pudo abrir la carpeta: {e}")

    def get_logs_list(self):
        """Retorna lista de archivos de log existentes."""
        self.ensure_logs_dir()
        files = sorted(os.listdir(self.logs_dir), reverse=True)
        return [f for f in files if f.endswith('.txt')]

    def delete_log(self, filename):
        """Elimina un archivo de log específico."""
        filepath = os.path.join(self.logs_dir, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False

    def clear_all_logs(self):
        """Elimina todos los archivos de log."""
        count = 0
        for filename in self.get_logs_list():
            filepath = os.path.join(self.logs_dir, filename)
            os.remove(filepath)
            count += 1
        return count

    @staticmethod
    def _sanitize_filename(name):
        """Elimina caracteres no válidos para nombres de archivo."""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '_')
        return name
