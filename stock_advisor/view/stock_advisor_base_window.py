# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'stock_advisor_base_window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(701, 285)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rsiBtn = QPushButton(self.centralwidget)
        self.rsiBtn.setObjectName(u"rsiBtn")
        self.rsiBtn.setGeometry(QRect(180, 120, 112, 32))
        self.ema44Btn = QPushButton(self.centralwidget)
        self.ema44Btn.setObjectName(u"ema44Btn")
        self.ema44Btn.setGeometry(QRect(460, 130, 112, 32))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 701, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"StockAdvisor Home", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.rsiBtn.setText(QCoreApplication.translate("MainWindow", u"rsi", None))
        self.ema44Btn.setText(QCoreApplication.translate("MainWindow", u"ema 44", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

