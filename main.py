#!/usr/bin/env python

# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import subprocess
import sys
import threading
import time
import tkinter
import webbrowser
from datetime import datetime, timedelta
from os import path
import cv2
from google.cloud import speech
from playsound import playsound
import wikipedia
import pyaudio
from wit import Wit
from six.moves import queue
import Windows


Ime = 'Hrvoje'

RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'

STREAMING_LIMIT = 240000  # 4 minutes
SAMPLE_RATE = 16000
CHUNK_SIZE = int(SAMPLE_RATE / 10)  # 100ms

USERNAME_CHECK = False
USERNAME_CHECK_VALUE = 'Computer'

ACTIVE_THREADS_LIST = []


def get_current_time():
    """Return Current Time in MS."""
    return int(round(time.time() * 1000))


if path.exists('C:/Users/Hrvoje/Downloads/Crvena Kraljica-a019d8541cd9.json'):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Hrvoje/Downloads/Crvena Kraljica-a019d8541cd9.json"
else:
    print('Configuration file does not exist - the program will not work without it.')

class GlavniProzor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.__flag = threading.Event()  # The flag used to pause the thread
        self.__flag.set()  # Set to True
        self.__running = threading.Event()  # Used to stop the thread identification
        self.__running.set()  # Set running to True

        self.UseDarkMode = False

        self.TextLabelDarkMode = '#1d42b3'  # Boja teksta - dark mode
        self.TextLabelDarkModeFinal = '#16389e'  # Boja teksta - dark mode - final

        self.TextLabelColor = '#03258c'  # Boja teksta - light mode
        self.TextLabelColorFinal = '#032ca8'  # Boja teksta - light mode - final

        self.MainWindowBackgroundDark = '#040814'  # Pozadina glavnog prozora - dark mode
        self.MainWindowBackground = '#e1e4eb'  # Pozadina glavnog prozora - light mode

        self.TextLabelBackgroundColorDark = self.MainWindowBackgroundDark  # Boja pozadine TextLabel - dark theme
        self.TextLabelBackgroundColor = self.MainWindowBackground  # Boja pozadine TextLabel

        # najti kak se rece mikrofon, kamera, zaslon.

    def returnScreenWidth(self):
        return self.QueenPrimaryWindow.winfo_screenwidth()

    def returnScreenHeight(self):
        return self.QueenPrimaryWindow.winfo_screenheight()

    def callback(self):
        self.QueenPrimaryWindow.quit()

    def EnableDarkMode(self, UsingMenu=False):
        if UsingMenu:
            self.UseDarkMode = True
            self.QueenPrimaryWindow.config(bg=self.MainWindowBackgroundDark)
            self.TextLabel.config(bg=self.TextLabelBackgroundColorDark)
            self.QueenPrimaryWindow.update()
        else:
            self.SayIntermittently('Turning on dark mode.')
            self.UseDarkMode = True
            self.QueenPrimaryWindow.config(bg=self.MainWindowBackgroundDark)
            self.TextLabel.config(bg=self.TextLabelBackgroundColorDark)
            self.QueenPrimaryWindow.update()

    def EnableLightMode(self, UsingMenu=False):
        if UsingMenu:
            self.UseDarkMode = True
            self.QueenPrimaryWindow.config(bg=self.MainWindowBackground)
            self.TextLabel.config(bg=self.TextLabelBackgroundColor)
            self.QueenPrimaryWindow.update()
        else:
            self.SayIntermittently('Turning off dark mode.')
            self.UseDarkMode = True
            self.QueenPrimaryWindow.config(bg=self.MainWindowBackground)
            self.TextLabel.config(bg=self.TextLabelBackgroundColor)
            self.QueenPrimaryWindow.update()

    def PromjenaLabel(self, NoviTekst, IsFinal=False):
        self.NoviTekst = NoviTekst
        if IsFinal:
            if self.UseDarkMode:
                self.TextLabel.config(text=NoviTekst, foreground=self.TextLabelDarkModeFinal,
                                      font=("Courier", 22))  # Tamnija boja teksta za potvrdu kraja
            else:
                self.TextLabel.config(text=NoviTekst, foreground=self.TextLabelColorFinal,
                                      font=("Courier", 22))  # Tamnija boja teksta za potvrdu kraja
        else:
            if self.UseDarkMode:
                self.TextLabel.config(text=NoviTekst, foreground=self.TextLabelDarkMode,
                                      font=("Courier", 22))  # Tamnija boja teksta za potvrdu kraja
            else:
                self.TextLabel.config(text=NoviTekst, foreground=self.TextLabelColor,
                                      font=("Courier", 22))  # Tamnija boja teksta za potvrdu kraja
            # self.TextLabel.config(text=NoviTekst, foreground=colorCode, font=("Courier", 22))

    def SayIntermittently(self, NoviTekst):
        if self.UseDarkMode:
            TextColor = self.TextLabelDarkMode
        else:
            TextColor = self.TextLabelColor
        PopisRijeci = NoviTekst.split()
        for Brojac in range(len(PopisRijeci)):
            self.TextLabel.config(text=PopisRijeci[Brojac], foreground=TextColor, font=("Courier", 22))
            self.QueenPrimaryWindow.update()
            time.sleep(0.3)

    # def SayIntermittentlyAdd(self, NoviTekst):
    #     PopisRijeci = NoviTekst.split()
    #     for Brojac in range(len(PopisRijeci)):
    #         self.TextLabel.config(text=self.TextLabel.cget('text') + PopisRijeci[Brojac], foreground='#c90c0c',
    #                               font=("Courier", 22))
    #         self.QueenPrimaryWindow.update()
    #         time.sleep(1)

    def ClearLabel(self):
        self.TextLabel.config(text='')
        self.QueenPrimaryWindow.update()

    # def ClearLabelIntermittently(self):
    #     while len(self.TextLabel.cget('text').split() != 0):
    #         TesktKutije = self.TextLabel.cget('text').split()
    #         NasumicniBroj = randint(0, len(self.TextLabel.cget('text').split()))
    #         del TesktKutije[NasumicniBroj]
    #         separator = ' '
    #         separator.join(TesktKutije)
    #         self.TextLabel.config(text=TesktKutije)
    #         self.QueenPrimaryWindow.update()
    #         time.sleep(0.3)

    def UpdateTime(self):  # pomocna funkcija
        # get the current local time from the PC
        NovoVrijeme = time.strftime('%H:%M:%S')
        # self.TimeLabel.config(text=NovoVrijeme)
        # self.TimeLabel.after(200, self.UpdateTime)
        # self.QueenPrimaryWindow.update()

    def run(self):
        self.isRunning = True
        self.QueenPrimaryWindow = tkinter.Tk()
        self.QueenPrimaryWindow.title('The Red Queen v0.5')
        # QueenPrimaryWindow.attributes('-fullscreen', True)
        self.QueenPrimaryWindow.state('zoomed')
        screen_width = self.QueenPrimaryWindow.winfo_screenwidth()
        screen_height = self.QueenPrimaryWindow.winfo_screenheight()

        if self.UseDarkMode:
            self.QueenPrimaryWindow.configure(bg=self.MainWindowBackgroundDark)
        else:
            self.QueenPrimaryWindow.configure(bg=self.MainWindowBackground)

        menubar = tkinter.Menu(self.QueenPrimaryWindow)
        # create a pulldown menu, and add it to the menu bar
        filemenu = tkinter.Menu(menubar, tearoff=0)

        # filemenu.add_command(label="Reboot", command = Helpers.restart_program)
        filemenu.add_command(label="Turn off", command=quit)
        filemenu.add_command(label="System version",
                             command=lambda: Windows.ShowSystemVersion(screen_width, screen_height))
        filemenu.add_command(label="Enable dark mode", command=lambda: self.EnableDarkMode(UsingMenu=True))
        # filemenu.add_command(label="Uključi/Isključi mikrofon", command=lambda: self.SwitchMicrophone())
        menubar.add_cascade(label="Red Queen", menu=filemenu)

        # self.TimeLabel = tkinter.Label(self.QueenPrimaryWindow, text="Početni tekst", highlightbackground="#000000")
        # self.TimeLabel.place(x=2460, y=1320)
        # self.TimeLabel.config(foreground="#032ca8", font=("Courier", 12))

        # self.TimeLabel.pack(fill="both", expand=True)
        if self.UseDarkMode:
            self.TextLabel = tkinter.Label(self.QueenPrimaryWindow, bg=self.TextLabelBackgroundColorDark,
                                           text="Red Queen v0.5", fg=self.TextLabelDarkMode,
                                           highlightbackground="white")
            self.TextLabel.pack(pady=screen_height / 2.5)
        else:
            self.TextLabel = tkinter.Label(self.QueenPrimaryWindow, bg=self.TextLabelBackgroundColor,
                                           text="Red Queen v0.5", fg=self.TextLabelColor, highlightbackground="white")
            self.TextLabel.pack(pady=screen_height / 2.5)
        self.UpdateTime()

        # TextInput = tkinter.Entry(font="Calibri 12", bd=0, insertbackground='red')
        # TextInput.bind("<Return>", lambda event: TextProcessing(TextInput.get(), self.QueenPrimaryWindow).start())
        # TextInput.place(x=20, y=930, width=1800, height=40)

        # SlikaMikrofon = Image.open("Microphone.png")
        # SlikaMikrofon = SlikaMikrofon.resize((40, 40), Image.ANTIALIAS)
        # SlikaMikrofon = PhotoImage(SlikaMikrofon)
        # LabelSlikaMikrofon = tkinter.Label(self.QueenPrimaryWindow, image=SlikaMikrofon, height=40, width=40, bd=0)
        # LabelSlikaMikrofon.pack()
        # LabelSlikaMikrofon.place(x=1850, y=930)
        # LabelSlikaMikrofon.bind("<Button-1>", lambda event: TTSThread.Switch())
        self.QueenPrimaryWindow.config(menu=menubar)
        self.QueenPrimaryWindow.mainloop()

    def KillThread(self):
        quit()


