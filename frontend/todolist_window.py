# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'todolist_window.ui'
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
    QMainWindow, QPushButton, QSizePolicy, QStatusBar,
    QTabWidget, QWidget)

class Ui_todolist_window(object):
    def setupUi(self, todolist_window):
        if not todolist_window.objectName():
            todolist_window.setObjectName(u"todolist_window")
        todolist_window.resize(800, 636)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(todolist_window.sizePolicy().hasHeightForWidth())
        todolist_window.setSizePolicy(sizePolicy)
        todolist_window.setMinimumSize(QSize(800, 636))
        todolist_window.setMaximumSize(QSize(800, 636))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(12)
        todolist_window.setFont(font)
        self.centralwidget = QWidget(todolist_window)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 781, 191))
        self.layout_options = QGridLayout(self.gridLayoutWidget)
        self.layout_options.setObjectName(u"layout_options")
        self.layout_options.setContentsMargins(0, 0, 0, 0)
        self.lbl_filter_cat = QLabel(self.gridLayoutWidget)
        self.lbl_filter_cat.setObjectName(u"lbl_filter_cat")
        self.lbl_filter_cat.setFont(font)

        self.layout_options.addWidget(self.lbl_filter_cat, 4, 0, 1, 1)

        self.lbl_sort = QLabel(self.gridLayoutWidget)
        self.lbl_sort.setObjectName(u"lbl_sort")
        self.lbl_sort.setFont(font)

        self.layout_options.addWidget(self.lbl_sort, 6, 0, 1, 1)

        self.lbl_todo_title = QLabel(self.gridLayoutWidget)
        self.lbl_todo_title.setObjectName(u"lbl_todo_title")
        font1 = QFont()
        font1.setFamilies([u"Arial Black"])
        font1.setPointSize(20)
        font1.setBold(True)
        self.lbl_todo_title.setFont(font1)
        self.lbl_todo_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_options.addWidget(self.lbl_todo_title, 1, 0, 1, 2)

        self.lbl_filter_prio = QLabel(self.gridLayoutWidget)
        self.lbl_filter_prio.setObjectName(u"lbl_filter_prio")
        self.lbl_filter_prio.setFont(font)

        self.layout_options.addWidget(self.lbl_filter_prio, 5, 0, 1, 1)

        self.combo_category = QComboBox(self.gridLayoutWidget)
        self.combo_category.setObjectName(u"combo_category")

        self.layout_options.addWidget(self.combo_category, 4, 1, 1, 1)

        self.combo_sort = QComboBox(self.gridLayoutWidget)
        self.combo_sort.setObjectName(u"combo_sort")

        self.layout_options.addWidget(self.combo_sort, 6, 1, 1, 1)

        self.combo_priority = QComboBox(self.gridLayoutWidget)
        self.combo_priority.setObjectName(u"combo_priority")

        self.layout_options.addWidget(self.combo_priority, 5, 1, 1, 1)

        self.lbl_welcome = QLabel(self.gridLayoutWidget)
        self.lbl_welcome.setObjectName(u"lbl_welcome")
        self.lbl_welcome.setFont(font)

        self.layout_options.addWidget(self.lbl_welcome, 0, 0, 1, 1)

        self.btn_acc_settings = QPushButton(self.gridLayoutWidget)
        self.btn_acc_settings.setObjectName(u"btn_acc_settings")
        self.btn_acc_settings.setFont(font)

        self.layout_options.addWidget(self.btn_acc_settings, 0, 1, 1, 1)

        self.tabs_tasks = QTabWidget(self.centralwidget)
        self.tabs_tasks.setObjectName(u"tabs_tasks")
        self.tabs_tasks.setGeometry(QRect(10, 210, 781, 401))
        self.tabs_tasks.setFont(font)
        self.tab_ongoing_tasks = QWidget()
        self.tab_ongoing_tasks.setObjectName(u"tab_ongoing_tasks")
        self.tabs_tasks.addTab(self.tab_ongoing_tasks, "")
        self.tab_completed_tasks = QWidget()
        self.tab_completed_tasks.setObjectName(u"tab_completed_tasks")
        self.tabs_tasks.addTab(self.tab_completed_tasks, "")
        todolist_window.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(todolist_window)
        self.statusbar.setObjectName(u"statusbar")
        todolist_window.setStatusBar(self.statusbar)

        self.retranslateUi(todolist_window)

        self.tabs_tasks.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(todolist_window)
    # setupUi

    def retranslateUi(self, todolist_window):
        todolist_window.setWindowTitle(QCoreApplication.translate("todolist_window", u"To Do List", None))
        self.lbl_filter_cat.setText(QCoreApplication.translate("todolist_window", u"Filter By Category:", None))
        self.lbl_sort.setText(QCoreApplication.translate("todolist_window", u"Sort by:", None))
        self.lbl_todo_title.setText(QCoreApplication.translate("todolist_window", u"To Do List", None))
        self.lbl_filter_prio.setText(QCoreApplication.translate("todolist_window", u"Filter by Priority:", None))
        self.lbl_welcome.setText(QCoreApplication.translate("todolist_window", u"Welcome, [Username]", None))
        self.btn_acc_settings.setText(QCoreApplication.translate("todolist_window", u"Account Settings", None))
        self.tabs_tasks.setTabText(self.tabs_tasks.indexOf(self.tab_ongoing_tasks), QCoreApplication.translate("todolist_window", u"Ongoing Tasks", None))
        self.tabs_tasks.setTabText(self.tabs_tasks.indexOf(self.tab_completed_tasks), QCoreApplication.translate("todolist_window", u"Completed Tasks", None))
    # retranslateUi

