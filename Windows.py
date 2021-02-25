import tkinter


def ShowSystemVersion(ParetnWindowWidth, ParentWindowHeight):
    QueenVersionWindow = tkinter.Tk()
    QueenVersionWindow.title('The Red Queen version information')
    QueenVersionWindow.geometry('%ix%i+%i+%i' % (
    ParetnWindowWidth / 4, ParentWindowHeight / 10, ParetnWindowWidth * 0.375, ParentWindowHeight * 0.45))
    QueenVersionWindow.resizable(0, 0)

    VersionWindowWidth = QueenVersionWindow.winfo_screenwidth()
    VersionWindowHeight = QueenVersionWindow.winfo_screenheight()

    TextBoxLabel = tkinter.Label(QueenVersionWindow, text='Queen version: v0.5', wraplength=500)
    TextBoxLabel.place(x=VersionWindowWidth * 0.005, y=VersionWindowHeight / 15)

    TextBoxLabel = tkinter.Label(QueenVersionWindow, text='Autor: Hrvoje Zeman', wraplength=500)
    TextBoxLabel.place(x=VersionWindowWidth * 0.005, y=VersionWindowHeight / 20)

    QueenVersionWindow.mainloop()
