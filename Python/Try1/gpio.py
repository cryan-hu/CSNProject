from threading import Timer
from tkinter import *
from tkinter import simpledialog
import csv
import RPi.GPIO as io




class NumPad():
    def __init__(self, master):
        self.loopt = False
        self.master = master

        self.tien = NONE
        self.knipper = NONE
        self.knipper2 = NONE
        self.status = self.leesStatus()
        self.fontToetsen = ('Courier',16)
        self.fontTekst = ('Courier',12)
        self.wwen = []
        self.gebruikers = []
        self.snelheid = IntVar()
        self.groen_pin = 27
        self.rood_pin = 22
        self.deur_pin = 17
        io.setwarnings(False)
        io.setmode(io.BCM)
        io.setup(self.groen_pin, io.OUT)
        io.setup(self.rood_pin, io.OUT)                     
        io.setup(self.deur_pin, io.IN, pull_up_down=io.PUD_UP)  # activate input with PullUp

        

        self.master.title("Alarm Systeem")
        self.leesCsv()
        self.check_deur()
        self.createFrames()
    def createFrames(self):
        frame = Frame(self.master)
        frame.pack(padx=15, pady=7)

        aanuit = StringVar()
        aanuit2 = StringVar()
        if self.status == 1:
            aanuit.set("Het systeem is ingeschakeld!")
            aanuit2.set("Voer de alarmcode in om het systeem uit te schakelen!")
            io.output(self.groen_pin, False)
        else:
            aanuit.set("Het systeem is uitgeschakeld!")
            aanuit2.set("Voer de alarmcode in om het systeem in te schakelen!")
            io.output(self.groen_pin, True)
        self.tekstvar = StringVar(value=aanuit.get())
        self.tekst = Label(frame, font=self.fontTekst, textvariable=self.tekstvar).pack(fill=X)

        self.tekstvar2 = StringVar(value=aanuit2.get())
        self.tekst2 = Label(frame, font=self.fontTekst, textvariable=self.tekstvar2).pack(fill=X)

        self.entrybox = StringVar()
        self.inputBox = Entry(frame, font=('Courier',16),textvariable=self.entrybox).pack(padx=14,fill=X)

        #self.moveButton = Button(frame,bg="red", fg="white", text="!!!TRIGGER!!!", width=7, font=self.fontTekst, command=self.beweging).pack()

        kp = Frame(frame, bd=3)
        kp.pack(side=BOTTOM)
        btn_list = [
        '1',  '2',  '3',
        '4',  '5',  '6',
        '7',  '8',  '9',
        'Log in',  '0',  'Correctie',]
        r = 1
        c = 0
        n= 0
        self.btn = list(range(len(btn_list)))
        for label in btn_list:
            cmd = lambda x = label: self.enter(x)
            self.btn[n] = Button(kp,bg="black", fg="white", text=label, width=8, height=4, font=self.fontToetsen, command=cmd)
            self.btn[9] = Button(kp,bg="red", fg="white", text=label, width=8, height=4, font=self.fontToetsen, command=self.inloggen)
            self.btn[11] = Button(kp,bg="red", fg="white", text=label, width=8, height=4, font=self.fontToetsen, command=self.clear)
            self.btn[n].grid(row=r, column=c)
            n+=1
            c+=1
            if c > 2:
                c = 0
                r +=1
    def check_deur(self):
        if io.input(self.deur_pin) == False:
            self.beweging()
        root.after(1000,self.check_deur)

    def leesStatus(self):                                           #Leest het status.txt bestand
        with open("status.txt",'r') as file:
            status = int(file.read(1))
            return status

    def writeStatus(self,a):                                         #Schrijft het status.txt bestand
        with open("status.txt",'w') as file:
            file.write(a)

    def clear(self):
        self.entrybox.set("")

    def enter(self,getal):
        nu = self.entrybox.get()
        self.entrybox.set(nu+getal)
        nu = self.entrybox.get()
        status = self.leesStatus()
        if nu == '1234':
            if status == 0:
                if self.loopt == False:
                    self.tekstvar.set('Het systeem wordt ingeschakeld!')
                    self.loopt = True
                    self.clear()
                    self.tien = self.master.after(10000,self.schakelIn)
                    self.countdown2(10)
            else:
                self.loopt = False
                self.master.after_cancel(self.tien)
                root.after_cancel(self.knipper)
                root.after_cancel(self.knipper2)
                self.tekstvar2.set('Voer de alarmcode in om het systeem in te schakelen!')
                self.tekstvar.set("Het systeem is uitgeschakeld!")
                io.output(self.groen_pin, True)
                io.output(self.rood_pin,False)
                self.writeStatus('0')
                self.clear()

    '''        elif nu == "5678":                               ##### Voor stil alarm naar andere pi
            self.loopt = False
            if status == 0:
                self.master.after_cancel(self.tien)
                self.tekstvar2.set("STIL ALARM")
                self.clear()
            else:
                self.master.after_cancel(self.tien)
                self.tekstvar2.set("STIL ALARM")
                self.clear()
    '''

    def beweging(self):
        status = self.leesStatus()
        if status == 1 and self.loopt == False:
            self.loopt = True
            self.tien = self.master.after(10000,self.alarmAf)
            self.countdown(10)

    def alarmAf(self):
        self.tekstvar.set('HET ALARM GAAT AF! Politie onderweg!')         #Bericht naar andere PI als zijnde Politie?
        self.tekstvar2.set('Voer de alarmcode in om het alarm uit te zetten!')
        root.after_cancel(self.knipper2)
        self.rood_snel_aan()

    def countdown(self, count):
        if count > 0 and self.loopt == True:
            self.tekstvar2.set('Voer binnen {} seconden de alarmcode in!'.format(count))
            self.master.after(1000, self.countdown, count-1)

    def countdown2(self, count):
        if count > 0 and self.loopt == True:
            self.tekstvar2.set('U heeft nog {} seconden om het pand te verlaten!'.format(count))
            self.master.after(1000, self.countdown2, count-1)

    def schakelIn(self):
        self.tekstvar2.set('Voer de alarmcode in om het systeem uit te schakelen!')
        self.tekstvar.set("Het systeem is ingeschakeld!")
        self.rood_slow_aan()
        io.output(self.groen_pin, False)
        self.writeStatus('1')
        self.loopt = False
        
    def rood_slow_aan(self):
        io.output(self.rood_pin,True)
        self.knipper2 = root.after(1000,self.rood_slow_uit)

    def rood_slow_uit(self):
        io.output(self.rood_pin,False)
        self.knipper2 = root.after(5000,self.rood_slow_aan)

    def rood_snel_aan(self):
        io.output(self.rood_pin,True)
        self.knipper = root.after(250,self.rood_snel_uit)

    def rood_snel_uit(self):
        io.output(self.rood_pin,False)
        self.knipper = root.after(250,self.rood_snel_aan)
        
        
        

    def inloggen(self):
        self.loginVenster = Toplevel()
        self.loginLabel = StringVar(value="Log in om alarminstellingen te veranderen")
        label1 = Label(self.loginVenster, textvariable=self.loginLabel).grid(row=0,columnspan=2)
        label2 = Label(self.loginVenster, text="Gebruiker:").grid(row=1,column=0)
        self.gebruikerVar = StringVar(value="jorrit")
        entry1 =Entry(self.loginVenster, textvariable=self.gebruikerVar).grid(row=1,column=1)
        label2 = Label(self.loginVenster, text="Wachtwoord:").grid(row=2,column=0)
        self.wwVar = StringVar(value="pizza")
        entry2 =Entry(self.loginVenster,show="*", textvariable=self.wwVar).grid(row=2,column=1)
        button1 = Button(self.loginVenster,text="Log in", command=self.verifieer).grid(row=3,columnspan=2)

    def verifieer(self):
        if self.gebruikerVar.get() in self.gebruikers and self.wwVar.get() == self.wwen[self.gebruikers.index(self.gebruikerVar.get())]:
            self.ingelogd()
        else:
            self.loginLabel.set("Verkeerd wachtwoord en/of gebruikersnaam!")

    def ingelogd(self):
            print("Gebruiker {} succesvol ingelogt!".format(self.gebruikerVar.get()))
            self.master.withdraw()
            self.loginVenster.destroy()
            self.veranderVenster = Toplevel()
            self.veranderVenster.geometry("400x400")
            self.createVerander()

    def createVerander(self):
        testalarm = Button(self.veranderVenster,text="Test Alarm", width=10, height=3).grid(row=0,column=0)
        verander1 = Button(self.veranderVenster,text="Verander1", width=10, height=3).grid(row=0,column=1)
        verander2 = Button(self.veranderVenster,text="Verander2", width=10, height=3).grid(row=0,column=2)
        SNELHEID = [
            ("Langzaam", "1"),
            ("Normaal", "2"),
            ("Snel", "3"),
        ]
        i = 0
        b = list(range(len(SNELHEID)))
        for text, mode in SNELHEID:
            b[i] = Radiobutton(self.veranderVenster, text=text,variable=self.snelheid, value=mode, width=10, height=3)
            b[i].grid(row=1,column=i)
            i += 1
        Radiobutton.select(b[1])
        terug = Button(self.veranderVenster,text="Terug", command=self.terug).grid(columnspan=3)

    def terug(self):
        selected = self.snelheid.get()
        if selected == 1:
            print("Radiobutton {} geselecteerd".format(selected)) #sla de geselecteerde knop op
        elif selected == 2:
            print("Radiobutton {} geselecteerd".format(selected))
        elif selected == 3:
            print("Radiobutton {} geselecteerd".format(selected))
        print("Instellingen opgeslagen")
        self.veranderVenster.destroy()
        self.master.update()
        self.master.deiconify()

    def leesCsv(self):
        with open('gebruikers.csv','r') as file:
            lees =  csv.reader(file, delimiter=';')
            for rij in lees:
                self.wwen.append(rij[1])
                self.gebruikers.append(rij[0])


root = Tk()
root.geometry("800x480")
numpad = NumPad(root)
root.mainloop()
