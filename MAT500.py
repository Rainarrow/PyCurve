from tkinter import *
from copy import deepcopy
import sys, math

CONST_POINT_SIZE = 5
CONST_ITER_STEPS = 1024

class Point():

    def __init__(self, X = 0, Y = 0):
        self.x = X
        self.y = Y

    def prnt(self):
        print("X: ", self.x, " Y: ", self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

def calcMidPoint(points):#Accepts list of Points, returns list of Points
    if(len(points) >= 2):
        result = []
        for i in range(0, len(points) - 1):
            x = 0.5 * points[i].x + 0.5 * points[i + 1].x
            y = 0.5 * points[i].y + 0.5 * points[i + 1].y
            result.append(Point(x, y))
    return result

def binomialCof(i, n):
    return math.factorial(n) / float(math.factorial(i) * math.factorial(n - i))

def bernstein(t, i, n):
    return binomialCof(i, n) * (t ** i) * ((1 - t) ** (n - i))

def bezier(points, t):
    n = len(points) - 1
    result = Point()

    for i, pt in enumerate(points):
        b = bernstein(t, i, n)
        result.x += pt.x * b
        result.y += pt.y * b

    return result

def bezierGenerator(points, n):
    for i in range(n):
        t = i / float(n - 1)
        yield bezier(points, t)

class Ilan(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, background = "white")

        self.algList = ("De Casteljau", "De Casteljau(Recursive)", "Bernstein")#, "Midpt Subdiv")
        self.parent = parent
        self.ctrlPoints = []
        self.plotPoints = [] #The actual curve goes here
        self.curAlg = StringVar()
        self.curAlg.set(self.algList[0])
        self.dragPtIndex = 128
        self.shouldDrawShell = IntVar()

        self.initUI()

        self.dragData = {"x": 0, "y": 0, "item": None}

    def initUI(self):

        self.parent.title("MAT500")

        menubar = Menu(self.parent)
        self.parent.config(menu = menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label = "Exit", command = self.onExit)
        menubar.add_cascade(label = "File", menu = fileMenu)


        self.toolbar = Frame(self.parent, height = 20, bd = 1, relief = RAISED)

        self.algMenu = OptionMenu(self.toolbar, self.curAlg, *self.algList, command = self.drawCurve)
        self.algMenu.pack(side = "left")

        self.clearBtn = Button(self.toolbar, text = "clear", command = self.clearAll)
        self.clearBtn.pack(side = "left")
        self.tScale = Scale(self.toolbar, orient = HORIZONTAL, from_ = 0.0, to = 1.0, resolution = 0.01, command = self.updateShellOnTScaleChange)
        self.tScale.set(0.5)
        self.tScale.pack(side = "left")
        
        self.ctrlPtNum = StringVar()
        self.ctrlPtNum.set("0") 
        self.ctrlPtNumLabel = Label(self.toolbar, textvariable = self.ctrlPtNum)
        self.ctrlPtNumLabel.pack(side = "left")

        self.shellCheckBox = Checkbutton(self.toolbar, text = "Draw Shell", variable = self.shouldDrawShell, command = self.drawCurve)
        self.shellCheckBox.pack(side = "left")

        self.toolbar.pack(side = "top", fill = X)

        self.canvas = Canvas(self)
        self.canvas.pack(fill = BOTH, expand = 1)
        #self.canvas.bind("<ButtonPress-2>", self.onCMB)
        self.canvas.bind("<ButtonPress-2>", self.testMidSubDiv)
        self.canvas.bind("<ButtonPress-3>", self.addInputPt)
        self.canvas.tag_bind("ctrlPts", "<ButtonPress-1>", self.onDrag)
        self.canvas.tag_bind("ctrlPts", "<ButtonPress-2>", self.getPos)
        self.canvas.tag_bind("ctrlPts", "<B1-Motion>", self.onMotion)

        self.pack(fill = BOTH, expand = 1)

    def onExit(self):
        self.quit()

    def testMidSubDiv(self, event):
        self.canvas.delete("test")
        ptl, ptr = self.midpointSubDiv(self.ctrlPoints)
        print(len(ptr))
        if(len(ptl) >=2):
            for i in range(len(ptl) - 1):
                self.canvas.create_line(ptl[i].x, ptl[i].y, ptl[i + 1].x, ptl[i + 1].y, tag = "test")
                self.canvas.create_oval(ptl[i].x, ptl[i].y, ptl[i].x + 10, ptl[i].y + 10, tag = "test", fill = "red")

        if(len(ptr) >=2):
            for i in range(len(ptr) - 1):
                self.canvas.create_line(ptr[i].x, ptr[i].y, ptr[i + 1].x, ptr[i + 1].y, tag = "test")
                self.canvas.create_oval(ptr[i].x, ptr[i].y, ptr[i].x + 10, ptr[i].y + 10, tag = "test", fill = "red")

    def addInputPt(self, event):
        #Receives input point from mouse click, draw line segments connecting them, then calls drawCurve
        self.canvas.create_oval(event.x - CONST_POINT_SIZE, event.y - CONST_POINT_SIZE, event.x + CONST_POINT_SIZE, event.y + CONST_POINT_SIZE, fill = "black", tag = "ctrlPts")
        self.ctrlPoints.append(Point(event.x, event.y))
        self.ctrlPtNum.set(len(self.ctrlPoints))
        self.drawLine(event)

        self.drawCurve(event)


    def onDrag(self, event):
        self.dragData["item"] = self.canvas.find_closest(event.x, event.y)[0]
        #self.dragData["item"] = self.canvas.find('closest', event.x, event.y, 'withtag', 'ctrlPts')
        self.dragData["x"] = event.x
        self.dragData["y"] = event.y

        (x1, y1, x2, y2) = self.canvas.coords(self.dragData["item"])
        #print(x1 + 3, y1 + 3)
        self.dragPtIndex = (self.ctrlPoints.index(Point(x1 + CONST_POINT_SIZE, y1 + CONST_POINT_SIZE)))

    def onMotion(self, event):
        delta_x = event.x - self.dragData["x"]
        delta_y = event.y - self.dragData["y"]

        self.canvas.move(self.dragData["item"], delta_x, delta_y)
        self.ctrlPoints[self.dragPtIndex].x += delta_x
        self.ctrlPoints[self.dragPtIndex].y += delta_y

        self.dragData["x"] = event.x
        self.dragData["y"] = event.y

        self.drawLine(event)
        self.drawCurve(event)

    def getPos(self, event):

        curItem = self.canvas.find_closest(event.x, event.y)
        (x1, y1, x2, y2) = self.canvas.coords(curItem)
        #print(x1, y1, x2, y2)
        print(x1 + 3, y1 + 3)

    def drawCurve(self, event = 0):
        #Calls other functions depending on the drop-down menu

        #Clear existing shells and curves
        self.canvas.delete("shell")
        self.canvas.delete("plot")

        if((self.curAlg.get() == self.algList[0] or self.curAlg.get() == self.algList[1]) and self.shouldDrawShell.get() == 1):
            self.drawShell(self.ctrlPoints, float(self.tScale.get()))

        if(self.curAlg.get() == self.algList[0]):
        #De Castlejau
            t = 0
            while(t <= CONST_ITER_STEPS):
                self.drawCurveNLI_NR(self.ctrlPoints, t / CONST_ITER_STEPS)
                t += 1
        elif(self.curAlg.get() == self.algList[1]):
            #De Castlejau, Recursive form
            t = 0
            while(t <= CONST_ITER_STEPS):
                self.drawCurveNLI(self.ctrlPoints, t / CONST_ITER_STEPS)
                t += 1
        elif(self.curAlg.get() == self.algList[2]):
            #BB-form
            self.drawCurveBB(self.ctrlPoints)
        elif(self.curAlg.get() == self.algList[3]):
            #Midpoint Subdivision
            print("Exception: algorithm still under work")
        else:
            print("wtf?! This should NOT happen!")
        

    def updateShellOnTScaleChange(self, t):
        if((self.curAlg.get() == self.algList[0] or self.curAlg.get() == self.algList[1]) and self.shouldDrawShell.get() == 1):
            self.canvas.delete("shell")
            self.drawShell(self.ctrlPoints, float(t))

    def plotPixel(self, x, y):
        self.canvas.create_line(x, y, x + 1, y, fill = "blue", tag = "plot")

    def clearAll(self):
        self.canvas.delete("all")
        self.ctrlPoints.clear()
        self.plotPoints.clear()
        self.ctrlPtNum.set(len(self.ctrlPoints))

    def drawLine(self, event):
        #Clear existing lines
        self.canvas.delete("line")
        #Redraw
        if(len(self.ctrlPoints) >=2):
            for i in range(len(self.ctrlPoints) - 1):
                self.canvas.create_line(self.ctrlPoints[i].x, self.ctrlPoints[i].y, self.ctrlPoints[i + 1].x, self.ctrlPoints[i + 1].y, tag = "line")

    def drawShellLine(self, points):
        if(len(points) >=2):
            for i in range(len(points) - 1):
                self.canvas.create_line(points[i].x, points[i].y, points[i + 1].x, points[i + 1].y, fill = "green", tag = "shell")

    def drawCurveNLI(self, points, t):
        #Nested Loop Interpolation, recursive form
        if(len(points) == 1):
            self.plotPixel(points[0].x, points[0].y)
        else:
            newPoints = []
            for i in range(0, len(points) - 1):
                x = (1 - t) * points[i].x + t * points[i + 1].x
                y = (1 - t) * points[i].y + t * points[i + 1].y
                newPoints.append(Point(x, y))
            
            self.drawCurveNLI(newPoints, t)

    def drawCurveNLI_NR(self, points, t):
        #Nested Loop Interpolation, Non-recursive version
        n = len(points)

        tmp = deepcopy(points)

        for k in range(1, n):
            for i in range (0, n - k):
                tmp[i].x = (1 - t) * tmp[i].x + t * tmp[i + 1].x
                tmp[i].y = (1 - t) * tmp[i].y + t * tmp[i + 1].y

        #for pt in self.plotPoints:
            #print(pt.x, pt.y)
        pt = tmp[0]
        self.plotPixel(pt.x, pt.y)


    def drawShell(self, points, t):
        if(len(points) > 2):
            newPoints = []
            for i in range(0, len(points) - 1):
                x = (1 - t) * points[i].x + t * points[i + 1].x
                y = (1 - t) * points[i].y + t * points[i + 1].y
                newPoints.append(Point(x, y))

            self.drawShellLine(newPoints)
            self.drawShell(newPoints, t)

    def drawCurveBB(self, points):
        for pt in bezierGenerator(self.ctrlPoints, CONST_ITER_STEPS):
            self.plotPixel(pt.x, pt.y)

    def midpointSubDiv(self, points):
        k = len(points)
        left = [Point() for _ in range(k)]
        right = [Point() for _ in range(k)]
        curr = [Point() for _ in range(k - 1)]

        left[0] = points[0]
        right[k - 1] = points[k - 1]

        for i in range(k - 1):
            curr[i].x = 0.5 * points[i].x + 0.5 * points[i + 1].x
            curr[i].y = 0.5 * points[i].y + 0.5 * points[i + 1].y

        
        for i in range(k - 2):
            left[i + 1] = curr[0]
            right[k - 2 - i] = curr[k - 2 - i]
            for j in range(k - 2 - i):
                curr[j].x = 0.5 * curr[j].x + 0.5 * curr[j + 1].x
                curr[j].y = 0.5 * curr[j].y + 0.5 * curr[j + 1].y

        left[k - 1] = curr[0]
        right[0] = curr[0]

        for pt in left:
            self.canvas.create_oval(pt.x, pt.y, pt.x + 20, pt.y + 20, tag = "fuck", fill = "blue")
            print("CURR", pt.x, pt.y)
        return left, right



def main():

    root = Tk()
    root.geometry("800x600+200+200")
    root.option_add('*tearOff', False)
    app = Ilan(root)
    root.mainloop()

if __name__ == '__main__':
    main()
