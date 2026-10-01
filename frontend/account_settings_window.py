# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'account_settings_window.ui'
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
    QPushButton, QSizePolicy, QWidget)

class Ui_account_settings_window(object):
    def setupUi(self, account_settings_window):
        if not account_settings_window.objectName():
            account_settings_window.setObjectName(u"account_settings_window")
        account_settings_window.resize(654, 289)
        self.gridLayoutWidget = QWidget(account_settings_window)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 631, 161))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.line_new_pwd = QLineEdit(self.gridLayoutWidget)
        self.line_new_pwd.setObjectName(u"line_new_pwd")
        self.line_new_pwd.setEchoMode(QLineEdit.EchoMode.Password)

        self.gridLayout.addWidget(self.line_new_pwd, 4, 1, 1, 1)

        self.lbl_update_pwd = QLabel(self.gridLayoutWidget)
        self.lbl_update_pwd.setObjectName(u"lbl_update_pwd")
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(12)
        self.lbl_update_pwd.setFont(font)

        self.gridLayout.addWidget(self.lbl_update_pwd, 3, 0, 1, 1)

        self.line_curr_pwd = QLineEdit(self.gridLayoutWidget)
        self.line_curr_pwd.setObjectName(u"line_curr_pwd")
        self.line_curr_pwd.setEchoMode(QLineEdit.EchoMode.Password)

        self.gridLayout.addWidget(self.line_curr_pwd, 3, 1, 1, 1)

        self.line_update_usrname = QLineEdit(self.gridLayoutWidget)
        self.line_update_usrname.setObjectName(u"line_update_usrname")

        self.gridLayout.addWidget(self.line_update_usrname, 1, 1, 1, 1)

        self.lbl_new_pass = QLabel(self.gridLayoutWidget)
        self.lbl_new_pass.setObjectName(u"lbl_new_pass")
        self.lbl_new_pass.setFont(font)

        self.gridLayout.addWidget(self.lbl_new_pass, 4, 0, 1, 1)

        self.lbl_update_usrname = QLabel(self.gridLayoutWidget)
        self.lbl_update_usrname.setObjectName(u"lbl_update_usrname")
        self.lbl_update_usrname.setFont(font)

        self.gridLayout.addWidget(self.lbl_update_usrname, 1, 0, 1, 1)

        self.lbl_update_acc_dets = QLabel(self.gridLayoutWidget)
        self.lbl_update_acc_dets.setObjectName(u"lbl_update_acc_dets")
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(12)
        font1.setBold(True)
        self.lbl_update_acc_dets.setFont(font1)
        self.lbl_update_acc_dets.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lbl_update_acc_dets, 0, 0, 1, 2)

        self.lbl_instruction = QLabel(self.gridLayoutWidget)
        self.lbl_instruction.setObjectName(u"lbl_instruction")
        self.lbl_instruction.setFont(font)
        self.lbl_instruction.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lbl_instruction, 2, 0, 1, 2)

        self.btn_update_cancel = QPushButton(account_settings_window)
        self.btn_update_cancel.setObjectName(u"btn_update_cancel")
        self.btn_update_cancel.setGeometry(QRect(390, 180, 201, 26))
        self.btn_update_dets = QPushButton(account_settings_window)
        self.btn_update_dets.setObjectName(u"btn_update_dets")
        self.btn_update_dets.setGeometry(QRect(50, 180, 201, 26))
        self.btn_logout = QPushButton(account_settings_window)
        self.btn_logout.setObjectName(u"btn_logout")
        self.btn_logout.setGeometry(QRect(220, 230, 201, 26))

        self.retranslateUi(account_settings_window)

        QMetaObject.connectSlotsByName(account_settings_window)
    # setupUi

    def retranslateUi(self, account_settings_window):
        account_settings_window.setWindowTitle(QCoreApplication.translate("account_settings_window", u"Form", None))
        self.lbl_update_pwd.setText(QCoreApplication.translate("account_settings_window", u"Current Password:", None))
        self.lbl_new_pass.setText(QCoreApplication.translate("account_settings_window", u"New Password:", None))
        self.lbl_update_usrname.setText(QCoreApplication.translate("account_settings_window", u"Username:", None))
        self.lbl_update_acc_dets.setText(QCoreApplication.translate("account_settings_window", u"Update Account Details", None))
        self.lbl_instruction.setText(QCoreApplication.translate("account_settings_window", u"Input current password to update account details:", None))
        self.btn_update_cancel.setText(QCoreApplication.translate("account_settings_window", u"Cancel", None))
        self.btn_update_dets.setText(QCoreApplication.translate("account_settings_window", u"Update Account Details", None))
        self.btn_logout.setText(QCoreApplication.translate("account_settings_window", u"Log Out", None))
    # retranslateUi