class SpeechToText(threading.Thread):  # trazena dretva

    '''

    Thread's purpose is to receive microphone stream, and then uses Google Speech to text API to convert a series of sounds into text.
    The text is then forwarded as a variable to NaturalLanguageProcessing class to determine intent.

    '''

    def __init__(self, WindowName, *args, **kwargs):
        threading.Thread.__init__(self)
        self.WindowName = WindowName
        # super(SpeechToText, self).__init__(*args, **kwargs)
        # self.__flag = threading.Event()  # The flag used to pause the thread
        # self.__flag.set()  # Set to True
        # self.__running = threading.Event()  # Used to stop the thread identification
        # self.__running.set()  # Set running to True

    def run(self):
        try:
            """start bidirectional streaming from microphone input to speech API"""
            client = speech.SpeechClient()
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=SAMPLE_RATE,
                language_code="en-US",
                enable_automatic_punctuation=True,
                max_alternatives=1
            )
            streaming_config = speech.StreamingRecognitionConfig(
                config=config,
                interim_results=True)

            mic_manager = ResumableMicrophoneStream(SAMPLE_RATE, CHUNK_SIZE)

            with mic_manager as stream:
                while not stream.closed:
                    stream.audio_input = []
                    audio_generator = stream.generator()

                    requests = (speech.StreamingRecognizeRequest(
                        audio_content=content) for content in audio_generator)

                    responses = client.streaming_recognize(streaming_config, requests)

                    # Now, put the transcription responses to use.
                    SpeechProcessing(responses, stream, self.WindowName)
                    if stream.result_end_time > 0:
                        stream.final_request_end_time = stream.is_final_end_time
                    stream.result_end_time = 0
                    stream.last_audio_input = []
                    stream.last_audio_input = stream.audio_input
                    stream.audio_input = []
                    stream.restart_counter = stream.restart_counter + 1

                    if not stream.last_transcript_was_final:
                        sys.stdout.write('\n')
                    stream.new_stream = True
        except:
            self.__init__(self.WindowName)

    # def pause(self):
    #     print("pausing")
    #     self.__flag.clear()  # Set to False to block the thread
    #     self.KillThread()
    #
    # def resume(self):
    #     print("resume")
    #     self.__flag.set()  # Set to True, let the thread stop blocking
    #     self.run()
    #
    # def stop(self):
    #     print("stopn")
    #     self.__flag.set()  # Resume the thread from the suspended state, if it is already suspended
    #     self.__running.clear()  # Set to False

    # def Switch(self):
    #     global MicrophoneIsActive
    #     if MicrophoneIsActive:
    #         MicrophoneIsActive = False
    #         print("Turning microphone off.")
    #     else:
    #         MicrophoneIsActive = True
    #         print("Turning microphone on.")

    def KillThread(self):
        quit()

    def ThreadStatus(self):
        return self.is_alive()


