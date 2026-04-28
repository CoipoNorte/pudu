import os
import sys
import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QListWidget, QLineEdit, QPushButton, QGroupBox,
    QTabWidget, QWidget, QApplication, QAbstractItemView
)
from PyQt5.QtCore import Qt


class ConfigWindow(QDialog):
    """Ventana de configuración visual para settings.json."""

    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self._setup_window()
        self._setup_ui()
        self._load_data()

    def _setup_window(self):
        self.setWindowTitle("⚙️ Configuración")
        self.setMinimumSize(550, 500)
        self.resize(600, 550)
        self.setStyleSheet("""
            QDialog {
                background-color: #16213e;
            }
            QLabel {
                color: #e0e0e0;
                font-size: 12px;
                background: transparent;
            }
            QTabWidget::pane {
                border: 1px solid #2a3a5c;
                border-radius: 6px;
                background-color: #0f1a30;
            }
            QTabBar::tab {
                background-color: #2a3a5c;
                color: #b0b0c0;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            QTabBar::tab:selected {
                background-color: #00d4ff;
                color: #0a0a1a;
                font-weight: bold;
            }
            QListWidget {
                background-color: #0a0f1e;
                color: #c8d6e5;
                border: 1px solid #2a3a5c;
                border-radius: 6px;
                padding: 4px;
                font-family: 'Consolas', monospace;
                font-size: 12px;
            }
            QListWidget::item {
                padding: 4px 8px;
                border-radius: 3px;
            }
            QListWidget::item:selected {
                background-color: #00d4ff;
                color: #0a0a1a;
            }
            QLineEdit {
                background-color: #0a0f1e;
                color: #e0e0e0;
                border: 1px solid #2a3a5c;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #00d4ff;
            }
            QPushButton {
                border: none;
                border-radius: 6px;
                padding: 7px 14px;
                font-size: 12px;
                font-weight: 600;
                min-width: 70px;
            }
            QPushButton#addBtn {
                background-color: #00e676;
                color: #0a0a1a;
            }
            QPushButton#addBtn:hover {
                background-color: #00c864;
            }
            QPushButton#removeBtn {
                background-color: #ff1744;
                color: #ffffff;
            }
            QPushButton#removeBtn:hover {
                background-color: #e01540;
            }
            QPushButton#saveBtn {
                background-color: #00d4ff;
                color: #0a0a1a;
                padding: 10px 30px;
                font-size: 13px;
            }
            QPushButton#saveBtn:hover {
                background-color: #00b8e6;
            }
            QPushButton#openBtn {
                background-color: #2a3a5c;
                color: #e0e0e0;
                padding: 10px 20px;
                font-size: 13px;
            }
            QPushButton#openBtn:hover {
                background-color: #354d73;
            }
            QGroupBox {
                border: 1px solid #2a3a5c;
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 16px;
                font-size: 12px;
                font-weight: 600;
                color: #00d4ff;
                background-color: #0f1a30;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 6px;
            }
        """)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(12)

        # Tabs
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs, 1)

        # Tab 1: Carpetas ignoradas
        self.tab_folders = self._create_list_tab(
            "Carpetas que se ignoran al escanear",
            "Nombre de carpeta..."
        )
        self.tabs.addTab(self.tab_folders['widget'], "📁 Carpetas")

        # Tab 2: Archivos ignorados
        self.tab_files = self._create_list_tab(
            "Archivos específicos que se ignoran",
            "Nombre de archivo..."
        )
        self.tabs.addTab(self.tab_files['widget'], "📄 Archivos")

        # Tab 3: Extensiones ignoradas
        self.tab_extensions = self._create_list_tab(
            "Extensiones que se ignoran (incluir el punto)",
            ".ext"
        )
        self.tabs.addTab(self.tab_extensions['widget'], "🔧 Extensiones")

        # Tab 4: Imágenes
        self.tab_images = self._create_list_tab(
            "Extensiones consideradas imagen",
            ".ext"
        )
        self.tabs.addTab(self.tab_images['widget'], "🖼️ Imágenes")

        # Tab 5: Excepciones
        self.tab_exc_folders = self._create_list_tab(
            "Carpetas que NO se ignoran (anulan ignorados)",
            "Nombre de carpeta..."
        )
        self.tab_exc_files = self._create_list_tab(
            "Archivos que NO se ignoran",
            "Nombre de archivo..."
        )
        self.tab_exc_extensions = self._create_list_tab(
            "Extensiones que NO se ignoran",
            ".ext"
        )

        exc_widget = QWidget()
        exc_layout = QVBoxLayout(exc_widget)
        exc_layout.setContentsMargins(5, 5, 5, 5)
        exc_layout.setSpacing(8)

        exc_folders_group = QGroupBox("Carpetas")
        exc_folders_layout = QVBoxLayout(exc_folders_group)
        exc_folders_layout.addWidget(self.tab_exc_folders['inner'])
        exc_layout.addWidget(exc_folders_group)

        exc_files_group = QGroupBox("Archivos")
        exc_files_layout = QVBoxLayout(exc_files_group)
        exc_files_layout.addWidget(self.tab_exc_files['inner'])
        exc_layout.addWidget(exc_files_group)

        exc_ext_group = QGroupBox("Extensiones")
        exc_ext_layout = QVBoxLayout(exc_ext_group)
        exc_ext_layout.addWidget(self.tab_exc_extensions['inner'])
        exc_layout.addWidget(exc_ext_group)

        self.tabs.addTab(exc_widget, "✅ Excepciones")

        # Botones inferiores
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(10)

        self.btn_open_json = QPushButton("📂  Abrir JSON")
        self.btn_open_json.setObjectName('openBtn')
        self.btn_open_json.setCursor(Qt.PointingHandCursor)
        self.btn_open_json.clicked.connect(self._open_json_file)
        bottom_row.addWidget(self.btn_open_json)

        bottom_row.addStretch()

        self.btn_save = QPushButton("💾  Guardar")
        self.btn_save.setObjectName('saveBtn')
        self.btn_save.setCursor(Qt.PointingHandCursor)
        self.btn_save.clicked.connect(self._save_config)
        bottom_row.addWidget(self.btn_save)

        layout.addLayout(bottom_row)

        # Status
        self.status = QLabel("")
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setStyleSheet("color: #8892b0; font-style: italic;")
        layout.addWidget(self.status)

    def _create_list_tab(self, description, placeholder):
        """Crea un tab con lista editable (agregar/quitar items)."""
        widget = QWidget()
        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        desc = QLabel(description)
        layout.addWidget(desc)

        list_widget = QListWidget()
        list_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        layout.addWidget(list_widget, 1)

        input_row = QHBoxLayout()
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_row.addWidget(input_field)

        btn_add = QPushButton("+ Agregar")
        btn_add.setObjectName('addBtn')
        btn_add.setCursor(Qt.PointingHandCursor)
        input_row.addWidget(btn_add)

        btn_remove = QPushButton("− Quitar")
        btn_remove.setObjectName('removeBtn')
        btn_remove.setCursor(Qt.PointingHandCursor)
        input_row.addWidget(btn_remove)

        layout.addLayout(input_row)

        # Conectar
        def add_item():
            text = input_field.text().strip()
            if text and not self._list_contains(list_widget, text):
                list_widget.addItem(text)
                input_field.clear()

        def remove_items():
            for item in list_widget.selectedItems():
                list_widget.takeItem(list_widget.row(item))

        btn_add.clicked.connect(add_item)
        input_field.returnPressed.connect(add_item)
        btn_remove.clicked.connect(remove_items)

        # Widget completo para tab
        tab_layout = QVBoxLayout(widget)
        tab_layout.setContentsMargins(5, 5, 5, 5)
        tab_layout.addWidget(inner)

        return {
            'widget': widget,
            'inner': inner,
            'list': list_widget,
            'input': input_field,
        }

    def _load_data(self):
        """Carga datos del config_manager a las listas."""
        config = self.config_manager.config

        self._fill_list(self.tab_folders['list'], config.get('ignored_folders', []))
        self._fill_list(self.tab_files['list'], config.get('ignored_files', []))
        self._fill_list(self.tab_extensions['list'], config.get('ignored_extensions', []))
        self._fill_list(self.tab_images['list'], config.get('image_extensions', []))

        exceptions = config.get('exceptions', {})
        self._fill_list(self.tab_exc_folders['list'], exceptions.get('folders', []))
        self._fill_list(self.tab_exc_files['list'], exceptions.get('files', []))
        self._fill_list(self.tab_exc_extensions['list'], exceptions.get('extensions', []))

    def _save_config(self):
        """Guarda las listas de vuelta al JSON."""
        config = self.config_manager.config

        config['ignored_folders'] = self._get_list_items(self.tab_folders['list'])
        config['ignored_files'] = self._get_list_items(self.tab_files['list'])
        config['ignored_extensions'] = self._get_list_items(self.tab_extensions['list'])
        config['image_extensions'] = self._get_list_items(self.tab_images['list'])

        config['exceptions'] = {
            'folders': self._get_list_items(self.tab_exc_folders['list']),
            'files': self._get_list_items(self.tab_exc_files['list']),
            'extensions': self._get_list_items(self.tab_exc_extensions['list']),
        }

        self.config_manager.config = config
        self.config_manager.save()
        self.status.setText("✅ Configuración guardada")
        QApplication.beep()

    def _open_json_file(self):
        """Abre el archivo JSON en el editor por defecto del sistema."""
        path = self.config_manager.config_path
        if os.path.exists(path):
            if sys.platform == 'win32':
                os.startfile(path)
            elif sys.platform == 'darwin':
                import subprocess
                subprocess.run(['open', path])
            else:
                import subprocess
                subprocess.run(['xdg-open', path])
            self.status.setText(f"📂 Abierto: {os.path.basename(path)}")
        else:
            self.status.setText("❌ Archivo JSON no encontrado")
            QApplication.beep()

    @staticmethod
    def _fill_list(list_widget, items):
        list_widget.clear()
        for item in sorted(items):
            list_widget.addItem(item)

    @staticmethod
    def _get_list_items(list_widget):
        items = []
        for i in range(list_widget.count()):
            items.append(list_widget.item(i).text())
        return sorted(items)

    @staticmethod
    def _list_contains(list_widget, text):
        for i in range(list_widget.count()):
            if list_widget.item(i).text() == text:
                return True
        return False
