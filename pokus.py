import sys
import threading
import time
import tkinter
from datetime import datetime, timedelta

class CountDown(threading.Thread):
    def __init__(self, BrojSekundi):
        threading.Thread.__init__(self)
        self.BrojSekundi = BrojSekundi

    def Convert(self, seconds):
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60

        return "%d:%02d:%02d" % (hour, minutes, seconds)

    def CountDown(self, Vrijeme):
        Vrijeme = datetime.strptime(Vrijeme, '%H:%M:%S')
        Vrijeme = Vrijeme - timedelta(seconds = 1)
        if str(Vrijeme.strftime('%H')) == '00' and str(Vrijeme.strftime('%M')) == '00' and str(Vrijeme.strftime('%S')) == '00':
            self.join()
        time.sleep(1)
        self.UpdateTime(Vrijeme)
        self.TimeLabel.after(200, self.CountDown(datetime.strftime(Vrijeme, '%H:%M:%S')))

    def UpdateTime(self, NewTime):  # pomocna funkcija
        self.TimeLabel.config(text=NewTime)
        self.QueenCounterWindow.update()

    def callback(self):
        self.QueenCounterWindow.quit()

    def run(self):
        self.QueenCounterWindow = tkinter.Tk()
        self.QueenCounterWindow.title('The Red Queen v0.5 - Timer Window')

        self.TimeLabel = tkinter.Label(self.QueenCounterWindow, text="Početni tekst", highlightbackground="#000000")
        self.TimeLabel.pack(fill="x", expand=True)
        self.TimeLabel.config(foreground="#032ca8", font=("Courier", 12))
        self.CountDown(self.Convert(self.BrojSekundi))
        self.QueenCounterWindow.mainloop()


x = CountDown(5)
x.start()