if __name__ == '__main__':
    GUIDretva = GlavniProzor()
    TTSThread = SpeechToText(GUIDretva)
    GUIDretva.start()
    TTSThread.start()


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
        if Vrijeme.hour == 00 and Vrijeme.minute == 00 and Vrijeme.second == 00:
            self.UpdateTime('Time\'s up')
            SoundThreadVar = SoundThread("WorkingRedQueen.mp3", True)
            SoundThreadVar.start()
        else:
            Vrijeme = Vrijeme - timedelta(seconds=1)
            time.sleep(1)
            self.UpdateTime(Vrijeme)
            Vrijeme = Vrijeme.strftime('%H:%M:%S')
            self.TimeLabel.after(200, self.CountDown(Vrijeme))

    def UpdateTime(self, NewTime):  # pomocna funkcija
        self.TimeLabel.config(text=NewTime)
        self.QueenCounterWindow.update()

    def KillThread(self):
        del self.BrojSekundi
        quit()

    def run(self):
        self.QueenCounterWindow = tkinter.Tk()
        self.QueenCounterWindow.title('The Red Queen v0.5 - Timer Window')

        self.TimeLabel = tkinter.Label(self.QueenCounterWindow, text="Početni tekst", highlightbackground="#000000")
        self.TimeLabel.pack(fill="x", expand=True)
        self.TimeLabel.config(foreground="#032ca8", font=("Courier", 12))
        self.CountDown(self.Convert(self.BrojSekundi))
        self.QueenCounterWindow.mainloop()

