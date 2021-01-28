import subprocess
import threading
import time

from playsound import playsound

class LockPC(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        cmd = 'rundll32.exe user32.dll, LockWorkStation'
        subprocess.call(cmd)

    def KillThread(self):
        quit()


class SoundThread(threading.Thread):
    def __init__(self, SoundFilePath, ContniousLoop = False):
        threading.Thread.__init__(self)
        self.SoundFilePath = SoundFilePath
        self.ContniousLoop = ContniousLoop
    # def __del__(self):
    def run(self):
        if self.ContniousLoop:
            while 1:
                playsound(self.SoundFilePath)
                time.sleep(0.8)
        playsound(self.SoundFilePath)

    def KillThread(self):
        del self.SoundFilePath
        del self.ContniousLoop
        quit()
