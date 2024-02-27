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
    QSizePolicy, QWidget)

class Ui_Track(object):
    def setupUi(self, Track):
        if not Track.objectName():
            Track.setObjectName(u"Track")
        Track.resize(939, 84)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Track.sizePolicy().hasHeightForWidth())
        Track.setSizePolicy(sizePolicy)
        Track.setMinimumSize(QSize(10, 50))
        self.horizontalLayout_2 = QHBoxLayout(Track)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.TrackWrapper = QHBoxLayout()
        self.TrackWrapper.setObjectName(u"TrackWrapper")
        self.TrackLabel = QLabel(Track)
        self.TrackLabel.setObjectName(u"TrackLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.TrackLabel.sizePolicy().hasHeightForWidth())
        self.TrackLabel.setSizePolicy(sizePolicy1)

        self.TrackWrapper.addWidget(self.TrackLabel)

        self.NameSeparator = QFrame(Track)
        self.NameSeparator.setObjectName(u"NameSeparator")
        self.NameSeparator.setStyleSheet(u"")
        self.NameSeparator.setFrameShadow(QFrame.Plain)
        self.NameSeparator.setFrameShape(QFrame.VLine)

        self.TrackWrapper.addWidget(self.NameSeparator)

        self.TrackElemntContainer = QHBoxLayout()
        self.TrackElemntContainer.setObjectName(u"TrackElemntContainer")

        self.TrackWrapper.addLayout(self.TrackElemntContainer)


        self.horizontalLayout_2.addLayout(self.TrackWrapper)


        self.retranslateUi(Track)

        QMetaObject.connectSlotsByName(Track)
    # setupUi

    def retranslateUi(self, Track):
        Track.setWindowTitle(QCoreApplication.translate("Track", u"Timeline", None))
        self.TrackLabel.setText(QCoreApplication.translate("Track", u"TextLabel", None))
    # retranslateUi

