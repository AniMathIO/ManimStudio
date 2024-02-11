# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'project_opening_dialog.ui'
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
    QPushButton, QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(680, 139)
        self.gridLayoutWidget = QWidget(Form)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(9, 9, 661, 121))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.projectSelectComboBox = QComboBox(self.gridLayoutWidget)
        self.projectSelectComboBox.setObjectName(u"projectSelectComboBox")

        self.gridLayout.addWidget(self.projectSelectComboBox, 0, 1, 1, 1)

        self.projectSelectLabel = QLabel(self.gridLayoutWidget)
        self.projectSelectLabel.setObjectName(u"projectSelectLabel")

        self.gridLayout.addWidget(self.projectSelectLabel, 0, 0, 1, 1)

        self.openProjectPushButton = QPushButton(self.gridLayoutWidget)
        self.openProjectPushButton.setObjectName(u"openProjectPushButton")

        self.gridLayout.addWidget(self.openProjectPushButton, 1, 0, 1, 2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.projectSelectLabel.setText(QCoreApplication.translate("Form", u"Select project:", None))
        self.openProjectPushButton.setText(QCoreApplication.translate("Form", u"Open Project", None))
    # retranslateUi

