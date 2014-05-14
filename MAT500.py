from tkinter import *


class Ilan(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, background = "white")

        self.parent = parent

        self.initUI()

    def initUI(self):

        self.parent.title("MAT500")
        self.pack(fill = BOTH, expand = 1)

        menubar = Menu(self.parent)
        self.parent.config(menu = menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label = "Exit", command = self.onExit)
        menubar.add_cascade(label = "File", menu = fileMenu)

    def onExit(self):
        self.quit()

def main():

    root = Tk()
    root.geometry("800x600+200+200")
    root.option_add('*tearOff', False)
    app = Ilan(root)
    root.mainloop()

if __name__ == '__main__':
    main()
