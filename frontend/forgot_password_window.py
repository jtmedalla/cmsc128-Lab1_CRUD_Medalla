# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'forgot_password_window.ui'
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

class Ui_forgot_password_window(object):
    def setupUi(self, forgot_password_window):
        if not forgot_password_window.objectName():
            forgot_password_window.setObjectName(u"forgot_password_window")
        forgot_password_window.resize(600, 300)
        forgot_password_window.setMinimumSize(QSize(600, 300))
        forgot_password_window.setMaximumSize(QSize(600, 300))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(12)
        forgot_password_window.setFont(font)
        self.centralwidget = QWidget(forgot_password_window)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 581, 221))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.lbl_security_question_1 = QLabel(self.gridLayoutWidget)
        self.lbl_security_question_1.setObjectName(u"lbl_security_question_1")

        self.gridLayout.addWidget(self.lbl_security_question_1, 2, 0, 1, 1)

        self.combo_security_question_2 = QComboBox(self.gridLayoutWidget)
        self.combo_security_question_2.setObjectName(u"combo_security_question_2")

        self.gridLayout.addWidget(self.combo_security_question_2, 4, 1, 1, 1)

        self.lbl_forgot_password = QLabel(self.gridLayoutWidget)
        self.lbl_forgot_password.setObjectName(u"lbl_forgot_password")
        self.lbl_forgot_password.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lbl_forgot_password, 0, 0, 1, 2)

        self.line_answer_1 = QLineEdit(self.gridLayoutWidget)
        self.line_answer_1.setObjectName(u"line_answer_1")

        self.gridLayout.addWidget(self.line_answer_1, 3, 1, 1, 1)

        self.combo_security_question_1 = QComboBox(self.gridLayoutWidget)
        self.combo_security_question_1.setObjectName(u"combo_security_question_1")

        self.gridLayout.addWidget(self.combo_security_question_1, 2, 1, 1, 1)

        self.line_answer_2 = QLineEdit(self.gridLayoutWidget)
        self.line_answer_2.setObjectName(u"line_answer_2")

        self.gridLayout.addWidget(self.line_answer_2, 5, 1, 1, 1)

        self.line_username = QLineEdit(self.gridLayoutWidget)
        self.line_username.setObjectName(u"line_username")

        self.gridLayout.addWidget(self.line_username, 1, 1, 1, 1)

        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 5, 0, 1, 1)

        self.lb_security_question_2 = QLabel(self.gridLayoutWidget)
        self.lb_security_question_2.setObjectName(u"lb_security_question_2")

        self.gridLayout.addWidget(self.lb_security_question_2, 4, 0, 1, 1)

        self.lbl_username = QLabel(self.gridLayoutWidget)
        self.lbl_username.setObjectName(u"lbl_username")

        self.gridLayout.addWidget(self.lbl_username, 1, 0, 1, 1)

        self.lbl_answer = QLabel(self.gridLayoutWidget)
        self.lbl_answer.setObjectName(u"lbl_answer")

        self.gridLayout.addWidget(self.lbl_answer, 3, 0, 1, 1)

        self.lbl_new_password = QLabel(self.gridLayoutWidget)
        self.lbl_new_password.setObjectName(u"lbl_new_password")

        self.gridLayout.addWidget(self.lbl_new_password, 6, 0, 1, 1)

        self.line_new_password = QLineEdit(self.gridLayoutWidget)
        self.line_new_password.setObjectName(u"line_new_password")
        self.line_new_password.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)

        self.gridLayout.addWidget(self.line_new_password, 6, 1, 1, 1)

        self.btn_submit = QPushButton(self.centralwidget)
        self.btn_submit.setObjectName(u"btn_submit")
        self.btn_submit.setGeometry(QRect(140, 240, 151, 26))
        self.btn_cancel = QPushButton(self.centralwidget)
        self.btn_cancel.setObjectName(u"btn_cancel")
        self.btn_cancel.setGeometry(QRect(310, 240, 151, 26))
        forgot_password_window.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(forgot_password_window)
        self.statusbar.setObjectName(u"statusbar")
        forgot_password_window.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.line_username, self.combo_security_question_1)
        QWidget.setTabOrder(self.combo_security_question_1, self.line_answer_1)
        QWidget.setTabOrder(self.line_answer_1, self.combo_security_question_2)
        QWidget.setTabOrder(self.combo_security_question_2, self.line_answer_2)
        QWidget.setTabOrder(self.line_answer_2, self.line_new_password)
        QWidget.setTabOrder(self.line_new_password, self.btn_submit)
        QWidget.setTabOrder(self.btn_submit, self.btn_cancel)

        self.retranslateUi(forgot_password_window)

        QMetaObject.connectSlotsByName(forgot_password_window)
    # setupUi

    def retranslateUi(self, forgot_password_window):
        forgot_password_window.setWindowTitle(QCoreApplication.translate("forgot_password_window", u"Forgot Password", None))
        self.lbl_security_question_1.setText(QCoreApplication.translate("forgot_password_window", u"Security Question 1:", None))
        self.lbl_forgot_password.setText(QCoreApplication.translate("forgot_password_window", u"Forgot Password", None))
        self.label_2.setText(QCoreApplication.translate("forgot_password_window", u"Answer 2:", None))
        self.lb_security_question_2.setText(QCoreApplication.translate("forgot_password_window", u"Security Question 2:", None))
        self.lbl_username.setText(QCoreApplication.translate("forgot_password_window", u"Username:", None))
        self.lbl_answer.setText(QCoreApplication.translate("forgot_password_window", u"Answer 1:", None))
        self.lbl_new_password.setText(QCoreApplication.translate("forgot_password_window", u"New Password:", None))
        self.btn_submit.setText(QCoreApplication.translate("forgot_password_window", u"Submit", None))
        self.btn_cancel.setText(QCoreApplication.translate("forgot_password_window", u"Cancel", None))
    # retranslateUi

