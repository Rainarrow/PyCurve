#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math
import numpy as np

from PyQt4 import QtGui, QtCore


def binomial(i, n):
    """Binomial coefficient"""
    return math.factorial(n) / float(
        math.factorial(i) * math.factorial(n - i))


def bernstein(t, i, n):
    """Bernstein polynom"""
    return binomial(i, n) * (t ** i) * ((1 - t) ** (n - i))


def bezier(t, points):
    """Calculate coordinate of a point in the bezier curve"""
    n = len(points) - 1
    x = y = 0
    for i, pos in enumerate(points):
        bern = bernstein(t, i, n)
        x += pos[0] * bern
        y += pos[1] * bern
    return x, y


def bezier_curve_range(n, points):
    """Range of points in a curve bezier"""
    for i in range(n):
        t = i / float(n - 1)
        yield bezier(t, points)


class BezierDrawer(QtGui.QWidget):
    """Draw a Bezier Curve"""
  
    def __init__(self):
        super(BezierDrawer, self).__init__()

        self.button = QtGui.QPushButton('Clear', self)
        self.button.clicked.connect(self.handleClearView)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.button)

        self.setGeometry(300, 300, 450, 450)
        self.setWindowTitle('Bezier Curves')
        self.coordList = []

    def handleClearView(self):
        self.view.scene.clear()
        self.coordList.clear()

    def paintEvent(self, e):
      
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHints(QtGui.QPainter.Antialiasing, True)
        self.doDrawing(qp)        
        qp.end()

    def mousePressEvent(self, event):

        self.coordList.append(event.pos())

    def doDrawing(self, qp):

        blackPen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.DashLine)
        redPen = QtGui.QPen(QtCore.Qt.red, 1, QtCore.Qt.DashLine)
        bluePen = QtGui.QPen(QtCore.Qt.blue, 1, QtCore.Qt.DashLine)
        greenPen = QtGui.QPen(QtCore.Qt.green, 1, QtCore.Qt.DashLine)
        redBrush = QtGui.QBrush(QtCore.Qt.red)

        steps = 1000
        controlPoints = (
                (50, 170),
                (150, 370),
                (250, 35),
                (400, 320))

        oldPoint = controlPoints[0]

        qp.setPen(redPen)
        qp.setBrush(redBrush)
        qp.drawEllipse(oldPoint[0] - 3, oldPoint[1] - 3, 6, 6)

        qp.drawText(oldPoint[0] + 5, oldPoint[1] - 3, '1')
        for i, point in enumerate(controlPoints[1:]):
            i += 2
            qp.setPen(blackPen)
            qp.drawLine(oldPoint[0], oldPoint[1], point[0], point[1])
            
            qp.setPen(redPen)
            qp.drawEllipse(point[0] - 3, point[1] - 3, 6, 6)

            qp.drawText(point[0] + 5, point[1] - 3, '%d' % i)
            oldPoint = point
            
        qp.setPen(bluePen)
        for point in bezier_curve_range(steps, controlPoints):
            qp.drawLine(oldPoint[0], oldPoint[1], point[0], point[1])
            oldPoint = point

def inputpoints():
	
	global controlPoints
	print("nr of points")
	nr = int(input())
	controlPoints = np.zeros((nr, 2), int)

	for i in range(nr):
		controlPoints[i][0] = int(input())
		controlPoints[i][1] = int(input())

def main(args):
    app = QtGui.QApplication(sys.argv)
    ex = BezierDrawer()
    ex.show()
    app.exec_()


if __name__=='__main__':
    #inputpoints()
    main(sys.argv[1:])


