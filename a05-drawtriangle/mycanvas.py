import sys
from PyQt5 import QtOpenGL
from PyQt5.QtWidgets import *
from OpenGL.GL import *

class MyCanvas(QtOpenGL.QGLWidget):

    def __init__(self):
        super(MyCanvas, self).__init__()
        self.m_model = None
        
        self.m_w = 0
        self.m_h = 0

    def initializeGL(self):
        #print("initializeGL")
        #glClearColor(1.0, 1.0, 1.0, 1.0)
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
        if (self.m_model==None)or(self.m_model.isEmpty()):
            return
        #Display model polygon RGB color at its vertices
        verts = self.m_model.getVerts()
        glShadeModel(GL_SMOOTH)
        glColor3f(0.0,1.0,0.0)
        glBegin (GL_TRIANGLES)
        for vtx in verts:
            glVertex2f(vtx.getX(), vtx.getY())
        glEnd()
        
    def setModel(self,_model):
           self.m_model = _model
