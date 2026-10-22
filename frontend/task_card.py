# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'task_card.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QLabel, QSizePolicy, QWidget)

class Ui_frm_add_task(object):
    def setupUi(self, frm_add_task):
        if not frm_add_task.objectName():
            frm_add_task.setObjectName(u"frm_add_task")
        frm_add_task.resize(750, 128)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(frm_add_task.sizePolicy().hasHeightForWidth())
        frm_add_task.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies([u"Arial"])
        frm_add_task.setFont(font)
        self.gridLayoutWidget = QWidget(frm_add_task)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 731, 113))
        self.tasklayout = QGridLayout(self.gridLayoutWidget)
        self.tasklayout.setObjectName(u"tasklayout")
        self.tasklayout.setContentsMargins(0, 0, 0, 0)
        self.lbl_placeholder_due = QLabel(self.gridLayoutWidget)
        self.lbl_placeholder_due.setObjectName(u"lbl_placeholder_due")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lbl_placeholder_due.sizePolicy().hasHeightForWidth())
        self.lbl_placeholder_due.setSizePolicy(sizePolicy1)

        self.tasklayout.addWidget(self.lbl_placeholder_due, 1, 3, 1, 1)

        self.lbl_placeholder_priority = QLabel(self.gridLayoutWidget)
        self.lbl_placeholder_priority.setObjectName(u"lbl_placeholder_priority")
        sizePolicy1.setHeightForWidth(self.lbl_placeholder_priority.sizePolicy().hasHeightForWidth())
        self.lbl_placeholder_priority.setSizePolicy(sizePolicy1)

        self.tasklayout.addWidget(self.lbl_placeholder_priority, 2, 3, 1, 1)

        self.lbl_details = QLabel(self.gridLayoutWidget)
        self.lbl_details.setObjectName(u"lbl_details")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lbl_details.sizePolicy().hasHeightForWidth())
        self.lbl_details.setSizePolicy(sizePolicy2)

        self.tasklayout.addWidget(self.lbl_details, 1, 1, 1, 1)

        self.lbl_date_added = QLabel(self.gridLayoutWidget)
        self.lbl_date_added.setObjectName(u"lbl_date_added")
        sizePolicy1.setHeightForWidth(self.lbl_date_added.sizePolicy().hasHeightForWidth())
        self.lbl_date_added.setSizePolicy(sizePolicy1)

        self.tasklayout.addWidget(self.lbl_date_added, 0, 2, 1, 1)

        self.lbl_priority = QLabel(self.gridLayoutWidget)
        self.lbl_priority.setObjectName(u"lbl_priority")
        sizePolicy1.setHeightForWidth(self.lbl_priority.sizePolicy().hasHeightForWidth())
        self.lbl_priority.setSizePolicy(sizePolicy1)

        self.tasklayout.addWidget(self.lbl_priority, 2, 2, 1, 1)

        self.lbl_placeholder_title = QLabel(self.gridLayoutWidget)
        self.lbl_placeholder_title.setObjectName(u"lbl_placeholder_title")
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(16)
        font1.setBold(True)
        self.lbl_placeholder_title.setFont(font1)

        self.tasklayout.addWidget(self.lbl_placeholder_title, 0, 1, 1, 1)

        self.lbl_category = QLabel(self.gridLayoutWidget)
        self.lbl_category.setObjectName(u"lbl_category")
        sizePolicy1.setHeightForWidth(self.lbl_category.sizePolicy().hasHeightForWidth())
        self.lbl_category.setSizePolicy(sizePolicy1)

        self.tasklayout.addWidget(self.lbl_category, 3, 2, 1, 1)

        self.lbl_placeholder_added = QLabel(self.gridLayoutWidget)
        self.lbl_placeholder_added.setObjectName(u"lbl_placeholder_added")
        sizePolicy1.setHeightForWidth(self.lbl_placeholder_added.sizePolicy().hasHeightForWidth())
        self.lbl_placeholder_added.setSizePolicy(sizePolicy1)

        self.tasklayout.addWidget(self.lbl_placeholder_added, 0, 3, 1, 1)

        self.lbl_date_due = QLabel(self.gridLayoutWidget)
        self.lbl_date_due.setObjectName(u"lbl_date_due")
        sizePolicy1.setHeightForWidth(self.lbl_date_due.sizePolicy().hasHeightForWidth())
        self.lbl_date_due.setSizePolicy(sizePolicy1)

        self.tasklayout.addWidget(self.lbl_date_due, 1, 2, 1, 1)

        self.lbl_placeholder_details = QLabel(self.gridLayoutWidget)
        self.lbl_placeholder_details.setObjectName(u"lbl_placeholder_details")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.lbl_placeholder_details.sizePolicy().hasHeightForWidth())
        self.lbl_placeholder_details.setSizePolicy(sizePolicy3)
        self.lbl_placeholder_details.setTextFormat(Qt.TextFormat.PlainText)
        self.lbl_placeholder_details.setWordWrap(True)

        self.tasklayout.addWidget(self.lbl_placeholder_details, 2, 1, 2, 1)

        self.chkbox_is_complete = QCheckBox(self.gridLayoutWidget)
        self.chkbox_is_complete.setObjectName(u"chkbox_is_complete")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.chkbox_is_complete.sizePolicy().hasHeightForWidth())
        self.chkbox_is_complete.setSizePolicy(sizePolicy4)
        self.chkbox_is_complete.setStyleSheet(u"QCheckBox::indicator{width:16px, height:16px};")

        self.tasklayout.addWidget(self.chkbox_is_complete, 1, 0, 2, 1)

        self.hline_bottom = QFrame(self.gridLayoutWidget)
        self.hline_bottom.setObjectName(u"hline_bottom")
        self.hline_bottom.setFrameShadow(QFrame.Shadow.Plain)
        self.hline_bottom.setLineWidth(2)
        self.hline_bottom.setFrameShape(QFrame.Shape.HLine)

        self.tasklayout.addWidget(self.hline_bottom, 4, 0, 1, 4)

        self.lbl_placeholder_category = QLabel(self.gridLayoutWidget)
        self.lbl_placeholder_category.setObjectName(u"lbl_placeholder_category")
        sizePolicy2.setHeightForWidth(self.lbl_placeholder_category.sizePolicy().hasHeightForWidth())
        self.lbl_placeholder_category.setSizePolicy(sizePolicy2)
        self.lbl_placeholder_category.setWordWrap(True)

        self.tasklayout.addWidget(self.lbl_placeholder_category, 3, 3, 1, 1)


        self.retranslateUi(frm_add_task)

        QMetaObject.connectSlotsByName(frm_add_task)
    # setupUi

    def retranslateUi(self, frm_add_task):
        frm_add_task.setWindowTitle(QCoreApplication.translate("frm_add_task", u"Frame", None))
        self.lbl_placeholder_due.setText(QCoreApplication.translate("frm_add_task", u"[12/12/2077]", None))
        self.lbl_placeholder_priority.setText(QCoreApplication.translate("frm_add_task", u"[Medium]", None))
        self.lbl_details.setText(QCoreApplication.translate("frm_add_task", u"Details:                                                                                       ", None))
        self.lbl_date_added.setText(QCoreApplication.translate("frm_add_task", u"Date Added:", None))
        self.lbl_priority.setText(QCoreApplication.translate("frm_add_task", u"Priority:", None))
        self.lbl_placeholder_title.setText(QCoreApplication.translate("frm_add_task", u"[Title]", None))
        self.lbl_category.setText(QCoreApplication.translate("frm_add_task", u"Category:", None))
        self.lbl_placeholder_added.setText(QCoreApplication.translate("frm_add_task", u"[12/12/2077", None))
        self.lbl_date_due.setText(QCoreApplication.translate("frm_add_task", u"Due Date:", None))
        self.lbl_placeholder_details.setText(QCoreApplication.translate("frm_add_task", u"[description]", None))
        self.chkbox_is_complete.setText("")
        self.lbl_placeholder_category.setText(QCoreApplication.translate("frm_add_task", u"[This is a very long category]", None))
    # retranslateUi

