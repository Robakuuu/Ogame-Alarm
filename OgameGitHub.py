from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs4
import os
import datetime
import sys
from guizero import App




def cls():
    os.system('cls' if os.name=='nt' else 'clear')








class Dane_logowania:
    email=""#Your Login to Ogame
    haslo=""#Your Password to Ogame
class userTrello:
    email=""#Your Login to Trello
    haslo=""#Your Password to Trello

browser=webdriver.Chrome(executable_path=r'C:\Users\UserX\PycharmProjects\Selenium\chromedriver.exe')#Your path to Chrome Driver
trello=webdriver.Chrome(executable_path=r'C:\Users\UserX\PycharmProjects\Selenium\chromedriver.exe')#Your path to Chrome Driver
browser.get('http://www.ogame.pl')
wiadomosc='PROBA'
tresc_ruchu=[]
text=""

def Logowanie_do_Ogame():
    try:
        items = browser.find_elements_by_tag_name("li")
        for item in items:
            text = item.text
            if item.text== "Login":
                LoginItem=item

        LoginItem.click()

        username = browser.find_element_by_name("email")
        username.clear()
        username.send_keys(Dane_logowania.email)

        password= browser.find_element_by_name("password")
        password.clear()
        password.send_keys(Dane_logowania.haslo)

        button_login= browser.find_element_by_class_name("button-lg")
        button_login.click()

        time.sleep(2)
        graj= browser.find_element_by_class_name("button-md")
        graj.click()

        time.sleep(2)
        graj2= browser.find_element_by_class_name("btn-primary")
        graj2.click()

        time.sleep(10)
        print("--------Zalogowano----------")
    except:
        print("Problem z zalogowaniem, zmien dane wejsciowe!")
        sys.exit()



def zamkniecie_karty():
    try:
        browser.switch_to.window(browser.window_handles[0])
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        print("--------Zamknieto Karte Wyboru Serwera----------")
    except:
        print("Problem z zamknieciem karty!")
        sys.exit()



def zapisHTML():
    html=bs4(browser.page_source,'html.parser')
    dozapisu=str(html)
    file = open("html.txt", "w")
    file.write(dozapisu)
    print("--------Utworzono HTML----------")


def szukaj_ataku():
    element=browser.find_element_by_id("attack_alert")
    przetlumaczona_lista=[]
    Informacja=element.get_attribute("class")
    print(datetime.datetime.now())
    if Informacja!="tooltip noAttack":
        print("!---Wykryto Flote---!")
        sprawdz_misje()
        przetlumaczona_lista=tresc_ruchu

        wiadomosc = str(datetime.datetime.now()) + '   RODZAJ RUCHU WROGIEJ FLOTY:'+ str(przetlumaczona_lista)
        Trello_notatki(wiadomosc)
    else:
        print("BRAK RUCHU WROGIEJ FLOTY")

    #3-transport
    #6-szpieguj
    #print(Informacja)


def otworz_trello():
    trello.get('http://www.trello.com')
    zaloguj=trello.find_element_by_xpath('//a[@href="/login"]')
    zaloguj.click()
def logowanie_trello():
    time.sleep(3)
    username = trello.find_element_by_name("user")
    username.clear()
    username.send_keys(userTrello.email)
    time.sleep(3)

    atlassian=trello.find_element_by_id("login")
    atlassian.click()
    time.sleep(3)
    atlassian = trello.find_element_by_id("login-submit")
    atlassian.click()
    time.sleep(3)

    password = trello.find_element_by_id("password")
    password.clear()
    password.send_keys(userTrello.haslo)
    time.sleep(3)

    atlassian = trello.find_element_by_id("login-submit")
    atlassian.click()
    time.sleep(15)
    print("----Zalogowano do Trello!-----")

    #button_login = trello.find_element_by_class_name("btn.success")
    #button_login.click()
def start_bota():

    czas_skanow = 60
    print("---SKAN URUCHOMIONY---")
    while True:
        browser.refresh()
        time.sleep(3)
        szukaj_ataku()
        time.sleep(czas_skanow)
def Trello_notatki(wiadomosc):
    wybranie_kafelka=trello.find_element_by_class_name('board-tile')
    wybranie_kafelka.click()
    time.sleep(5)
    wybranie_kafelka = trello.find_element_by_class_name('js-open-card-composer')
    wybranie_kafelka.click()
    time.sleep(5)
    wybranie_kafelka = trello.find_element_by_class_name('js-card-title')
    wybranie_kafelka.clear()
    wybranie_kafelka.send_keys(wiadomosc)
    time.sleep(5)
    wybranie_kafelka = trello.find_element_by_class_name('js-add-card')
    wybranie_kafelka.click()
    time.sleep(5)
    wybranie_kafelka=trello.find_element_by_name('house')
    wybranie_kafelka.click()
    time.sleep(5)



def sprawdz_misje():

    lista_misji=browser.find_elements_by_class_name('eventFleet')
    #print(lista_misji)
    for misja in lista_misji:
        tekst = misja.get_attribute("data-mission-type")
        #koordy = misja.find_element_by_class_name('coordsOrigin')

        tekst = [w.replace('1', '!ATAK!') for w in tekst]
        tekst = [w.replace('3', 'Transport') for w in tekst]
        tekst = [w.replace('6', 'Szpieguj') for w in tekst]


        koordy= misja.find_element_by_xpath("//td[@class='coordsOrigin']//a[@target='_top']").get_attribute("href")
        Galaxy=koordy.find('&galaxy')
        Galaxy+=8
        Numer_Galaktyki=koordy[Galaxy]
        System = koordy.find('&system')
        System += 8
        Numer_systemu = koordy[System::]
        print("Skad Atak-  "+Numer_Galaktyki+":"+Numer_systemu)





        tresc_ruchu.append(str(tekst)+" Galaktyka:"+Numer_Galaktyki+" System:"+Numer_systemu)
        #tresc_ruchu+tekst
def proba_logowania():
    zamknij_reklame()
    time.sleep(10)
    Logowanie_do_Ogame()
    zamkniecie_karty()
    otworz_trello()
    logowanie_trello()
    try:
        start_bota()
    except:
        proba_logowania()

def gui_run():
    app = App(title="Hello world")
    app.display()

def zamknij_reklame():
    time.sleep(5)
    try:
        reklama=browser.find_element_by_link_text('x')
        reklama.click()
    except:
        print("Nie ma reklamy")

#gui_run()
proba_logowania()

















