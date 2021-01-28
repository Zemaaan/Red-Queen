import webbrowser
import ctypes
from datetime import datetime
# formerly asdfghjkl.py
datum = datetime.now().strftime('%d-%m-%Y')
vrijeme = datetime.now().strftime('%H:%M:%S')

# @formatter:off
facebook = ['Facebook', 'facebook', 'feys', 'otvori facebook', 'otvori Facebook', 'Otvori Facebook', 'Feys','Open Facebook', 'open Facebook', 'Open facebook', 'open Facebook']
google = ['Google', 'google', 'otvori google', 'otvori Google', 'Otvori Google', 'guglaj', 'Open Google', 'open Facebook', 'Open google', 'open Facebook']
twitter = ['Twitter', 'twitter', 'otvori twitter', 'otvori Twitter', 'Otvori Twitter', 'Open Twitter', 'open Facebook', 'Open twitter', 'open Facebook']
youtube = ['Youtube', 'youtube', 'otvori youtube', 'otvori Youtube', 'Otvori Youtube', 'Open Youtube', 'open Facebook', 'Open youtube', 'open Facebook']
log = ['Purge log', 'purge log', 'Purge Log', 'purge Log', 'clean log', 'Izbrisi zapis', 'izbrisi zapis', 'Purge', 'purge']
cd_lid = ['Otvori CD', 'otvori CD', 'otvori Cd', 'otvori cd', 'cd']
# @formatter:on


while True:
    userInput = input()
    podjeljeno = userInput.split()
    count = len(podjeljeno)

    if userInput in log:
        potvrda = input("")
        if potvrda == purge_log_password:
            f = open('C:/Users/Hrvoje/Desktop/log.txt', 'w')
            f.write('')
            f.close()
            print("Prociscivanje zavrseno")
        else:
            print("Pogresna Lozinka")

    elif userInput in cd_lid:
        # @formatter:off
        ctypes.windll.winmm.mciSendStringW("set cdaudio door open", None, 0, None)  # "set cdaudio door open" is command to open cd tray
        ctypes.windll.winmm.mciSendStringW("set cdaudio door close", None, 0, None)  # "set cdaudio door close" is command to slose cd tray
        # @formatter:on
        f = open('C:/Users/Hrvoje/Desktop/log.txt', 'a')
        f.write('Stalak za CD uspjesno otvoren dana ')
        f.write(datum)
        f.write(' u ')
        f.write(vrijeme)
        f.write('\n')
        f.close()

    elif userInput in facebook:
        print("Otvaram Facebook...")
        webbrowser.open('http://www.facebook.com/logout.php')
        f = open('C:/Users/Hrvoje/Desktop/log.txt', 'a')
        f.write('Facebook uspjesno otvoren dana ')
        f.write(datum)
        f.write(' u ')
        f.write(vrijeme)
        f.write('\n')
        f.close()

    elif userInput in google:
        print("Otvaram Google...")
        webbrowser.open('https://www.google.com')
        f = open('C:/Users/Hrvoje/Desktop/log.txt', 'a')
        f.write('Google uspjesno otvoren dana ')
        f.write(datum)
        f.write(' u ')
        f.write(vrijeme)
        f.write('\n')
        f.close()

    elif userInput in twitter:
        print("Otvaram Twitter...")
        webbrowser.open('https://twitter.com/')
        f = open('C:/Users/Hrvoje/Desktop/log.txt', 'a')
        f.write('Twitter uspjesno otvoren dana ')
        f.write(datum)
        f.write(' u ')
        f.write(vrijeme)
        f.write('\n')
        f.close()

    elif userInput in youtube:
        print("Otvaram Youtube...")
        webbrowser.open('https://youtube.com/')
        f = open('C:/Users/Hrvoje/Desktop/log.txt', 'a')
        f.write('Youtube uspjesno otvoren dana ')
        f.write(datum)
        f.write(' u ')
        f.write(vrijeme)
        f.write('\n')
        f.close()

    else:
        if count >= 2 and podjeljeno[0] == 'Podjeli':
            replaced = userInput.replace('Podjeli', '')
            podjeljeno = replaced.split()
            print(podjeljeno)

        elif count >= 2 and podjeljeno[0] == 'Google':
            replaced = userInput.replace('Google', '')
            f = open('C:/Users/Hrvoje/Desktop/log.txt', 'a')
            f.write('Uspjesno proguglano')
            f.write(replaced)
            f.write(' dana ')
            f.write(datum)
            f.write(' u ')
            f.write(vrijeme)
            f.write('\n')
            f.close()
            webbrowser.open("https://www.google.com/search?q={}".format(replaced))

        elif count == 2 and podjeljeno[0] == 'Open':  # opening a web adress
            replaced = userInput.replace('Open', '')
            webbrowser.open(replaced)

        else:
            webbrowser.open("https://www.google.com/search?q={}".format(userInput))
