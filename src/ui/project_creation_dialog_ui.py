# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'project_creation_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
    QLineEdit, QPushButton, QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(549, 232)
        self.gridLayoutWidget = QWidget(Form)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(9, 9, 531, 211))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.projectNameLineEdit = QLineEdit(self.gridLayoutWidget)
        self.projectNameLineEdit.setObjectName(u"projectNameLineEdit")

        self.gridLayout.addWidget(self.projectNameLineEdit, 0, 1, 1, 1)

        self.projectNameLabel = QLabel(self.gridLayoutWidget)
        self.projectNameLabel.setObjectName(u"projectNameLabel")

        self.gridLayout.addWidget(self.projectNameLabel, 0, 0, 1, 1)

        self.folderSelectLabel = QLabel(self.gridLayoutWidget)
        self.folderSelectLabel.setObjectName(u"folderSelectLabel")

        self.gridLayout.addWidget(self.folderSelectLabel, 1, 0, 1, 1)

        self.folderSelectComboBox = QComboBox(self.gridLayoutWidget)
        self.folderSelectComboBox.setObjectName(u"folderSelectComboBox")

        self.gridLayout.addWidget(self.folderSelectComboBox, 1, 1, 1, 1)

        self.createProjectPushButton = QPushButton(self.gridLayoutWidget)
        self.createProjectPushButton.setObjectName(u"createProjectPushButton")

        self.gridLayout.addWidget(self.createProjectPushButton, 2, 0, 1, 2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.projectNameLabel.setText(QCoreApplication.translate("Form", u"Project name:", None))
        self.folderSelectLabel.setText(QCoreApplication.translate("Form", u"Select folder:", None))
        self.createProjectPushButton.setText(QCoreApplication.translate("Form", u"Create Project", None))
    # retranslateUi

