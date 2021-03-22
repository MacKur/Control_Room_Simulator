import sys
import random

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5 import QtCore, QtGui, QtWidgets


class LiniaProdukcyjna(QWidget):
    def __init__(self):
        super().__init__()
        self.wartosc_CPU = 0
        self.maks_wentylatorow = 10
        self.start = True
        self.tempUp = 45
        self.tempDown = 15
        self.ilosc_wentylatorow = 0
        self.moc_wentylatorow = 0
        self.temperatura = 0
        self.nie_zmieniaj_went = False
        self.licznik_zmian_went = 0
        self.userON = 0
        self.initUI()

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.repaint()
        else:
            super.timerEvent(event)

    def tempLCD(self):
        temp = random.uniform(8.5, 9)
        if self.wartosc_CPU == 0:
            self.temperatura = 0
        else:
            self.temperatura = temp * self.wartosc_CPU / 4 - self.ilosc_wentylatorow * 10
            if self.temperatura < 3:
                self.temperatura = random.randint(3, 8)

        roznica_temp = self.tempUp - self.temperatura
        if roznica_temp != 0:
            if self.ilosc_wentylatorow != 0:
                if roznica_temp > 30:
                    self.moc_wentylatorow = random.randint(5, 20)
                elif 30 > roznica_temp > 10:
                    self.moc_wentylatorow = random.randint(20, 30)
                elif 10 > roznica_temp > 0:
                    self.moc_wentylatorow = random.randint(30, 50)
                elif 0 > roznica_temp > -15:
                    self.moc_wentylatorow = random.randint(30, 50)
                elif -15 > roznica_temp > -30:
                    self.moc_wentylatorow = random.randint(50, 75)
                elif -30 > roznica_temp > -40:
                    self.moc_wentylatorow = random.randint(75, 85)
                    komunikat = self.okno_komunikatow.toPlainText() + "UWAGA: Duże użycie wentylatorów! \n"
                    self.okno_komunikatow.setPlainText(komunikat)
                elif roznica_temp < -40:
                    self.moc_wentylatorow = random.randint(90, 100)
                    komunikat = self.okno_komunikatow.toPlainText() + "UWAGA: Wentylatory pracują na maksymalnych " \
                                                                      "obrotach! \n "
                    self.okno_komunikatow.setPlainText(komunikat)
            else:
                self.moc_wentylatorow = 0

        self.tempC.display(self.temperatura)
        self.wykorzystanie_went.setValue(self.moc_wentylatorow)

    def praca_wentylatorow(self):
        if (
                self.temperatura > self.tempUp and self.ilosc_wentylatorow < self.maks_wentylatorow and self.nie_zmieniaj_went == False):
            self.ilosc_wentylatorow = self.ilosc_wentylatorow + 1
            komunikat = self.okno_komunikatow.toPlainText() + "Uruchamianie dodatkowego wentylatora \n"
            self.okno_komunikatow.setPlainText(komunikat)
        elif self.temperatura < self.tempDown and self.ilosc_wentylatorow > 0 and self.nie_zmieniaj_went == False:
            self.ilosc_wentylatorow = self.ilosc_wentylatorow - 1
            komunikat = self.okno_komunikatow.toPlainText() + "Wyłączanie jednego wentylatora \n"
            self.okno_komunikatow.setPlainText(komunikat)

        self.ilosc_went_aktyw.display(self.ilosc_wentylatorow)

    def wlacz_CPU(self):
        if self.wartosc_CPU < 25:
            self.wartosc_CPU = self.wartosc_CPU + 2
            self.wykorzystanie_CPU.setValue(self.wartosc_CPU)

        else:
            rand = random.randint(-2, 2)
            temp = self.wartosc_CPU + rand
            self.wartosc_CPU = temp
            self.wykorzystanie_CPU.setValue(self.wartosc_CPU)
            self.timerTurnOn.stop()

    def onUser(self):
        if self.start:
            self.start = False
            content = self.okno_komunikatow.toPlainText() + "Uruchomienie linii produkcyjnej \n"
            self.okno_komunikatow.setPlainText(content)
            self.timerTurnOn = QtCore.QTimer()
            self.timerTurnOn.start(200)
            self.timerTurnOn.timeout.connect(self.wlacz_CPU)
            self.timerTurnOnLCD = QtCore.QTimer()
            self.timerTurnOnLCD.start(2000)
            self.timerTurnOnLCD.timeout.connect(self.tempLCD)
            self.timerTurnOnFans = QtCore.QTimer()
            self.timerTurnOnFans.start(2000)
            self.timerTurnOnFans.timeout.connect(self.praca_wentylatorow)
            self.checkUser = QtCore.QTimer()
            self.checkUser.start(100)
            self.checkUser.timeout.connect(self.userCheck)
        elif not self.start:
            self.nie_zmieniaj_went = False
            self.licznik_zmian_went = 0
            content = self.okno_komunikatow.toPlainText() + "Uwaga: Powrót do trybu automatycznego \n"
            self.okno_komunikatow.setPlainText(content)

    def wlacz_wentylator(self):
        if not self.start:
            self.licznik_zmian_went = 0
            self.ilosc_wentylatorow = self.ilosc_wentylatorow + 1
            if not self.nie_zmieniaj_went:
                content = self.okno_komunikatow.toPlainText() + "Uwaga: Przejscie do trybu manualnego. Aby wrócic do " \
                                                                "trybu auto proszę nacisnąć przycisk |OK| \n " \
                                                                "Uruchamianie dod. wentylatora "
                self.okno_komunikatow.setPlainText(content)
                self.nie_zmieniaj_went = True
            else:
                content = self.okno_komunikatow.toPlainText() + " Uruchamianie dodatkowego wentylatora\n"
                self.okno_komunikatow.setPlainText(content)

    def wylacz_wentylator(self):
        if self.ilosc_wentylatorow > 0 and self.start == False:
            self.ilosc_wentylatorow = self.ilosc_wentylatorow - 1
            self.licznik_zmian_went = self.licznik_zmian_went + 1
            if not self.nie_zmieniaj_went:
                content = self.okno_komunikatow.toPlainText() + "Uwaga: Przejście do trybu manualnego. Aby wrócić do " \
                                                                "trybu auto proszę nacisnąć przycisk |OK| \n " \
                                                                "Wyłączanie wentylatora "
                self.okno_komunikatow.setPlainText(content)
                self.nie_zmieniaj_went = True
            else:
                content = self.okno_komunikatow.toPlainText() + " Wyłączanie wentylatora\n"
                self.okno_komunikatow.setPlainText(content)

    def mniej_pracy_went(self):
        if not self.start:
            self.poprzednia_wartosc_CPU = self.wartosc_CPU
            self.t_mniej_pracy = QtCore.QTimer()
            self.t_mniej_pracy.start(200)
            self.t_mniej_pracy.timeout.connect(self.mniej_pracy_zmiana)

    def wiecej_pracy_went(self):
        if not self.start:
            self.poprzednia_wartosc_CPU = self.wartosc_CPU
            self.t_wiecej_pracy = QtCore.QTimer()
            self.t_wiecej_pracy.start(200)
            self.t_wiecej_pracy.timeout.connect(self.wiecej_pracy_zmiana)

    def wiecej_pracy_zmiana(self):
        randomDif = random.randint(12, 17)
        if abs(self.wartosc_CPU - self.poprzednia_wartosc_CPU) < randomDif and self.wartosc_CPU < 90:
            self.wartosc_CPU = self.wartosc_CPU + random.randint(0, 3)
            self.wykorzystanie_CPU.setValue(self.wartosc_CPU)
        elif self.wartosc_CPU >= 90:
            self.wartosc_CPU = random.randint(90, 95)
            self.t_wiecej_pracy.stop()
        else:
            self.t_wiecej_pracy.stop()

    def mniej_pracy_zmiana(self):
        randomDif = random.randint(12, 17)
        if abs(self.wartosc_CPU - self.poprzednia_wartosc_CPU) < randomDif and self.wartosc_CPU > 5:
            self.wartosc_CPU = self.wartosc_CPU - random.randint(0, 3)
            self.wykorzystanie_CPU.setValue(self.wartosc_CPU)
        elif self.wartosc_CPU <= 5:
            self.wartosc_CPU = random.randint(3, 5)
            self.t_mniej_pracy.stop()
        else:
            self.t_mniej_pracy.stop()

    def userCheck(self):
        self.userON = self.userON + 1
        if self.userON == 60:
            content = self.okno_komunikatow.toPlainText() + "Prosze potwierdzić obecność przyciskiem [obecny] \n "
            self.okno_komunikatow.setPlainText(content)
        elif self.userON == 120:
            content = self.okno_komunikatow.toPlainText() + "ERROR \nBrak obecności uzytkownika, " \
                                                    "linia produkcyjna zostaje wylaczona\n "
            self.okno_komunikatow.setPlainText(content)
            self.start = True
            self.wartosc_CPU = 0
            self.wykorzystanie_CPU.setValue(self.wartosc_CPU)

    def uzytkownik_obecny(self):
        self.userON = 0
        content = self.okno_komunikatow.toPlainText() + "-----------------------\nUżytkownik " \
                                                        "obecny\n-----------------------\n "
        self.okno_komunikatow.setPlainText(content)

    def initUI(self):
        self.setGeometry(100, 100, 653, 559)
        self.setWindowTitle('ASK ZAD 6')
        self.setStyleSheet("#ok{\n" "background:green;\n" "}\n" "#off{\n" "background:red;\n" "}")
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.wykorzystanie_CPU = QtWidgets.QProgressBar(self)
        self.wykorzystanie_CPU.setGeometry(QtCore.QRect(190, 60, 91, 23))
        self.wykorzystanie_CPU.setProperty("value", 24)
        self.wykorzystanie_CPU.setTextVisible(True)
        self.wykorzystanie_CPU.setObjectName("wykorzystanie_CPU")
        self.wykorzystanie_CPU_label = QtWidgets.QLabel(self)
        self.wykorzystanie_CPU_label.setGeometry(QtCore.QRect(20, 60, 151, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.wykorzystanie_CPU_label.setFont(font)
        self.wykorzystanie_CPU_label.setObjectName("wykorzystanie_CPU_label")
        self.tempC_label = QtWidgets.QLabel(self)
        self.tempC_label.setGeometry(QtCore.QRect(20, 20, 161, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tempC_label.setFont(font)
        self.tempC_label.setObjectName("tempC_label")
        self.tempC = QtWidgets.QLCDNumber(self)
        self.tempC.setGeometry(QtCore.QRect(190, 20, 81, 23))
        self.tempC.setStyleSheet("font: 12pt \"MS Shell Dlg 2\" rgb(0, 0, 0);")
        self.tempC.setObjectName("tempC")
        self.on = QtWidgets.QPushButton(self)
        self.on.setGeometry(QtCore.QRect(50, 430, 221, 121))
        palette = QtGui.QPalette()
        gradient = QtGui.QRadialGradient(0.5, 0.5, 0.5, 0.5, 0.5)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.00568182, QtGui.QColor(32, 255, 73))
        gradient.setColorAt(0.744318, QtGui.QColor(50, 203, 0))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        gradient = QtGui.QRadialGradient(0.5, 0.5, 0.5, 0.5, 0.5)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.00568182, QtGui.QColor(32, 255, 73))
        gradient.setColorAt(0.744318, QtGui.QColor(50, 203, 0))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        gradient = QtGui.QRadialGradient(0.5, 0.5, 0.5, 0.5, 0.5)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.00568182, QtGui.QColor(32, 255, 73))
        gradient.setColorAt(0.744318, QtGui.QColor(50, 203, 0))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        gradient = QtGui.QRadialGradient(0.5, 0.5, 0.5, 0.5, 0.5)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.00568182, QtGui.QColor(32, 255, 73))
        gradient.setColorAt(0.744318, QtGui.QColor(50, 203, 0))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        gradient = QtGui.QRadialGradient(0.5, 0.5, 0.5, 0.5, 0.5)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.00568182, QtGui.QColor(32, 255, 73))
        gradient.setColorAt(0.744318, QtGui.QColor(50, 203, 0))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        gradient = QtGui.QRadialGradient(0.5, 0.5, 0.5, 0.5, 0.5)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.00568182, QtGui.QColor(32, 255, 73))
        gradient.setColorAt(0.744318, QtGui.QColor(50, 203, 0))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        gradient = QtGui.QRadialGradient(0.5, 0.5, 0.5, 0.5, 0.5)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.00568182, QtGui.QColor(32, 255, 73))
        gradient.setColorAt(0.744318, QtGui.QColor(50, 203, 0))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        gradient = QtGui.QRadialGradient(0.5, 0.5, 0.5, 0.5, 0.5)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.00568182, QtGui.QColor(32, 255, 73))
        gradient.setColorAt(0.744318, QtGui.QColor(50, 203, 0))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        gradient = QtGui.QRadialGradient(0.5, 0.5, 0.5, 0.5, 0.5)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.00568182, QtGui.QColor(32, 255, 73))
        gradient.setColorAt(0.744318, QtGui.QColor(50, 203, 0))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.on.setPalette(palette)
        self.on.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, "
                              "fy:0.5, stop:0.00568182 rgba(32, 255, 73, 255), stop:0.744318 rgba(50, 203, 0, 255))")
        self.on.setObjectName("on")
        self.up = QtWidgets.QPushButton(self)
        self.up.setGeometry(QtCore.QRect(380, 430, 221, 121))
        self.up.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, "
                               "fy:0.5, stop:0 rgba(255, 0, 0, 255), stop:1 rgba(196, 0, 0, 255))")
        self.up.setAutoDefault(True)
        self.up.setObjectName("up")
        self.went_label = QtWidgets.QLabel(self)
        self.went_label.setGeometry(QtCore.QRect(320, 60, 191, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.went_label.setFont(font)
        self.went_label.setObjectName("went_label")
        self.wykorzystanie_went = QtWidgets.QProgressBar(self)
        self.wykorzystanie_went.setGeometry(QtCore.QRect(520, 60, 91, 23))
        self.wykorzystanie_went.setProperty("value", 24)
        self.wykorzystanie_went.setObjectName("wykorzystanie_went")

        self.wlacz_went = QtWidgets.QPushButton(self)
        self.wlacz_went.setGeometry(QtCore.QRect(30, 110, 271, 51))
        self.wlacz_went.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, "
                                          "radius:1.56, fx:0.5, fy:0.494318, stop:0.210227 rgba(198, 198, 198, "
                                          "255), stop:0.602273 rgba(100, 100, 100, 255))")
        self.wlacz_went.setObjectName("wlacz_went")
        self.ilosc_went_aktyw = QtWidgets.QLCDNumber(self)
        self.ilosc_went_aktyw.setGeometry(QtCore.QRect(520, 20, 81, 23))
        self.ilosc_went_aktyw.setStyleSheet("font: 12pt \"MS Shell Dlg 2\" rgb(0, 0, 0);")
        self.ilosc_went_aktyw.setObjectName("ilosc_went_aktyw")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(320, 20, 191, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.wylacz_went = QtWidgets.QPushButton(self)
        self.wylacz_went.setGeometry(QtCore.QRect(30, 180, 271, 51))
        self.wylacz_went.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.56, "
                                      "fx:0.5, fy:0.494318, stop:0.210227 rgba(198, 198, 198, 255), stop:0.602273 "
                                      "rgba(100, 100, 100, 255))")
        self.wylacz_went.setObjectName("wylacz_went")
        self.okno_komunikatow = QtWidgets.QTextEdit(self)
        self.okno_komunikatow.setGeometry(QtCore.QRect(130, 260, 371, 141))
        self.okno_komunikatow.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.okno_komunikatow.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.okno_komunikatow.setOverwriteMode(True)
        self.okno_komunikatow.setObjectName("okno_komunikatow")
        self.wiecej_pracy = QtWidgets.QPushButton(self)
        self.wiecej_pracy.setGeometry(QtCore.QRect(350, 110, 271, 51))
        self.wiecej_pracy.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.56, "
                                    "fx:0.5, fy:0.494318, stop:0.210227 rgba(198, 198, 198, 255), stop:0.602273 rgba("
                                    "100, 100, 100, 255))")
        self.wiecej_pracy.setObjectName("wiecej_pracy")
        self.mniej_pracy = QtWidgets.QPushButton(self)
        self.mniej_pracy.setGeometry(QtCore.QRect(350, 180, 271, 51))
        self.mniej_pracy.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.56, "
                                    "fx:0.5, fy:0.494318, stop:0.210227 rgba(198, 198, 198, 255), stop:0.602273 rgba("
                                    "100, 100, 100, 255))")
        self.mniej_pracy.setObjectName("mniej_pracy")

        self.on.clicked.connect(self.onUser)
        self.wlacz_went.clicked.connect(self.wlacz_wentylator)
        self.wylacz_went.clicked.connect(self.wylacz_wentylator)
        self.wiecej_pracy.clicked.connect(self.wiecej_pracy_went)
        self.mniej_pracy.clicked.connect(self.mniej_pracy_went)
        self.up.clicked.connect(self.uzytkownik_obecny)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.show()

    def retranslateUi(self, _):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "Symulator stanowiska dyspozytorskiego linii produkcyjnej"))
        self.wykorzystanie_CPU_label.setText(_translate("self", "Wykorzystanie procesora"))
        self.tempC_label.setText(_translate("self", "Temperatura procesora [C]"))
        self.on.setText(_translate("self", "ON"))
        self.up.setText(_translate("self", "Obecny"))
        self.went_label.setText(_translate("self", "Prędkość obrotowa wentylatorów"))
        self.wlacz_went.setText(_translate("self", "Włącz dodatkowy wentylator"))
        self.label.setText(_translate("self", "Ilość działających wentylatorów"))
        self.wylacz_went.setText(_translate("self", "Wyłącz jeden wentylator"))
        self.wiecej_pracy.setText(_translate("self", "Przyspiesz pracę"))
        self.mniej_pracy.setText(_translate("self", "Zwolnij pracę"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = LiniaProdukcyjna()
    sys.exit(app.exec_())
