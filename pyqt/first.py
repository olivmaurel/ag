import sys, os
from PyQt5.QtWidgets import (QMainWindow, QMessageBox,
                             QPushButton, QGridLayout, QApplication, QDesktopWidget)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import Qt as qtcore

LOCALPATH = os.path.dirname(os.path.abspath(__file__))


class Entity(object):
    pass

class Character(Entity):

    def __init__(self, name):
        super().__init__()
        self.hunger = 0
        self.actionPoints = 0
        self.name = name




class Game(QMainWindow):
    def __init__(self):
        super().__init__()
        self.turn = 0

        self.initUI()

    def initUI(self):

        # Window config
        self.statusBar()
        self.resize(1024, 768)
        self.setWindowFlag(qtcore.FramelessWindowHint)
        self.center()

        # Icon
        self.setWindowIcon(QIcon(os.path.join(LOCALPATH, 'images/icon.png')))

        newchar = Character('Albonpin')
        charbtn = QPushButton(newchar.name)
        charbtn.move(50, 0)
        nxtbtn = QPushButton('Next turn', self)
        nxtbtn.move(50, 50)
        nxtbtn.clicked.connect(lambda: self.nextTurn(newchar))

        eatbtn = QPushButton('Eat something', self)
        eatbtn.move(50, 75)
        eatbtn.clicked.connect(lambda: self.eatAction(newchar))

        qbtn = QPushButton('Quit', self)
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.move(50, 125)


        self.show()

    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was pressed')

    def nextTurn(self, char):

        char.hunger += 1
        if char.hunger > 10:
            self.statusBar().showMessage('You\'re dead')
        else:
            char.actionPoints += 1
            self.turn += 1
            self.statusBar().showMessage('Turn {}:| Hunger:{}'.format(self.turn, char.hunger))

    def eatAction(self, char):
        if char.actionPoints > 0:
            char.hunger -= 5
            self.statusBar().showMessage('Yummy! | Hunger:{}'.format(self.turn, char.hunger))
            char.actionPoints = 0
        else:
            self.statusBar().showMessage('Can\'t eat, no action points left, click on next turn')

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    sys.exit(app.exec_())