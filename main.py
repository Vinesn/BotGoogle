import subprocess
API = subprocess.Popen(['runapi.bat'])
import setuplibs
import webbrowser
from sikulix4python import *
import pyautogui
import time
import pyperclip
from sql_grabber import *

def logIn(EMAIL, PASSWD, scr):
    try:
        print(f"Podjęto próbę zalogowania się na {G_emailIn}..." '\n')
        time.sleep(1)
        pyautogui.hotkey('alt', 'd')
        pyautogui.write("https://www.google.com/intl/pl_pl/business/"); pyautogui.press("enter")
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)
        if scr.exists("zarzad.png"):
            scr.click("zarzad.png")
        time.sleep(1)
        if scr.exists("history.png"):
            scr.click("history.png")
            time.sleep(1)
            if scr.exists("passwd.png"):
                scr.click("passwd.png")
                pyperclip.copy(PASSWD); pyautogui.hotkey('ctrl', 'v')
                pyautogui.press("enter")
        elif scr.exists("Kominkipl.png"):
            return
        else:
            if scr.exists("email.png"):
                scr.click("email.png")
                pyperclip.copy(EMAIL); pyautogui.hotkey('ctrl', 'v')
                pyautogui.press("enter")
            time.sleep(1)
            if scr.exists("passwd.png"):
                scr.click("passwd.png")
                pyperclip.copy(PASSWD); pyautogui.hotkey('ctrl', 'v')
                pyautogui.press("enter")
        
        print(f"Pomyślnie zalogowano na konto {EMAIL}!" '\n')
            
    except:
        input("Wystapil blad podczas logowania." '\n')

def PhotoSend(zdjpath, scr):
    try:
        print(f"Podjęto próbę dodania zdjęcia na strone firmy {G_emailIn}..." '\n')
        time.sleep(1)
        pyautogui.hotkey('alt', 'd')
        pyautogui.write("https://www.google.com/intl/pl_pl/business/"); pyautogui.press("enter")
        time.sleep(1)
        if scr.exists("zarzad.png"):
            scr.click("zarzad.png")
        time.sleep(5)
        time.sleep(2)
        if scr.exists("zdj.png"):
            scr.click("zdj.png")
        time.sleep(3)
        if scr.exists("dod.png"):
            scr.click("dod.png")
        time.sleep(1)
        if scr.exists("wybor.png"):
            scr.click("wybor.png")
        time.sleep(3)
        if scr.exists("plikpath.png"):
            scr.click("plikpath.png")
            pyautogui.keyDown("Ctrl")
            pyautogui.press("a")
            pyautogui.keyUp("Ctrl")
            pyperclip.copy(zdjpath); pyautogui.hotkey('ctrl', 'v')
            pyautogui.press("enter")
        time.sleep(5)
        if scr.exists("x.png"):
            scr.click("x.png")
            
        print(f"Pomyslnie upublikowano zdjecie: ({zdjpath})" '\n')

    except:
        input("Wystapil blad podczas wstawiania zdjecia." '\n')

def ItemSell(Nazwa_Produktu, Kategoria, Cena, Opis, Zdjeciepath, scr):
    try:
        print(f"Podjęto próbę dodania produktu na stronę firmy {G_emailIn}..." '\n')
        if not scr.exists("strona.png"):
            pyautogui.hotkey('alt', 'd')
            pyautogui.write("https://www.google.com/intl/pl_pl/business/"); pyautogui.press("enter")
            time.sleep(1)
            if scr.exists("zarzad.png"):
                scr.click("zarzad.png")
        time.sleep(3)
        if scr.exists("dodajprod.png"):
            scr.click("dodajprod.png")
        time.sleep(1)
        # PUSTA LISTA CZY NIE
        if scr.exists("rozpocz.png"):
            scr.click("rozpocz.png")
            time.sleep(5)
        elif scr.exists("dodajproduktnast.png"):
            scr.click("dodajproduktnast.png")
            time.sleep(5)
        #Wypełnianie Danych
        
        scr.click("nazwaprod.png"); pyperclip.copy(Nazwa_Produktu); pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        scr.click("kategoria.png")
        time.sleep(5)
        scr.click("createnew.png")
        scr.click("kategorianew.png"); pyperclip.copy(Kategoria); pyautogui.hotkey('ctrl', 'v')
        if not scr.exists("Cena.png"):
            pyautogui.scroll(-60)
        scr.click("Cena.png"); pyautogui.write(Cena)
        time.sleep(1)
        if not scr.exists("Opis.png"):
            pyautogui.scroll(-200)
        scr.click("opis.png"); pyperclip.copy(Opis); pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        if not scr.exists("itemphoto.png"):
            pyautogui.scroll(400)
            time.sleep(3)
        scr.click("itemphoto.png")
        time.sleep(1)
        if scr.exists("plikpath.png"):
            scr.click("plikpath.png")
            pyperclip.copy(Zdjeciepath); pyautogui.hotkey('ctrl', 'v')
            pyautogui.press("enter")
        time.sleep(5)
        scr.click("itempost.png")
        time.sleep(5)
        if scr.exists("x.png"):
            scr.click("x.png")

        print(f"Pomyślnie dodano produkt ({Nazwa_Produktu}) na strone firmy." '\n')
        
    except:
        input("Wystapil blad podczas dodawnaia towaru." '\n')
        

def G1(email, password, host, user, DBpassword, db, symbol):
    #Instalacja Bibliotek
    setuplibs.auto_install()
    
    reset()

    addImagePath(r".\Screens")
    webbrowser.open("https://google.com/")
    
    scr = Screen()
    
    # LOGOWANIE NA GOOGLE
    logIn(email, password, scr)

    # Odpalanie funkcji, pobierając dane z SQL
    all_items = InfoGrabber(host, user, DBpassword, db, symbol)

    for item in all_items:
        # DODANIE ZDJECIA NA PROFIL GOOGLE
        if item['Zdjecie'] != "BRAK WYMAGANEGO PARAMETRU: Zdjęcie":
            PhotoSend(item['Zdjecie'], scr)
        # DODANIE PRODUKTU NA PROFIL GOOGLE
        if item['Nazwa'] and item['Kategoria'] is not None and item['Zdjecie'] != "BRAK WYMAGANEGO PARAMETRU: Zdjęcie":
            ItemSell(
                item["Nazwa"],
                item["Kategoria"],
                str(item["CenaBrutto"]),
                item["Opis"],
                item['Zdjecie'], 
                scr
            )
        else:
            print("Nie wykryto produktów, które spełniają owych wymaganych parametrów: Nazwa, Cena, Opis, Zdjęcie")
            
    API.terminate()

symbolIn = input("Symbol: ") 
userIn = input("User: ")
passwordIn = input("Password: ")
hostIn = input("Host: ")
dbIn = input("Database: ")
G_emailIn = input("Google Email: ")
G_passwdIn = input("Google Password: ")

# Wywołanie G1 z odpowiednimi argumentami
G1(G_emailIn, G_passwdIn, hostIn, userIn, passwordIn, dbIn, symbolIn)