class ResumableMicrophoneStream:
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk_size):
        self._rate = rate
        self.chunk_size = chunk_size
        self._num_channels = 1
        self._buff = queue.Queue()
        self.closed = True
        self.start_time = get_current_time()
        self.restart_counter = 0
        self.audio_input = []
        self.last_audio_input = []
        self.result_end_time = 0
        self.is_final_end_time = 0
        self.final_request_end_time = 0
        self.bridging_offset = 0
        self.last_transcript_was_final = False
        self.new_stream = True
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=self._num_channels,
            rate=self._rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

    def __enter__(self):

        self.closed = False
        return self

    def __exit__(self, type, value, traceback):

        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, *args, **kwargs):
        """Continuously collect data from the audio stream, into the buffer."""

        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        """Stream Audio from microphone to API and to local buffer"""

        while not self.closed:
            data = []

            if self.new_stream and self.last_audio_input:

                chunk_time = STREAMING_LIMIT / len(self.last_audio_input)

                if chunk_time != 0:

                    if self.bridging_offset < 0:
                        self.bridging_offset = 0

                    if self.bridging_offset > self.final_request_end_time:
                        self.bridging_offset = self.final_request_end_time

                    chunks_from_ms = round(
                        (self.final_request_end_time - self.bridging_offset)
                        / chunk_time
                    )

                    self.bridging_offset = round(
                        (len(self.last_audio_input) - chunks_from_ms) * chunk_time
                    )

                    for i in range(chunks_from_ms, len(self.last_audio_input)):
                        data.append(self.last_audio_input[i])

                self.new_stream = False

            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            self.audio_input.append(chunk)

            if chunk is None:
                return
            data.append(chunk)
            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)

                    if chunk is None:
                        return
                    data.append(chunk)
                    self.audio_input.append(chunk)

                except queue.Empty:
                    break

            yield b"".join(data)


