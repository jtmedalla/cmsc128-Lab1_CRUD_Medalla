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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QStatusBar,
    QWidget)

class Ui_login_window(object):
    def setupUi(self, login_window):
        if not login_window.objectName():
            login_window.setObjectName(u"login_window")
        login_window.resize(567, 255)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(login_window.sizePolicy().hasHeightForWidth())
        login_window.setSizePolicy(sizePolicy)
        login_window.setMinimumSize(QSize(567, 255))
        login_window.setMaximumSize(QSize(567, 255))
        self.centralwidget = QWidget(login_window)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(80, 20, 401, 207))
        self.login_layout = QGridLayout(self.gridLayoutWidget)
        self.login_layout.setObjectName(u"login_layout")
        self.login_layout.setContentsMargins(0, 0, 0, 0)
        self.lbl_password = QLabel(self.gridLayoutWidget)
        self.lbl_password.setObjectName(u"lbl_password")
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(12)
        self.lbl_password.setFont(font)

        self.login_layout.addWidget(self.lbl_password, 3, 0, 1, 2)

        self.btn_signup = QPushButton(self.gridLayoutWidget)
        self.btn_signup.setObjectName(u"btn_signup")
        self.btn_signup.setFont(font)

        self.login_layout.addWidget(self.btn_signup, 6, 1, 1, 1)

        self.lbl_username = QLabel(self.gridLayoutWidget)
        self.lbl_username.setObjectName(u"lbl_username")
        self.lbl_username.setFont(font)

        self.login_layout.addWidget(self.lbl_username, 1, 0, 1, 2)

        self.lbl_title = QLabel(self.gridLayoutWidget)
        self.lbl_title.setObjectName(u"lbl_title")
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(20)
        font1.setBold(True)
        self.lbl_title.setFont(font1)
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)

        self.login_layout.addWidget(self.lbl_title, 0, 0, 1, 2)

        self.line_password = QLineEdit(self.gridLayoutWidget)
        self.line_password.setObjectName(u"line_password")
        self.line_password.setFont(font)
        self.line_password.setMaxLength(64)
        self.line_password.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)

        self.login_layout.addWidget(self.line_password, 4, 0, 1, 2)

        self.line_username = QLineEdit(self.gridLayoutWidget)
        self.line_username.setObjectName(u"line_username")
        self.line_username.setFont(font)
        self.line_username.setMaxLength(32)

        self.login_layout.addWidget(self.line_username, 2, 0, 1, 2)

        self.btn_login = QPushButton(self.gridLayoutWidget)
        self.btn_login.setObjectName(u"btn_login")
        self.btn_login.setFont(font)

        self.login_layout.addWidget(self.btn_login, 6, 0, 1, 1)

        self.btn_forgot_password = QPushButton(self.gridLayoutWidget)
        self.btn_forgot_password.setObjectName(u"btn_forgot_password")
        self.btn_forgot_password.setFont(font)

        self.login_layout.addWidget(self.btn_forgot_password, 7, 0, 1, 2)

        login_window.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(login_window)
        self.statusbar.setObjectName(u"statusbar")
        login_window.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.line_username, self.line_password)
        QWidget.setTabOrder(self.line_password, self.btn_login)
        QWidget.setTabOrder(self.btn_login, self.btn_signup)

        self.retranslateUi(login_window)

        QMetaObject.connectSlotsByName(login_window)
    # setupUi

    def retranslateUi(self, login_window):
        login_window.setWindowTitle(QCoreApplication.translate("login_window", u"Log In", None))
        self.lbl_password.setText(QCoreApplication.translate("login_window", u"Password:", None))
        self.btn_signup.setText(QCoreApplication.translate("login_window", u"Sign Up", None))
        self.lbl_username.setText(QCoreApplication.translate("login_window", u"Username:", None))
        self.lbl_title.setText(QCoreApplication.translate("login_window", u"To-Do List", None))
        self.line_password.setInputMask("")
        self.line_password.setText("")
        self.btn_login.setText(QCoreApplication.translate("login_window", u"Login", None))
        self.btn_forgot_password.setText(QCoreApplication.translate("login_window", u"Forgot Password?", None))
    # retranslateUi

