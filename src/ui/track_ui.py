# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'track.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_TrackContainer(object):
    def setupUi(self, TrackContainer):
        if not TrackContainer.objectName():
            TrackContainer.setObjectName(u"TrackContainer")
        TrackContainer.resize(939, 84)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TrackContainer.sizePolicy().hasHeightForWidth())
        TrackContainer.setSizePolicy(sizePolicy)
        TrackContainer.setMinimumSize(QSize(10, 50))
        self.horizontalLayout_2 = QHBoxLayout(TrackContainer)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.TrackHorizontalLayout = QHBoxLayout()
        self.TrackHorizontalLayout.setObjectName(u"TrackHorizontalLayout")
        self.TrackName = QLabel(TrackContainer)
        self.TrackName.setObjectName(u"TrackName")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.TrackName.sizePolicy().hasHeightForWidth())
        self.TrackName.setSizePolicy(sizePolicy1)

        self.TrackHorizontalLayout.addWidget(self.TrackName)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.TrackHorizontalLayout.addLayout(self.verticalLayout)

        self.NameSeparator = QFrame(TrackContainer)
        self.NameSeparator.setObjectName(u"NameSeparator")
        self.NameSeparator.setStyleSheet(u"")
        self.NameSeparator.setFrameShadow(QFrame.Plain)
        self.NameSeparator.setFrameShape(QFrame.VLine)

        self.TrackHorizontalLayout.addWidget(self.NameSeparator)


        self.horizontalLayout_2.addLayout(self.TrackHorizontalLayout)


        self.retranslateUi(TrackContainer)

        QMetaObject.connectSlotsByName(TrackContainer)
    # setupUi

    def retranslateUi(self, TrackContainer):
        TrackContainer.setWindowTitle(QCoreApplication.translate("TrackContainer", u"Timeline", None))
        self.TrackName.setText(QCoreApplication.translate("TrackContainer", u"TextLabel", None))
    # retranslateUi

