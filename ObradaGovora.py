STREAMING_LIMIT = 240000  # 4 minutes
SAMPLE_RATE = 16000
CHUNK_SIZE = int(SAMPLE_RATE / 10)  # 100ms


'''

FILE CONTENTS HAVE BEEN MOVED TO Threads.py

'''



# class TextProcessing(threading.Thread):
#     def __init__(self, TekstZaObradu, WindowName):
#         self.TekstZaObradu = TekstZaObradu
#         self.WindowName = WindowName
#         threading.Thread.__init__(self)
#         # NaturalLanguageProcessing(TekstZaObradu, WindowName).start()
#
#     def run(self):
#         client = Wit("L2SE6YQB54PDESGSR5S5HPCTXFEVB4A7")
#         resp = client.message(self.TekstZaObradu)
#         print(resp['intents'][0]['name'])
#         if resp['intents'][0]['name'] == 'FindInformation':
#             print(resp['intents'][0]['name'])
#         elif resp['intents'][0]['name'] == 'LockComputer':
#             self.WindowName.SayIntermittently('I will now lock the PC')
#             LockPCThread = LockPC()
#             LockPCThread.start()
#         elif resp['intents'][0]['name'] == 'CountDown':
#             TimeFrame = resp['entities']['wit$duration:duration'][0]['normalized']['value']
#             BrojacProzor = CountDown(TimeFrame)
#             BrojacProzor.start()
#         elif resp['intents'][0]['name'] == 'NameCheck':
#             self.WindowName.SayIntermittently('Your name is Hrvoje')

# stickytape "E:\Artificial Intelligence\The Red Queen\v0.5" --add-python-path "E:\Artificial Intelligence\The Red Queen\v0.5" --output-file "E:\Artificial Intelligence\The Red Queen\v0.5"
