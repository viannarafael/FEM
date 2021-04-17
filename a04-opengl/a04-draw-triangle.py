import sys
from PyQt5.QtWidgets import *
from OpenGL.GL import *
from PyQt5 import QtOpenGL

class MyCanvas(QtOpenGL.QGLWidget):

    def __init__(self):
        super(MyCanvas, self).__init__()
        self.setGeometry(100,100,600,400)
        self.setWindowTitle("MyGLDrawer")
        self.m_w = 0
        self.m_h = 0


    def initializeGL(self):
        #print("initializeGL")
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)


    def resizeGL(self,_width, _height):
        #print("resizeGl")
        #store GL canvas sizes in object properties
        self.m_w = _width
        self.m_h = _height
        #setup the viewport to canvas dimensions
        glViewport(0, 0, self.m_w, self.m_h)
        #reset the coordinate system
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        #estabilish the clipping volume by setting up an ortographic projection
        glOrtho(0.0, self.m_w, 0.0, self.m_h, -1.0, 1.0)
        #setup display in model coordinates
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()     

    def paintGL(self):
        #print("paintGL")
        #clear the buffer with the current collor
        glClear(GL_COLOR_BUFFER_BIT)
        #draw a triangle with RGB color at the 3 vertices
        #interpolating smoothly the color in the interior
        xA = self.m_w / 3.0
        yA = self.m_h / 3.0
        xB = self.m_w * (2.0 / 3.0)
        yB = self.m_h / 3.0
        xC = self.m_w / 2.0
        yC = self.m_h * (2.0 / 3.0)
        glBegin(GL_TRIANGLES)
        glColor3f(1.0, 0.0, 0.0)
        glVertex2f(xA,yA)
        glColor3f(0.0, 1.0, 0.0)
        glVertex2f(xB,yB)
        glColor3f(0.0, 0.0, 1.0)
        glVertex2f(xC,yC)
        glEnd()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyCanvas()
    widget.show()
    sys.exit(app.exec_())
