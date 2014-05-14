from tkinter import *


class Ilan(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, background = "white")

        self.parent = parent
        self.points = []

        self.initUI()

    def initUI(self):

        self.parent.title("MAT500")
        self.pack(fill = BOTH, expand = 1)

        menubar = Menu(self.parent)
        self.parent.config(menu = menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label = "Exit", command = self.onExit)
        menubar.add_cascade(label = "File", menu = fileMenu)

        self.canvas = Canvas(self)
        self.canvas.bind("<Button-1>", self.addPoint)
        self.canvas.bind("<Button-2>", self.printPoints)
        self.canvas.pack(fill = BOTH, expand = 1)

    def onExit(self):
        self.quit()

    def addPoint(self, event):
        self.canvas.create_oval(event.x, event.y, event.x + 1, event.y + 1, fill = "black")
        self.points.append(event.x)
        self.points.append(event.y)

    def printPoints(self, event):
        print(len(self.points))

def main():

    root = Tk()
    root.geometry("800x600+200+200")
    root.option_add('*tearOff', False)
    app = Ilan(root)
    root.mainloop()

if __name__ == '__main__':
    main()
