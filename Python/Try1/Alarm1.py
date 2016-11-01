from threading import Timer
import time
import csv

def ingeschakeld():
    t = Timer(10.0, alarmAf)                                #Creeert een timer die na 10 seconden de functie alarmAf() uitvoert.
    t.start()                                               #Start de timer van 10 seconden om de alarmcode in te voeren
    while True:
        code = int(input('Voer binnen 10 seconden de alarmcode in!'))
        if code == 1234:
            t.cancel()                                      #Stopt de timer
            print('Systeem uitgeschakeld!')
            writeStatus('0')
            break
        elif code == 5678:
            t.cancel()                                      #Stopt de timer
            stilAlarm()                                     #Het stille alarm gaat af en de politie wordt op de hoogte gesteld.
            writeStatus('0')                                #Zet het systeem uit (0) in status.txt
            break
        else:
            print('Foutieve alarmcode ingevoerd!')

def uitgeschakeld():
    while True:
                loginKnop = int(input('Loginknop ingedrukt?'))
                if loginKnop == 1:                          #Als de loginknop wordt ingedrukt naar het loginvenster
                    login()
                    break
                else:
                    while True:
                        code = int(input('Voer de alarmcode in om het systeem in te schakelen!'))
                        if code == 1234:
                            print('Het systeem wordt ingeschakeld!\nVerlaat binnen 10 seconden het pand!')
                            time.sleep(10)                  #Als de juiste alarmcode is ingevoerd de bewoner 10 seconden de tijd geven om het pand te verlaten
                            writeStatus('1')                #Zet het systeem aan (1) in status.txt
                            break
                        elif code == 5678:
                            stilAlarm()                     #Laat het stille alarm af gaan als de stil code wordt ingevoert, zelfs al staat het systeem uit.
                            break
                        else:
                            print('Foutieve alarmcode ingevoerd!')
                    break

def login():                                                #Inlogfunctie
    wwen = []
    gebruikers = []
    with open('gebruikers.csv','r') as file:
        lees =  csv.reader(file, delimiter=';')
        for rij in lees:
            wwen.append(rij[1])
            gebruikers.append(rij[0])
    while True:
        gebruiker = input('Geef uw gebruikersnaam op: ')
        ww = input('Geef uw wachtwoord op: ')
        if gebruiker in gebruikers and ww in wwen:
            print('U kunt nu uw gegevens veranderen')
            opties()
            break
        elif user == 'stop' or ww == 'stop':
            print('Gestopt')
            break
        else:
            print('Foute gebruikersnaam en/of wachtwoord!')

def opties():                                               #Opties voor het veranderen van het alarm na inloggen
    while True:
        keuze = int(input('0: Uitloggen.\n1: Alarm licht veranderen.\n2: Verander alarmcode.\n3: Verander stille code.\nGeef uw keuze op: '))
        if keuze == 0:
            print('Uitgelogd!')
            break
        elif keuze == 1:
            print('Veranderd alarm licht!')
        elif keuze == 2:
            print('Verander alarm code!')
        elif keuze == 3:
            print('Verander stille code!')
        else:
            print('Geen geldige keuze!')

def leesStatus():                                           #Leest het status.txt bestand
    with open("status.txt",'r') as file:
        status = int(file.read(1))
        return status

def writeStatus(a):                                         #Schrijft het status.txt bestand
    with open("status.txt",'w') as file:
        file.write(a)

def alarmAf():
    print('\nHET ALARM GAAT AF! Politie onderweg!')         #Bericht naar andere PI als zijnde Politie?
    print('Voer de alarmcode in om het alarm uit te zetten!')

def stilAlarm():                                            #Stil alarm (overval bij juwelier, bank, etc) voor het op de hoogte stellen van de politie, zonder dat het alarm echt af gaat.
    print('STIL ALARM!. Politie is onderweg!')              #Bericht naar andere PI als zijnde Politie?

while True:
    beweging = int(input('Is er een beweging?'))            #Beweegt er een raam/deur?
    if beweging == 1:                                       #Staat het systeem aan of uit?
        status = leesStatus()
        if status == 1:
            print('Het alarm systeem staat aan!')
            ingeschakeld()
        elif status == 0:
            print('Het alarm systeem staat uit!')
            uitgeschakeld()

