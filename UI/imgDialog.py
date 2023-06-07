import typing
from PyQt6.QtWidgets import *
from PyQt6 import QtCore, uic
from PyQt6.QtWidgets import QWidget

class imgDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi("UI/imgDialog.ui", self)      