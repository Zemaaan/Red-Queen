#!/usr/bin/env
try:
    import ctypes
    from tkinter import *
    import os
    import webbrowser
    import platform
    from datetime import *
    import subprocess
    import platform
    import os
    from nltk import *

except:
    raise ImportError("Modules missing... Exiting")


# @formatter:off
facebook = ['Facebook', 'facebook', 'feys', 'otvori facebook', 'otvori Facebook', 'Otvori Facebook', 'Feys','Open Facebook', 'open Facebook', 'Open facebook', 'open Facebook']
google = ['Google', 'google', 'otvori google', 'otvori Google', 'Otvori Google', 'guglaj', 'Open Google','open Facebook', 'Open google', 'open Facebook']
twitter = ['Twitter', 'twitter', 'otvori twitter', 'otvori Twitter', 'Otvori Twitter', 'Open Twitter', 'open Facebook','Open twitter', 'open Facebook']
youtube = ['Youtube', 'youtube', 'otvori youtube', 'otvori Youtube', 'Otvori Youtube', 'Open Youtube', 'open Facebook','Open youtube', 'open Facebook']
log = ['Purge log', 'purge log', 'Purge Log', 'purge Log', 'clean log', 'Izbrisi zapis', 'izbrisi zapis', 'Purge','purge']
cd_lid = ['Otvori CD', 'otvori CD', 'otvori Cd', 'otvori cd', 'cd']
os_array = {'OS system', 'os system', 'Os system', 'OS System', 'System version', 'system version', 'System', 'system', 'System Version'}
sleep = ['sleep', 'Sleep', 'go to sleep', 'Go to sleep']
time = ['Time', 'time']
date = ['Date', 'date']
# @formatter:on
window = Tk()


def named_entities(text):
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    prev = None
    continuous_chunk = []
    current_chunk = []
    for i in chunked:
            if type(i) == Tree:
                    current_chunk.append(" ".join([token for token, pos in i.leaves()]))
            elif current_chunk:
                    named_entity = " ".join(current_chunk)
                    if named_entity not in continuous_chunk:
                            continuous_chunk.append(named_entity)
                            continuous_chunk = [continuous_chunk.replace('[', '') for continuous_chunk in continuous_chunk]
                            current_chunk = []
            else:
                    continue
    return continuous_chunk


def terminate():
    window.destroy()


def onclick():
    user = e.get()
    podjeljeno = user.split()
    count = len(podjeljeno)
    if user == '':
        empty_warning_window = Tk()
        empty_warning_window.title("E.V.E empty input field")
        empty_warning_window.configure(background='#000000')
        empty_warning_window.minsize(width=550, height=25)
        empty_warning_window.pack(padx=10, pady=300)
        os.wait()
    if user == 'Version':
        version = Tk()
        version.title("E.V.E version data")
        version.append("ddd")
        version.configure(background='#2CC1F2')
        version.minsize(width=550, height=25)
        os.wait()
    if podjeljeno[0] == 'show' and podjeljeno[1] == 'information' and podjeljeno[2] == 'on':
        ime = user
        user = user.replace('show information on', '')
        import wikipedia
        wikipedia_article = wikipedia.summary(user)
        wikipedia_article = wikipedia_article.encode("utf-8", 'ignore')
        wiki_window = Tk()
        text = Text(wiki_window)
        text.pack(pady=5, ipadx=500, ipady=330, side=BOTTOM)
        text.insert(INSERT, wikipedia_article)
        wiki_window.title("E.V.E v0.1 - " + user)
        os.wait()
    if user in facebook:
        webbrowser.open('http://www.facebook.com/logout.php')
    elif user in twitter:
        webbrowser.open('https://twitter.com/')
    elif user in cd_lid:
        # @formatter:off
        ctypes.windll.winmm.mciSendStringW("set cdaudio door open", None, 0, None)  # "set cdaudio door open" is command to open cd tray
        # @formatter:on
    elif user in youtube:
        webbrowser.open('http://www.youtube.com')
    elif user in google:
        webbrowser.open('http://www.google.com')
    elif user in time:
        print(datetime.now().strftime('%H:%M:%S'))
    elif user in date:
        print(datetime.now().strftime('%d-%m-%Y'))
    elif user in os_array:
        os_window = Tk()
        os_window.title("E.V.E v0.1 - Platform version")
        os_window.resizable(width=FALSE, height=FALSE)
        os_window.minsize(width=1360, height=700)
        os_window.maxsize(width=1360, height=700)
        text = Text(os_window)
        text.pack(pady=1, ipadx=500, ipady=330, side=BOTTOM)
        text.insert(INSERT, platform.system() + ' ' + platform.release())
        os_window.mainloop()
    elif count >= 2 and podjeljeno[0] == 'Google':
        replaced = user.replace('Google', '')
        webbrowser.open("https://www.google.com/search?q={}".format(replaced))
    elif user == 'Terminate':
        terminate()
    elif user in sleep:
        os.system(r'%windir%\system32\rundll32.exe powrprof.dll,SetSuspendState Hibernate')
    elif podjeljeno[0] == 'Google':
        webbrowser.open("https://www.google.com/search?q={}".format(user))
    else:
        entity = named_entities(user)
        import wikipedia
        article = wikipedia.summary(entity[0])
        wiki_window = Tk()
        text = Text(wiki_window)
        text.pack(pady=5, ipadx=500, ipady=330, side=BOTTOM)
        text.insert(INSERT, article)
        wiki_window.title("E.V.E v0.1 - " + entity[0])


window.configure(background='#2CC1F2')


window.title("The Red Queen v0.1")

window.resizable(width=FALSE, height=FALSE)
window.minsize(width=1300, height=700)
window.maxsize(width=1300, height=700)
e = Entry(window, font="Helvetica 25 bold", text="cekam naredbu")
e.pack(padx=10, pady=300, ipadx=100, ipady=10)
button = Button(window, text="   Predaj zahtjev   ", command=onclick)
button.pack(ipadx=100)
button.place(x=650, y=400)
window.mainloop()
