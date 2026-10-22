# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'edit_task.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QFormLayout,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QStatusBar, QTextEdit, QWidget)

class Ui_window_add_task(object):
    def setupUi(self, window_add_task):
        if not window_add_task.objectName():
            window_add_task.setObjectName(u"window_add_task")
        window_add_task.resize(477, 330)
        font = QFont()
        font.setFamilies([u"Arial"])
        window_add_task.setFont(font)
        self.centralwidget = QWidget(window_add_task)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setFont(font)
        self.formLayoutWidget = QWidget(self.centralwidget)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(10, 10, 461, 291))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.lbl_title = QLabel(self.formLayoutWidget)
        self.lbl_title.setObjectName(u"lbl_title")
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(24)
        font1.setBold(True)
        self.lbl_title.setFont(font1)
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.SpanningRole, self.lbl_title)

        self.lb_title = QLabel(self.formLayoutWidget)
        self.lb_title.setObjectName(u"lb_title")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lb_title)

        self.line_title = QLineEdit(self.formLayoutWidget)
        self.line_title.setObjectName(u"line_title")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.line_title)

        self.lbl_date_due = QLabel(self.formLayoutWidget)
        self.lbl_date_due.setObjectName(u"lbl_date_due")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lbl_date_due)

        self.date_date_due = QDateEdit(self.formLayoutWidget)
        self.date_date_due.setObjectName(u"date_date_due")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.date_date_due)

        self.lbl_priority = QLabel(self.formLayoutWidget)
        self.lbl_priority.setObjectName(u"lbl_priority")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lbl_priority)

        self.cmb_priority = QComboBox(self.formLayoutWidget)
        self.cmb_priority.setObjectName(u"cmb_priority")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.cmb_priority)

        self.lb_category = QLabel(self.formLayoutWidget)
        self.lb_category.setObjectName(u"lb_category")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.lb_category)

        self.line_category = QLineEdit(self.formLayoutWidget)
        self.line_category.setObjectName(u"line_category")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.line_category)

        self.lbl_details = QLabel(self.formLayoutWidget)
        self.lbl_details.setObjectName(u"lbl_details")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.lbl_details)

        self.textEdit = QTextEdit(self.formLayoutWidget)
        self.textEdit.setObjectName(u"textEdit")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.textEdit)

        self.btn_add_task = QPushButton(self.formLayoutWidget)
        self.btn_add_task.setObjectName(u"btn_add_task")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.SpanningRole, self.btn_add_task)

        window_add_task.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(window_add_task)
        self.statusbar.setObjectName(u"statusbar")
        window_add_task.setStatusBar(self.statusbar)

        self.retranslateUi(window_add_task)

        QMetaObject.connectSlotsByName(window_add_task)
    # setupUi

    def retranslateUi(self, window_add_task):
        window_add_task.setWindowTitle(QCoreApplication.translate("window_add_task", u"MainWindow", None))
        self.lbl_title.setText(QCoreApplication.translate("window_add_task", u"Task Details", None))
        self.lb_title.setText(QCoreApplication.translate("window_add_task", u"Title:", None))
        self.lbl_date_due.setText(QCoreApplication.translate("window_add_task", u"Date Due:", None))
        self.lbl_priority.setText(QCoreApplication.translate("window_add_task", u"Priority: ", None))
        self.lb_category.setText(QCoreApplication.translate("window_add_task", u"Category: ", None))
        self.lbl_details.setText(QCoreApplication.translate("window_add_task", u"Details:", None))
        self.btn_add_task.setText(QCoreApplication.translate("window_add_task", u"Update Task", None))
    # retranslateUi

