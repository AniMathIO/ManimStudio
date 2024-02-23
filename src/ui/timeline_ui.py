# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'timeline.ui'
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
from PySide6.QtWidgets import (QApplication, QSizePolicy, QVBoxLayout, QWidget)

class Ui_TimelineContainer(object):
    def setupUi(self, TimelineContainer):
        if not TimelineContainer.objectName():
            TimelineContainer.setObjectName(u"TimelineContainer")
        TimelineContainer.resize(921, 364)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TimelineContainer.sizePolicy().hasHeightForWidth())
        TimelineContainer.setSizePolicy(sizePolicy)
        self.TimelineVerticalLayoutMain = QVBoxLayout(TimelineContainer)
        self.TimelineVerticalLayoutMain.setObjectName(u"TimelineVerticalLayoutMain")

        self.retranslateUi(TimelineContainer)

        QMetaObject.connectSlotsByName(TimelineContainer)
    # setupUi

    def retranslateUi(self, TimelineContainer):
        TimelineContainer.setWindowTitle(QCoreApplication.translate("TimelineContainer", u"Timeline", None))
    # retranslateUi

