from tkinter import *
import sys, math

CONST_POINT_SIZE = 5

class Point():

    def __init__(self, X = 0, Y = 0):
        self.x = X
        self.y = Y

    def addP(self, rhs):
        self.x += rhs.x
        self.y += rhs.y

    def subP(self, rhs):
        self.x -= rhs.x
        self.y -= rhs.y

    def mulP(self, rhs):
        self.x *= rhs.x
        self.y *= rhs.y

    def divP(self, rhs):
        self.x /= rhs.x
        self.y /= rhs.y

    def prnt(self):
        print("X: ", self.x, " Y: ", self.y)

    def resetP(self):
        self.x = 0
        self.y = 0
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

def binomialCof(i, n):
    return math.factorial(n) / float(math.factorial(i) * math.factorial(n - i))

def bernstein(t, i, n):
    return binomialCof(i, n) * (t ** i) * ((1 - t) ** (n - i))

class Ilan(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, background = "white")

        self.parent = parent
        self.points = []
        self.ctrlPoints = []
        self.dragPtIndex = 128

        self.initUI()

        self.dragData = {"x": 0, "y": 0, "item": None}

    def initUI(self):

        self.parent.title("MAT500")

        menubar = Menu(self.parent)
        self.parent.config(menu = menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label = "Exit", command = self.onExit)
        menubar.add_cascade(label = "File", menu = fileMenu)

        algList = ("De Casteljau", "Bernstein", "Midpt Subdiv")
        self.strVar = StringVar()
        self.strVar.set(algList[0])

        self.toolbar = Frame(self.parent, height = 20, bd = 1, relief = RAISED)

        self.algMenu = OptionMenu(self.toolbar, self.strVar, *algList)
        self.algMenu.pack(side = "left")

        self.clearBtn = Button(self.toolbar, text = "clear", state = DISABLED)
        self.clearBtn.pack(side = "left")
        self.tScale = Scale(self.toolbar, orient = HORIZONTAL, from_ = 0.0, to = 1.0, resolution = 0.01, command = self.updateShellOnTScaleChange)
        self.tScale.set(0.5)
        self.tScale.pack(side = "left")
        self.toolbar.pack(side = "top", fill = X)

        self.canvas = Canvas(self)
        self.canvas.pack(fill = BOTH, expand = 1)
        self.canvas.bind("<ButtonPress-2>", self.onCMB)
        #self.canvas.bind("<ButtonPress-2>", self.drawLine)
        self.canvas.bind("<ButtonPress-3>", self.onRMB)
        self.canvas.tag_bind("ctrlPts", "<ButtonPress-1>", self.onDrag)
        self.canvas.tag_bind("ctrlPts", "<ButtonPress-2>", self.getPos)
        self.canvas.tag_bind("ctrlPts", "<B1-Motion>", self.onMotion)

        self.pack(fill = BOTH, expand = 1)
    def onExit(self):
        self.quit()

    def onRMB(self, event):
        self.canvas.create_oval(event.x - CONST_POINT_SIZE, event.y - CONST_POINT_SIZE, event.x + CONST_POINT_SIZE, event.y + CONST_POINT_SIZE, fill = "black", tag = "ctrlPts")
        self.ctrlPoints.append(Point(event.x, event.y))
        print("Add point: x = ", event.x, "y = ", event.y)
        self.drawLine(event)

        self.onCMB(event)


    def onDrag(self, event):
        self.dragData["item"] = self.canvas.find_closest(event.x, event.y)[0]
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
        self.onCMB(event)

    def getPos(self, event):

        curItem = self.canvas.find_closest(event.x, event.y)
        (x1, y1, x2, y2) = self.canvas.coords(curItem)
        #print(x1, y1, x2, y2)
        print(x1 + 3, y1 + 3)

    def onCMB(self, event):
        self.canvas.delete("shell")
        self.drawShell(self.ctrlPoints, float(self.tScale.get()))

        self.canvas.delete("plot")
        t = 0
        while(t <= 1024):
            self.drawCurveNLI(self.ctrlPoints, t / 1024)
            t += 1

    def updateShellOnTScaleChange(self, t):
        self.canvas.delete("shell")
        self.drawShell(self.ctrlPoints, float(t))

    def plotPixel(self, x, y):
        self.canvas.create_line(x, y, x + 1, y, fill = "blue", tag = "plot")

    def drawLine(self, event):
        #Clear existing lines
        self.canvas.delete("line")
        #Redraw
        if(len(self.ctrlPoints) >=2):
            for i in range(len(self.ctrlPoints) - 1):
                self.canvas.create_line(self.ctrlPoints[i].x, self.ctrlPoints[i].y, self.ctrlPoints[i + 1].x, self.ctrlPoints[i + 1].y, tag = "line")

    def drawShellLine(self, points):
        #Redraw
        if(len(points) >=2):
            for i in range(len(points) - 1):
                self.canvas.create_line(points[i].x, points[i].y, points[i + 1].x, points[i + 1].y, fill = "green", tag = "shell")

    def drawCurveNLI(self, points, t):
        #Clear existing curves
        #Redraw
        if(len(points) == 1):
            self.plotPixel(points[0].x, points[0].y)
        else:
            newPoints = []
            for i in range(0, len(points) - 1):
                x = (1 - t) * points[i].x + t * points[i+1].x
                y = (1 - t) * points[i].y + t * points[i+1].y
                newPoints.append(Point(x, y))
            
            self.drawCurveNLI(newPoints, t)

    def drawShell(self, points, t):
        if(len(points) > 2):
            newPoints = []
            for i in range(0, len(points) - 1):
                x = (1 - t) * points[i].x + t * points[i + 1].x
                y = (1 - t) * points[i].y + t * points[i + 1].y
                newPoints.append(Point(x, y))
                print(len(newPoints))
                print("NP: ", x, y)

            self.drawShellLine(newPoints)
            self.drawShell(newPoints, t)


def main():

    root = Tk()
    root.geometry("800x600+200+200")
    root.option_add('*tearOff', False)
    app = Ilan(root)
    root.mainloop()

if __name__ == '__main__':
    main()