def SpeechProcessing(responses, stream, WindowName):  # listen_print loop
    for response in responses:
        if get_current_time() - stream.start_time > STREAMING_LIMIT:
            stream.start_time = get_current_time()
            break

        if not response.results:
            continue

        result = response.results[0]

        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript

        result_seconds = 0
        result_nanos = 0

        if result.result_end_time.seconds:
            result_seconds = result.result_end_time.seconds

        if result.result_end_time.microseconds:
            result_nanos = result.result_end_time.microseconds

        stream.result_end_time = int((result_seconds * 1000) + (result_nanos / 1000000))

        corrected_time = (stream.result_end_time - stream.bridging_offset
                          + (STREAMING_LIMIT * stream.restart_counter))

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.

        if result.is_final:
            WindowName.PromjenaLabel(transcript + "\r", True)
            NaturalLanguageProcessingDretva = NaturalLanguageProcessing(transcript, WindowName)
            NaturalLanguageProcessingDretva.start()
            PlaySound = SoundThread("WorkingRedQueen.mp3")
            time.sleep(0.1)
            PlaySound.start()
            stream.is_final_end_time = stream.result_end_time
            stream.last_transcript_was_final = True

        # Exit recognition if any of the transcribed phrases could be
        # one of our keywords.
        # if re.search(r'\b(exit|quit)\b', transcript, re.I):
        #     sys.stdout.write('Exiting...\n')
        #     stream.closed = True
        #     break
        else:
            WindowName.PromjenaLabel(transcript + "\r")
            sys.stdout.write(transcript + "\r")
            stream.last_transcript_was_final = False


def CloseCamera():
    print("Camera")
    for Thread in ACTIVE_THREADS_LIST:
        if type(Thread) == OpenVideoFeed:
            Thread.KillThread()


