# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFontComboBox, QFormLayout,
    QGridLayout, QLabel, QPushButton, QSizePolicy,
    QSpinBox, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(479, 169)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.fontSizeLabel = QLabel(Form)
        self.fontSizeLabel.setObjectName(u"fontSizeLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.fontSizeLabel)

        self.fontSizeSpinBox = QSpinBox(Form)
        self.fontSizeSpinBox.setObjectName(u"fontSizeSpinBox")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.fontSizeSpinBox)

        self.fontFamilyLabel = QLabel(Form)
        self.fontFamilyLabel.setObjectName(u"fontFamilyLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.fontFamilyLabel)

        self.fontComboBox = QFontComboBox(Form)
        self.fontComboBox.setObjectName(u"fontComboBox")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.fontComboBox)

        self.themeLabel = QLabel(Form)
        self.themeLabel.setObjectName(u"themeLabel")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.themeLabel)

        self.themeComboBox = QComboBox(Form)
        self.themeComboBox.setObjectName(u"themeComboBox")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.themeComboBox)


        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)

        self.saveSettingsBtn = QPushButton(Form)
        self.saveSettingsBtn.setObjectName(u"saveSettingsBtn")

        self.gridLayout.addWidget(self.saveSettingsBtn, 1, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.fontSizeLabel.setText(QCoreApplication.translate("Form", u"Fontsize:", None))
        self.fontFamilyLabel.setText(QCoreApplication.translate("Form", u"Font Family:", None))
        self.themeLabel.setText(QCoreApplication.translate("Form", u"Theme:", None))
        self.saveSettingsBtn.setText(QCoreApplication.translate("Form", u"Save Settings", None))
    # retranslateUi

