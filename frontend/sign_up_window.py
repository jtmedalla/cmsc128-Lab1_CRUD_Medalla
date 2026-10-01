# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sign_up_window.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QStatusBar, QWidget)

class Ui_create_account_window(object):
    def setupUi(self, create_account_window):
        if not create_account_window.objectName():
            create_account_window.setObjectName(u"create_account_window")
        create_account_window.resize(574, 300)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(create_account_window.sizePolicy().hasHeightForWidth())
        create_account_window.setSizePolicy(sizePolicy)
        create_account_window.setMinimumSize(QSize(574, 300))
        create_account_window.setMaximumSize(QSize(574, 300))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(12)
        create_account_window.setFont(font)
        self.centralwidget = QWidget(create_account_window)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 551, 189))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.lbl_create_account = QLabel(self.gridLayoutWidget)
        self.lbl_create_account.setObjectName(u"lbl_create_account")
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(20)
        font1.setBold(True)
        self.lbl_create_account.setFont(font1)
        self.lbl_create_account.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lbl_create_account, 0, 0, 1, 2)

        self.line_new_password = QLineEdit(self.gridLayoutWidget)
        self.line_new_password.setObjectName(u"line_new_password")
        self.line_new_password.setFont(font)
        self.line_new_password.setMaxLength(64)
        self.line_new_password.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)

        self.gridLayout.addWidget(self.line_new_password, 2, 1, 1, 1)

        self.lbl_confirm_password = QLabel(self.gridLayoutWidget)
        self.lbl_confirm_password.setObjectName(u"lbl_confirm_password")
        self.lbl_confirm_password.setFont(font)

        self.gridLayout.addWidget(self.lbl_confirm_password, 3, 0, 1, 1)

        self.lbl_new_password = QLabel(self.gridLayoutWidget)
        self.lbl_new_password.setObjectName(u"lbl_new_password")
        self.lbl_new_password.setFont(font)

        self.gridLayout.addWidget(self.lbl_new_password, 2, 0, 1, 1)

        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.line_new_username = QLineEdit(self.gridLayoutWidget)
        self.line_new_username.setObjectName(u"line_new_username")
        self.line_new_username.setFont(font)
        self.line_new_username.setMaxLength(32)

        self.gridLayout.addWidget(self.line_new_username, 1, 1, 1, 1)

        self.cmb_security = QComboBox(self.gridLayoutWidget)
        self.cmb_security.setObjectName(u"cmb_security")

        self.gridLayout.addWidget(self.cmb_security, 4, 1, 1, 1)

        self.line_confirm_password = QLineEdit(self.gridLayoutWidget)
        self.line_confirm_password.setObjectName(u"line_confirm_password")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.line_confirm_password.sizePolicy().hasHeightForWidth())
        self.line_confirm_password.setSizePolicy(sizePolicy1)
        self.line_confirm_password.setFont(font)
        self.line_confirm_password.setMaxLength(64)
        self.line_confirm_password.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)

        self.gridLayout.addWidget(self.line_confirm_password, 3, 1, 1, 1)

        self.lbl_security_question = QLabel(self.gridLayoutWidget)
        self.lbl_security_question.setObjectName(u"lbl_security_question")

        self.gridLayout.addWidget(self.lbl_security_question, 4, 0, 1, 1)

        self.lbl_answer = QLabel(self.gridLayoutWidget)
        self.lbl_answer.setObjectName(u"lbl_answer")

        self.gridLayout.addWidget(self.lbl_answer, 5, 0, 1, 1)

        self.lineEdit = QLineEdit(self.gridLayoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout.addWidget(self.lineEdit, 5, 1, 1, 1)

        self.btn_create_acc = QPushButton(self.centralwidget)
        self.btn_create_acc.setObjectName(u"btn_create_acc")
        self.btn_create_acc.setGeometry(QRect(100, 210, 151, 31))
        self.btn_cancel = QPushButton(self.centralwidget)
        self.btn_cancel.setObjectName(u"btn_cancel")
        self.btn_cancel.setGeometry(QRect(280, 210, 151, 31))
        create_account_window.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(create_account_window)
        self.statusbar.setObjectName(u"statusbar")
        create_account_window.setStatusBar(self.statusbar)

        self.retranslateUi(create_account_window)

        QMetaObject.connectSlotsByName(create_account_window)
    # setupUi

    def retranslateUi(self, create_account_window):
        create_account_window.setWindowTitle(QCoreApplication.translate("create_account_window", u"Create an Account", None))
        self.lbl_create_account.setText(QCoreApplication.translate("create_account_window", u"Create An Account:", None))
        self.lbl_confirm_password.setText(QCoreApplication.translate("create_account_window", u"Confirm Password:", None))
        self.lbl_new_password.setText(QCoreApplication.translate("create_account_window", u"New Password:", None))
        self.label.setText(QCoreApplication.translate("create_account_window", u"New Username:", None))
        self.lbl_security_question.setText(QCoreApplication.translate("create_account_window", u"Recovery Question", None))
        self.lbl_answer.setText(QCoreApplication.translate("create_account_window", u"Answer:", None))
        self.btn_create_acc.setText(QCoreApplication.translate("create_account_window", u"Create Account", None))
        self.btn_cancel.setText(QCoreApplication.translate("create_account_window", u"Cancel", None))
    # retranslateUi

