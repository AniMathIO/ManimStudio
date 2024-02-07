# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'videoeditor.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLayout,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QSlider, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(790, 576)
        self.gridLayoutWidget = QWidget(Form)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(9, 9, 771, 561))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setSizeConstraint(QLayout.SetMinimumSize)
        self.backwardBtn = QPushButton(self.gridLayoutWidget)
        self.backwardBtn.setObjectName(u"backwardBtn")

        self.gridLayout_2.addWidget(self.backwardBtn, 0, 1, 1, 1)

        self.backwardToEndBtn = QPushButton(self.gridLayoutWidget)
        self.backwardToEndBtn.setObjectName(u"backwardToEndBtn")

        self.gridLayout_2.addWidget(self.backwardToEndBtn, 0, 0, 1, 1)

        self.forwardBtn = QPushButton(self.gridLayoutWidget)
        self.forwardBtn.setObjectName(u"forwardBtn")

        self.gridLayout_2.addWidget(self.forwardBtn, 0, 3, 1, 1)

        self.forwardToStartBtn = QPushButton(self.gridLayoutWidget)
        self.forwardToStartBtn.setObjectName(u"forwardToStartBtn")

        self.gridLayout_2.addWidget(self.forwardToStartBtn, 0, 4, 1, 1)

        self.playBtn = QPushButton(self.gridLayoutWidget)
        self.playBtn.setObjectName(u"playBtn")

        self.gridLayout_2.addWidget(self.playBtn, 0, 2, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_2, 1, 2, 1, 3)

        self.libraryWidget = QListWidget(self.gridLayoutWidget)
        self.libraryWidget.setObjectName(u"libraryWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.libraryWidget.sizePolicy().hasHeightForWidth())
        self.libraryWidget.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.libraryWidget, 0, 0, 2, 2)

        self.videoLabel = QLabel(self.gridLayoutWidget)
        self.videoLabel.setObjectName(u"videoLabel")

        self.gridLayout.addWidget(self.videoLabel, 3, 0, 1, 1)

        self.audioLabel = QLabel(self.gridLayoutWidget)
        self.audioLabel.setObjectName(u"audioLabel")

        self.gridLayout.addWidget(self.audioLabel, 4, 0, 1, 1)

        self.videoSlider = QSlider(self.gridLayoutWidget)
        self.videoSlider.setObjectName(u"videoSlider")
        self.videoSlider.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.videoSlider, 3, 1, 1, 4)

        self.audioSlider = QSlider(self.gridLayoutWidget)
        self.audioSlider.setObjectName(u"audioSlider")
        self.audioSlider.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.audioSlider, 4, 1, 1, 4)

        self.videoPreview = QLabel(self.gridLayoutWidget)
        self.videoPreview.setObjectName(u"videoPreview")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.videoPreview.sizePolicy().hasHeightForWidth())
        self.videoPreview.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.videoPreview, 0, 2, 1, 3)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.backwardBtn.setText(QCoreApplication.translate("Form", u"\u23ea", None))
        self.backwardToEndBtn.setText(QCoreApplication.translate("Form", u"\u23ee\ufe0f", None))
        self.forwardBtn.setText(QCoreApplication.translate("Form", u"\u23e9", None))
        self.forwardToStartBtn.setText(QCoreApplication.translate("Form", u"\u23ed\ufe0f", None))
        self.playBtn.setText(QCoreApplication.translate("Form", u"\u25b6\ufe0f", None))
        self.videoLabel.setText(QCoreApplication.translate("Form", u"Video 1", None))
        self.audioLabel.setText(QCoreApplication.translate("Form", u"Audio 1", None))
        self.videoPreview.setText(QCoreApplication.translate("Form", u"TextLabel", None))
    # retranslateUi

