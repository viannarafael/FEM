import sys
from PyQt5.QtWidgets import *

class MyWidget(QWidget):

    def __init__(self):
        super(MyWidget, self).__init__()
        self.setGeometry(100,100,200,50)
        self.setWindowTitle("Ex1")
        self.r1 = QLabel("a = ")
        self.r2 = QLabel("b = ")
        self.r3 = QLabel("a + b = ")
        self.t1 = QLineEdit()
        self.t2 = QLineEdit()
        self.t3 = QLineEdit()
        self.b1 = QPushButton("Calculate")
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.r1)
        self.vbox.addWidget(self.t1)
        self.vbox.addWidget(self.r2)
        self.vbox.addWidget(self.t2)
        self.vbox.addWidget(self.b1)
        self.vbox.addWidget(self.r3)
        self.vbox.addWidget(self.t3)
        self.setLayout(self.vbox)
        # Connecting the signal
        self.b1.clicked.connect(self.magic)

    # @Slot()
    def magic(self):
        print("Button clicked")
        a=float(self.t1.text())
        b=float(self.t2.text())
        self.t3.setText(str(a+b))
    def keyPressEvent(self,e):
        if e.key() == QT.Key_Escape:
            self.close()
        
                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())
