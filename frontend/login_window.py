# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login_window.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QStatusBar, QWidget)

class Ui_login_window(object):
    def setupUi(self, login_window):
        if not login_window.objectName():
            login_window.setObjectName(u"login_window")
        login_window.resize(628, 395)
        self.centralwidget = QWidget(login_window)
        self.centralwidget.setObjectName(u"centralwidget")
        self.lbl_title = QLabel(self.centralwidget)
        self.lbl_title.setObjectName(u"lbl_title")
        self.lbl_title.setGeometry(QRect(210, 70, 171, 41))
        font = QFont()
        font.setFamilies([u"Arial Black"])
        font.setPointSize(18)
        font.setBold(True)
        self.lbl_title.setFont(font)
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.lbl_username = QLabel(self.centralwidget)
        self.lbl_username.setObjectName(u"lbl_username")
        self.lbl_username.setGeometry(QRect(150, 120, 81, 18))
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(12)
        self.lbl_username.setFont(font1)
        self.line_username = QLineEdit(self.centralwidget)
        self.line_username.setObjectName(u"line_username")
        self.line_username.setGeometry(QRect(150, 140, 311, 26))
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        self.line_username.setFont(font2)
        self.lbl_password = QLabel(self.centralwidget)
        self.lbl_password.setObjectName(u"lbl_password")
        self.lbl_password.setGeometry(QRect(150, 180, 81, 18))
        self.lbl_password.setFont(font1)
        self.line_password = QLineEdit(self.centralwidget)
        self.line_password.setObjectName(u"line_password")
        self.line_password.setGeometry(QRect(150, 200, 311, 26))
        self.line_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.btn_login = QPushButton(self.centralwidget)
        self.btn_login.setObjectName(u"btn_login")
        self.btn_login.setGeometry(QRect(160, 250, 131, 31))
        self.btn_signup = QPushButton(self.centralwidget)
        self.btn_signup.setObjectName(u"btn_signup")
        self.btn_signup.setGeometry(QRect(320, 250, 131, 31))
        login_window.setCentralWidget(self.centralwidget)
        self.lbl_password.raise_()
        self.line_password.raise_()
        self.lbl_title.raise_()
        self.btn_signup.raise_()
        self.line_username.raise_()
        self.lbl_username.raise_()
        self.btn_login.raise_()
        self.statusbar = QStatusBar(login_window)
        self.statusbar.setObjectName(u"statusbar")
        login_window.setStatusBar(self.statusbar)

        self.retranslateUi(login_window)

        QMetaObject.connectSlotsByName(login_window)
    # setupUi

    def retranslateUi(self, login_window):
        login_window.setWindowTitle(QCoreApplication.translate("login_window", u"Form", None))
        self.lbl_title.setText(QCoreApplication.translate("login_window", u"To-Do List", None))
        self.lbl_username.setText(QCoreApplication.translate("login_window", u"Username:", None))
        self.lbl_password.setText(QCoreApplication.translate("login_window", u"Password:", None))
        self.line_password.setInputMask("")
        self.line_password.setText("")
        self.btn_login.setText(QCoreApplication.translate("login_window", u"Login", None))
        self.btn_signup.setText(QCoreApplication.translate("login_window", u"Sign Up", None))
    # retranslateUi

