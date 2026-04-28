import os
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QLineEdit, QCheckBox, QLabel,
    QFileDialog, QTextEdit, QGroupBox, QApplication
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon

from ui.styles import MAIN_STYLE
from ui.widgets import create_button, create_separator, create_button_row, create_status_label
from ui.config_window import ConfigWindow
from core.scanner import DirectoryScanner
from core.file_manager import FileManager
from core.config_manager import ConfigManager


def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DropZone(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self._main_window = None

    def set_main_window(self, window):
        self._main_window = window

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and os.path.isdir(urls[0].toLocalFile()):
                event.acceptProposedAction()
                return
        event.ignore()

    def dragLeaveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            if os.path.isdir(path):
                self.setText(path)
                event.acceptProposedAction()
                if self._main_window:
                    self._main_window._on_path_dropped(path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.scanner = DirectoryScanner(self.config_manager)
        self.file_manager = FileManager(self.config_manager)
        self._clear_confirm = False
        self._setup_window()
        self._setup_ui()
        self._connect_signals()

    def _setup_window(self):
        self.setWindowTitle("File Structure Reader")
        self.setMinimumSize(600, 700)
        self.resize(650, 750)
        self.setStyleSheet(MAIN_STYLE)
        self.setAcceptDrops(True)
        icon_path = os.path.join(get_base_dir(), 'assets', 'icon.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

    def _setup_ui(self):
        central = QWidget()
        central.setObjectName('centralWidget')
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(25, 20, 25, 20)
        main_layout.setSpacing(15)

        # ═══ Directorio ═══
        dir_group = QGroupBox("Directorio  —  arrastra una carpeta aquí")
        dir_layout = QVBoxLayout(dir_group)
        path_row = QHBoxLayout()
        self.path_input = DropZone()
        self.path_input.set_main_window(self)
        self.path_input.setPlaceholderText("Arrastra una carpeta o haz clic en Buscar...")
        path_row.addWidget(self.path_input)
        self.btn_select = create_button("Buscar", 'secondaryBtn', '📂')
        path_row.addWidget(self.btn_select)
        dir_layout.addLayout(path_row)
        main_layout.addWidget(dir_group)

        # ═══ Opciones ═══
        options_group = QGroupBox("Opciones")
        options_layout = QVBoxLayout(options_group)

        options_top_row = QHBoxLayout()

        checkboxes_layout = QVBoxLayout()
        self.chk_omit_images = QCheckBox("Omitir archivos de imagen")
        checkboxes_layout.addWidget(self.chk_omit_images)
        self.chk_show_hidden = QCheckBox("Mostrar archivos ocultos")
        checkboxes_layout.addWidget(self.chk_show_hidden)
        options_top_row.addLayout(checkboxes_layout)

        options_top_row.addStretch()

        self.btn_config = create_button("Configuración", 'secondaryBtn', '⚙️')
        options_top_row.addWidget(self.btn_config)

        options_layout.addLayout(options_top_row)
        main_layout.addWidget(options_group)

        # ═══ Acciones ═══
        actions_group = QGroupBox("Acciones")
        actions_layout = QVBoxLayout(actions_group)
        self.btn_generate = create_button("Generar", 'primaryBtn', '⚡')
        self.btn_copy = create_button("Copiar", 'successBtn', '📋')
        self.btn_open_logs = create_button("Abrir Logs", 'secondaryBtn', '📁')
        self.btn_clear_logs = create_button("Limpiar Logs", 'warningBtn', '🗑️')
        actions_layout.addLayout(create_button_row(self.btn_generate, self.btn_copy))
        actions_layout.addLayout(create_button_row(self.btn_open_logs, self.btn_clear_logs))
        main_layout.addWidget(actions_group)

        # ═══ Vista Previa ═══
        preview_group = QGroupBox("Vista Previa")
        preview_layout = QVBoxLayout(preview_group)
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setPlaceholderText(
            "Aquí aparecerá el árbol de estructura...\n\n"
            "1. Arrastra una carpeta o selecciona con Buscar\n"
            "2. Configura las opciones\n"
            "3. Haz clic en Generar"
        )
        preview_layout.addWidget(self.preview_text)
        main_layout.addWidget(preview_group, 1)

        # ═══ Status ═══
        main_layout.addWidget(create_separator())
        self.status_label = create_status_label("Listo — Arrastra una carpeta para comenzar")
        main_layout.addWidget(self.status_label)

    def _connect_signals(self):
        self.btn_select.clicked.connect(self._on_select_directory)
        self.btn_generate.clicked.connect(self._on_generate)
        self.btn_copy.clicked.connect(self._on_copy)
        self.btn_open_logs.clicked.connect(self._on_open_logs)
        self.btn_clear_logs.clicked.connect(self._on_clear_logs)
        self.btn_config.clicked.connect(self._on_open_config)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and os.path.isdir(urls[0].toLocalFile()):
                event.acceptProposedAction()
                return
        event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            if os.path.isdir(path):
                self.path_input.setText(path)
                self._on_path_dropped(path)
                event.acceptProposedAction()

    def _on_path_dropped(self, path):
        folder_name = os.path.basename(os.path.normpath(path))
        self._update_status(f"📂 Carpeta cargada: {folder_name}")
        self._beep()

    def _on_select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Seleccionar Directorio")
        if directory:
            self.path_input.setText(directory)
            self._update_status(f"📂 {os.path.basename(os.path.normpath(directory))}")

    def _on_generate(self):
        path = self.path_input.text().strip()
        if not path:
            self._update_status("⚠️ Selecciona un directorio primero")
            self._beep()
            return
        if not os.path.isdir(path):
            self._update_status("❌ Ruta no válida")
            self._beep()
            return

        self.config_manager.set('show_hidden_files', self.chk_show_hidden.isChecked())

        try:
            self._update_status("⏳ Escaneando...")
            QApplication.processEvents()
            tree = self.scanner.scan(path, self.chk_omit_images.isChecked())
            self.preview_text.setPlainText(tree)
            saved_path = self.file_manager.save_reading(tree, path)
            self._update_status(f"✅ Guardado: {os.path.basename(saved_path)}")
            self._beep()
        except Exception as e:
            self._update_status(f"❌ Error: {str(e)}")
            self._beep()

    def _on_copy(self):
        content = self.preview_text.toPlainText() or self.file_manager.get_last_content()
        if not content:
            self._update_status("⚠️ Genera una lectura primero")
            self._beep()
            return
        QApplication.clipboard().setText(content)
        self._update_status("📋 Copiado al portapapeles")
        self._beep()

    def _on_open_logs(self):
        try:
            self.file_manager.open_logs_folder()
            self._update_status("📁 Carpeta de logs abierta")
        except RuntimeError as e:
            self._update_status(f"❌ {str(e)}")
            self._beep()

    def _on_clear_logs(self):
        logs = self.file_manager.get_logs_list()
        if not logs:
            self._update_status("ℹ️ No hay logs para eliminar")
            return
        if not self._clear_confirm:
            self._clear_confirm = True
            self._update_status(f"⚠️ ¿Eliminar {len(logs)} log(s)? Clic de nuevo para confirmar")
            self._beep()
            QTimer.singleShot(3000, self._reset_clear_confirm)
            return
        count = self.file_manager.clear_all_logs()
        self._update_status(f"🗑️ {count} log(s) eliminados")
        self._beep()
        self._clear_confirm = False

    def _reset_clear_confirm(self):
        if self._clear_confirm:
            self._clear_confirm = False
            self._update_status("Eliminación cancelada")

    def _on_open_config(self):
        """Abre la ventana de configuración."""
        dialog = ConfigWindow(self.config_manager, self)
        dialog.exec_()
        # Recargar config después de cerrar
        self.config_manager.load()
        self._update_status("⚙️ Configuración actualizada")

    def _update_status(self, text):
        self.status_label.setText(text)

    @staticmethod
    def _beep():
        QApplication.beep()
