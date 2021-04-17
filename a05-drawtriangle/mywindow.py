from PyQt5.QtWidgets import *
from mycanvas import *
from mymodel import *

class MyWindow(QMainWindow):

    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(100,100,500,400)
        self.setWindowTitle("MyGLdrawer")
        self.canvas = MyCanvas()
        self.setCentralWidget(self.canvas)
        #create a model object and pass to canvas
        self.model = MyModel()
        self.canvas.setModel(self.model)
