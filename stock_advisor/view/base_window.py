import logging
import random
import sys
from time import sleep

from PyQt5.QtCore import QMutex, QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

logging.basicConfig(format="%(message)s", level=logging.INFO)

balance = 100.00
mutex = QMutex()

