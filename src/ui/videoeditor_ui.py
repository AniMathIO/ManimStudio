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
    QSlider, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(790, 517)
        self.gridLayout_3 = QGridLayout(Form)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.videoPreview = QLabel(Form)
        self.videoPreview.setObjectName(u"videoPreview")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.videoPreview.sizePolicy().hasHeightForWidth())
        self.videoPreview.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.videoPreview, 0, 2, 1, 2)

        self.timelineLabel = QLabel(Form)
        self.timelineLabel.setObjectName(u"timelineLabel")

        self.gridLayout.addWidget(self.timelineLabel, 2, 0, 1, 1)

        self.libraryWidget = QListWidget(Form)
        self.libraryWidget.setObjectName(u"libraryWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.libraryWidget.sizePolicy().hasHeightForWidth())
        self.libraryWidget.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.libraryWidget, 0, 0, 2, 2)

        self.timelineSlider = QSlider(Form)
        self.timelineSlider.setObjectName(u"timelineSlider")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.timelineSlider.sizePolicy().hasHeightForWidth())
        self.timelineSlider.setSizePolicy(sizePolicy2)
        self.timelineSlider.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.timelineSlider, 2, 1, 1, 3)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.forwardToStartBtn = QPushButton(Form)
        self.forwardToStartBtn.setObjectName(u"forwardToStartBtn")

        self.gridLayout_2.addWidget(self.forwardToStartBtn, 1, 4, 1, 1)

        self.backwardBtn = QPushButton(Form)
        self.backwardBtn.setObjectName(u"backwardBtn")

        self.gridLayout_2.addWidget(self.backwardBtn, 1, 1, 1, 1)

        self.playBtn = QPushButton(Form)
        self.playBtn.setObjectName(u"playBtn")

        self.gridLayout_2.addWidget(self.playBtn, 1, 2, 1, 1)

        self.backwardToEndBtn = QPushButton(Form)
        self.backwardToEndBtn.setObjectName(u"backwardToEndBtn")

        self.gridLayout_2.addWidget(self.backwardToEndBtn, 1, 0, 1, 1)

        self.forwardBtn = QPushButton(Form)
        self.forwardBtn.setObjectName(u"forwardBtn")

        self.gridLayout_2.addWidget(self.forwardBtn, 1, 3, 1, 1)

        self.videoPreviewSlider = QSlider(Form)
        self.videoPreviewSlider.setObjectName(u"videoPreviewSlider")
        self.videoPreviewSlider.setOrientation(Qt.Horizontal)

        self.gridLayout_2.addWidget(self.videoPreviewSlider, 0, 0, 1, 5)


        self.gridLayout.addLayout(self.gridLayout_2, 1, 2, 1, 2)

        self.timelineVerticalLayout = QVBoxLayout()
        self.timelineVerticalLayout.setObjectName(u"timelineVerticalLayout")
        self.timelineVerticalLayout.setSizeConstraint(QLayout.SetMaximumSize)

        self.gridLayout.addLayout(self.timelineVerticalLayout, 3, 0, 1, 4)


        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.videoPreview.setText(QCoreApplication.translate("Form", u"VideoPreview", None))
        self.timelineLabel.setText(QCoreApplication.translate("Form", u"Timeline", None))
        self.forwardToStartBtn.setText(QCoreApplication.translate("Form", u"\u23ed\ufe0f", None))
        self.backwardBtn.setText(QCoreApplication.translate("Form", u"\u23ea", None))
        self.playBtn.setText(QCoreApplication.translate("Form", u"\u25b6\ufe0f", None))
        self.backwardToEndBtn.setText(QCoreApplication.translate("Form", u"\u23ee\ufe0f", None))
        self.forwardBtn.setText(QCoreApplication.translate("Form", u"\u23e9", None))
    # retranslateUi

