MAIN_STYLE = """
QMainWindow {
    background-color: #1a1a2e;
}
QWidget#centralWidget {
    background-color: #16213e;
}
QLabel {
    font-size: 13px;
    color: #e0e0e0;
    font-weight: 500;
    background: transparent;
}
QLabel#titleLabel {
    font-size: 20px;
    font-weight: 700;
    color: #00d4ff;
    padding: 5px 0;
}
QLabel#statusLabel {
    font-size: 11px;
    color: #8892b0;
    font-style: italic;
}
QLineEdit {
    border: 2px solid #2a3a5c;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 13px;
    background-color: #0f1a30;
    color: #e0e0e0;
}
QLineEdit:focus {
    border-color: #00d4ff;
}
QCheckBox {
    font-size: 13px;
    color: #b0b0c0;
    spacing: 8px;
    background: transparent;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #2a3a5c;
    border-radius: 4px;
    background-color: #0f1a30;
}
QCheckBox::indicator:checked {
    background-color: #00d4ff;
    border-color: #00d4ff;
}
QPushButton {
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 13px;
    font-weight: 600;
    min-width: 100px;
}
QPushButton#primaryBtn {
    background-color: #00d4ff;
    color: #0a0a1a;
}
QPushButton#primaryBtn:hover {
    background-color: #00b8e6;
}
QPushButton#secondaryBtn {
    background-color: #2a3a5c;
    color: #e0e0e0;
}
QPushButton#secondaryBtn:hover {
    background-color: #354d73;
}
QPushButton#successBtn {
    background-color: #00e676;
    color: #0a0a1a;
}
QPushButton#successBtn:hover {
    background-color: #00c864;
}
QPushButton#warningBtn {
    background-color: #ff9100;
    color: #0a0a1a;
}
QPushButton#warningBtn:hover {
    background-color: #e08200;
}
QPushButton#dangerBtn {
    background-color: #ff1744;
    color: #ffffff;
}
QPushButton#dangerBtn:hover {
    background-color: #e01540;
}
QPushButton:disabled {
    background-color: #1a2332;
    color: #4a5568;
}
QGroupBox {
    border: 1px solid #2a3a5c;
    border-radius: 8px;
    margin-top: 10px;
    padding-top: 20px;
    font-size: 13px;
    font-weight: 600;
    color: #00d4ff;
    background-color: #0f1a30;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 15px;
    padding: 0 8px;
}
QTextEdit {
    border: 2px solid #2a3a5c;
    border-radius: 8px;
    padding: 10px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 12px;
    background-color: #0a0f1e;
    color: #c8d6e5;
}
QTextEdit:focus {
    border-color: #00d4ff;
}
"""
