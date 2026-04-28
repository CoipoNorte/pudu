from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt


def create_button(text, object_name='secondaryBtn', icon_text='', parent=None):
    display = f"{icon_text}  {text}" if icon_text else text
    btn = QPushButton(display, parent)
    btn.setObjectName(object_name)
    btn.setCursor(Qt.PointingHandCursor)
    return btn


def create_separator():
    sep = QWidget()
    sep.setFixedHeight(1)
    sep.setStyleSheet("background-color: #2a3a5c;")
    return sep


def create_button_row(*buttons):
    layout = QHBoxLayout()
    layout.setSpacing(10)
    for btn in buttons:
        layout.addWidget(btn)
    return layout


def create_status_label(text='Listo'):
    label = QLabel(text)
    label.setObjectName('statusLabel')
    label.setAlignment(Qt.AlignCenter)
    return label