class NaturalLanguageProcessing(threading.Thread):
    '''

    Thread's purpose is to receive text which requires processing (TekstZaObradu), and reference to main GUI window (WindowName).
    The thread then uses the Wit.ai API library to understand what order you meant to give, and act accordingly

    '''

    def __init__(self, TekstZaObradu, WindowName):
        self.TekstZaObradu = TekstZaObradu
        self.TargetWindow = WindowName
        threading.Thread.__init__(self)

    def run(self):  # moja koda
        # print("Pokrenuta dretva", self.TekstZaObradu)
        client = Wit("L2SE6YQB54PDESGSR5S5HPCTXFEVB4A7")
        resp = client.message(self.TekstZaObradu)
        try:
            UserIntent = resp['intents'][0]['name']
            if UserIntent == 'FindInformation':
                # pass
                SearchTerm = resp['entities']['SearchTerm:SearchTerm'][0]['value']
                WikipediaSummary = wikipedia.summary(SearchTerm)
                NewFile = open('C:/Users/Hrvoje/Desktop/' + SearchTerm + '.txt', 'a', encoding='utf-8')
                NewFile.write(WikipediaSummary)
                NewFile.close()
                os.startfile('C:/Users/Hrvoje/Desktop/' + SearchTerm + '.txt')
            elif UserIntent == 'LockComputer':
                self.TargetWindow.SayIntermittentlyAdd('Locking the PC')
                LockPCThread = LockPC()
                ACTIVE_THREADS_LIST.append(LockPCThread)
                LockPCThread.start()
            elif UserIntent == 'CountDown':
                TimeFrame = resp['entities']['wit$duration:duration'][0]['normalized']['value']
                BrojacProzor = CountDown(TimeFrame)
                BrojacProzor.start()
            elif UserIntent == 'NameCheck':
                self.TargetWindow.SayIntermittently('Your name is %s' % Ime)
            elif UserIntent == 'OpenCamera':
                self.TargetWindow.SayIntermittently('Opening camera.')
                CameraThread = OpenVideoFeed()
                ACTIVE_THREADS_LIST.append(CameraThread)
                CameraThread.start()
            elif UserIntent == 'CloseCamera':
                CloseCamera()
            elif UserIntent == 'FavoriteSong':
                webbrowser.open('https://www.youtube.com/watch?v=wXP4D_hCfqw&list=RDwXP4D_hCfqw&start_radio=1')
                # istraziti kaj je neko drugi napravil slicno tome kaj dejansko sam naredil,
                # ali je želo drugi to naredil
                # mentor isce v polju de radi, navdusljeni
            elif UserIntent == 'CountDown':
                TimeFrame = resp['entities']['wit$duration:duration'][0]['normalized']['value']
                BrojacProzor = CountDown(TimeFrame)
                ACTIVE_THREADS_LIST.append(BrojacProzor)
                BrojacProzor.start()
            elif UserIntent == 'NameCheck':
                self.TargetWindow.SayIntermittently('Your name is %s' % Ime)
            elif UserIntent == 'OpenNote':
                # IsEncrypted = resp['traits']['Encrypted'][0]['value']  # Either "True" or "False"
                print(resp['entities']['FileName:FileName'])
                FileName = resp['entities']['FileName:FileName'][0]['value']
                # if(IsEncrypted == 'True'):
            elif UserIntent == 'TurnOnDarkMode':
                self.TargetWindow.EnableDarkMode()
            elif UserIntent == 'TurnOffDarkMode':
                self.TargetWindow.EnableLightMode()
            elif UserIntent == 'SearchImages':
                print(resp)
                SearchTerm = resp['entities']['SearchTerm:SearchTerm'][0]['value']
                URL = 'https://www.google.com/search?q={}&tbm=isch'.format(SearchTerm.replace(' ', '+'))
                print(SearchTerm)
                webbrowser.open(URL)
                # https://www.google.com/search?q=New+York&tbm=isch
            elif UserIntent == 'ShowInfo':
                screen_width = self.TargetWindow.returnScreenWidth()
                screen_height = self.TargetWindow.returnScreenHeight()
                Windows.ShowSystemVersion(screen_width, screen_height)
            elif UserIntent == 'OpenWit':
                self.TargetWindow.SayIntermittently('Opening Wit language console.')
                webbrowser.open("https://wit.ai/apps/709037316327811/understanding")
        except IndexError:
            self.TargetWindow.SayIntermittently('I didn\'t quite understand that.')

    def KillThread(self):
        quit()


class LockPC(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        cmd = 'rundll32.exe user32.dll, LockWorkStation'
        subprocess.call(cmd)

    def KillThread(self):
        quit()


class SoundThread(threading.Thread):
    def __init__(self, SoundFilePath, ContniousLoop=False):
        threading.Thread.__init__(self)
        self.SoundFilePath = SoundFilePath
        self.ContniousLoop = ContniousLoop

    # def __del__(self):
    def run(self):
        if self.ContniousLoop:
            while 1:
                playsound(self.SoundFilePath)
                time.sleep(1.1)
        playsound(self.SoundFilePath)

    def KillThread(self):
        del self.SoundFilePath
        del self.ContniousLoop
        quit()


class OpenVideoFeed(threading.Thread):

    def run(self):
        vid = cv2.VideoCapture(0)
        CameraRunning = True
        while CameraRunning:
            # Capture the video frame
            # by frame
            ret, frame = vid.read()

            # Display the resulting frame
            cv2.imshow('frame', frame)

            # the 'q' button is set as the
            # quitting button you may use any
            # desired button of your choice
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # After the loop release the cap object
        vid.release()
        # Destroy all the windows
        cv2.destroyAllWindows()

    def KillThread(self):
        print("CamreKill")

        quit()


def KillAllThreads():
    for Thread in ACTIVE_THREADS_LIST:
        Thread.KillThread()
