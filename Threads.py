import sys
import time
import tkinter

from google.cloud import speech
from wit import Wit

import Windows
import threading
from datetime import datetime, timedelta
from Miscellaneous import SoundThread, LockPC
from random import randint

# noinspection PyAttributeOutsideInit
from ResumableMicrophoneStream import ResumableMicrophoneStream

Ime = 'Hrvoje'

STREAMING_LIMIT = 240000  # 4 minutes
SAMPLE_RATE = 16000
CHUNK_SIZE = int(SAMPLE_RATE / 10)  # 100ms


class GlavniProzor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def callback(self):
        self.QueenPrimaryWindow.quit()

    def PromjenaLabel(self, NoviTekst, IsFinal=False, colorCode='#032ca8'):
        self.NoviTekst = NoviTekst
        self.colorCode = colorCode
        if IsFinal:
            self.TextLabel.config(text=NoviTekst, foreground="#032ca8",
                                  font=("Courier", 22))  # Tamnija boja teksta za potvrdu kraja
        else:
            self.TextLabel.config(text=NoviTekst, foreground=colorCode, font=("Courier", 22))

    def SayIntermittently(self, NoviTekst):
        PopisRijeci = NoviTekst.split()
        for Brojac in range(len(PopisRijeci)):
            self.TextLabel.config(text=PopisRijeci[Brojac], foreground='#c90c0c', font=("Courier", 22))
            self.QueenPrimaryWindow.update()
            time.sleep(0.3)

    def SayIntermittentlyAdd(self, NoviTekst):
        PopisRijeci = NoviTekst.split()
        for Brojac in range(len(PopisRijeci)):
            self.TextLabel.config(text=self.TextLabel.cget('text') + PopisRijeci[Brojac], foreground='#c90c0c', font=("Courier", 22))
            self.QueenPrimaryWindow.update()
            time.sleep(1)

    def ClearLabel(self):
        self.TextLabel.config(text='')
        self.QueenPrimaryWindow.update()

    def ClearLabelIntermittently(self):
        while len(self.TextLabel.cget('text').split() != 0):
            TesktKutije = self.TextLabel.cget('text').split()
            NasumicniBroj = randint(0, len(self.TextLabel.cget('text').split()))
            del TesktKutije[NasumicniBroj]
            separator = ' '
            separator.join(TesktKutije)
            self.TextLabel.config(text=TesktKutije)
            self.QueenPrimaryWindow.update()
            time.sleep(0.3)

    def UpdateTime(self):  # pomocna funkcija
        # get the current local time from the PC
        NovoVrijeme = time.strftime('%H:%M:%S')
        self.TimeLabel.config(text=NovoVrijeme)
        self.TimeLabel.after(200, self.UpdateTime)
        self.QueenPrimaryWindow.update()

    def run(self):
        self.QueenPrimaryWindow = tkinter.Tk()
        self.QueenPrimaryWindow.title('The Red Queen v0.5')
        # QueenPrimaryWindow.attributes('-fullscreen', True)
        self.QueenPrimaryWindow.state('zoomed')
        screen_width = self.QueenPrimaryWindow.winfo_screenwidth()
        screen_height = self.QueenPrimaryWindow.winfo_screenheight()

        menubar = tkinter.Menu(self.QueenPrimaryWindow)
        # create a pulldown menu, and add it to the menu bar
        filemenu = tkinter.Menu(menubar, tearoff=0)

        # filemenu.add_command(label="Reboot", command = Helpers.restart_program)
        filemenu.add_command(label="Turn off", command=quit)
        filemenu.add_command(label="System version",
                             command=lambda: Windows.ShowSystemVersion(screen_width, screen_height))
        menubar.add_cascade(label="Red Queen", menu=filemenu)

        self.TimeLabel = tkinter.Label(self.QueenPrimaryWindow, text="Početni tekst", highlightbackground="#000000")
        self.TimeLabel.place(x=2460, y=1320)
        self.TimeLabel.config(foreground="#032ca8", font=("Courier", 12))

        # self.TimeLabel.pack(fill="both", expand=True)

        self.TextLabel = tkinter.Label(self.QueenPrimaryWindow, text="Početni tekst", highlightbackground="#000000")
        self.TextLabel.pack(fill="x", expand=True)

        # TextBox = tkinter.Text(self.QueenPrimaryWindow, height=1, width=100, font=("Helvetica", 18))
        # TextBox.bind('<Return>', callback)
        # TextBox.pack()

        # TextBox = tkinter.Entry(self.QueenPrimaryWindow, style='pad.TEntry', padding='5 1 1 1')
        # TextBox.bind('<Return>', TextProcessing(TextBox.get(), self.QueenPrimaryWindow))
        # TextBox.pack()

        self.UpdateTime()

        self.QueenPrimaryWindow.config(menu=menubar)
        self.QueenPrimaryWindow.mainloop()

    def KillThread(self):
        quit()

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
            WindowName.PromjenaLabel(transcript, True)
            sys.stdout.write(transcript + '\n')
            NaturalLanguageProcessingDretva = NaturalLanguageProcessing(transcript, WindowName)
            NaturalLanguageProcessingDretva.start()
            PlaySound = SoundThread("WorkingRedQueen.mp3")
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
            WindowName.PromjenaLabel(transcript)
            sys.stdout.write(transcript + "\r")
            stream.last_transcript_was_final = False

class NaturalLanguageProcessing(threading.Thread):

    '''

    Thread's purpose is to receive text which requires processing (TekstZaObradu), and reference to main GUI window (WindowName).
    The thread then uses the Wit.ai API library to understand what order you meant to give, and act accordingly

    '''

    def __init__(self, TekstZaObradu, WindowName):
        self.TekstZaObradu = TekstZaObradu
        self.TargetWindow = WindowName
        threading.Thread.__init__(self)

    def run(self):
        client = Wit("L2SE6YQB54PDESGSR5S5HPCTXFEVB4A7")
        resp = client.message(self.TekstZaObradu)
        try:
            UserIntent = resp['intents'][0]['name']
            if UserIntent == 'FindInformation':
                print(UserIntent)
            elif UserIntent == 'LockComputer':
                self.TargetWindow.SayIntermittentlyAdd('Locking the PC')
                LockPCThread = LockPC()
                LockPCThread.start()
            elif UserIntent == 'CountDown':
                TimeFrame = resp['entities']['wit$duration:duration'][0]['normalized']['value']
                BrojacProzor = CountDown(TimeFrame)
                BrojacProzor.start()
            elif UserIntent == 'NameCheck':
                self.TargetWindow.SayIntermittently('Your name is %s' % Ime)
        except IndexError:
            self.TargetWindow.SayIntermittently('I didn\'t quite understand that.')

    def KillThread(self):
        quit()

class SpeechToText(threading.Thread):

    '''

    Thread's purpose is to receive microphone stream, and then uses Google Speech to text API to convert a series of sounds into text.
    The text is then forwarded as a variable to NaturalLanguageProcessing class to determine intent.

    '''
    def __init__(self, WindowName):
        threading.Thread.__init__(self)
        self.WindowName = WindowName

    def run(self):
        """start bidirectional streaming from microphone input to speech API"""
        client = speech.SpeechClient()
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=SAMPLE_RATE,
            language_code="en-US",
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

                responses = client.streaming_recognize(streaming_config,
                                                       requests)

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

    def KillThread(self):
        quit()

def get_current_time():
    """Return Current Time in MS."""
    return int(round(time.time() * 1000))