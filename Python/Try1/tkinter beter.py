from threading import Timer
from tkinter import *


class NumPad():
    def __init__(self, master):
        self.loopt = False
        self.master = master
        self.master.title("Alarm Systeem")
        self.tien = NONE
        self.status = self.leesStatus()
        self.fontToetsen = ('Courier',16)
        self.fontTekst = ('Courier',12)
        self.createFrames()
    def createFrames(self):
        frame = Frame(self.master)
        frame.pack(padx=15, pady=7)

        aanuit = StringVar()
        aanuit2 = StringVar()
        if self.status == 1:
            aanuit.set("Het systeem is ingeschakeld!")
            aanuit2.set("Voer de alarmcode in om het systeem uit te schakelen!")
        else:
            aanuit.set("Het systeem is uitgeschakeld!")
            aanuit2.set("Voer de alarmcode in om het systeem in te schakelen!")
        self.tekstvar = StringVar(value=aanuit.get())
        self.tekst = Label(frame, font=self.fontTekst, textvariable=self.tekstvar).pack(fill=X)

        self.tekstvar2 = StringVar(value=aanuit2.get())
        self.tekst2 = Label(frame, font=self.fontTekst, textvariable=self.tekstvar2).pack(fill=X)

        self.entrybox = StringVar()
        self.inputBox = Entry(frame, font=('Courier',16),textvariable=self.entrybox).pack(padx=14,fill=X)

        self.moveButton = Button(frame,bg="red", fg="white", text="!!!TRIGGER!!!", width=7, font=self.fontTekst, command=self.beweging).pack()

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
            self.btn[n] = Button(kp,bg="black", fg="white", text=label, width=12, height=6, font=self.fontToetsen, command=cmd)
            self.btn[9] = Button(kp,bg="red", fg="white", text=label, width=12, height=6, font=self.fontToetsen, command=inloggen)
            self.btn[11] = Button(kp,bg="red", fg="white", text=label, width=12, height=6, font=self.fontToetsen, command=self.clear)
            self.btn[n].grid(row=r, column=c)
            n+=1
            c+=1
            if c > 2:
                c = 0
                r +=1

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
                self.tekstvar2.set('Voer de alarmcode in om het systeem in te schakelen!')
                self.tekstvar.set("Het systeem is uitgeschakeld!")
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
        print("Er beweegt iets!")
        status = self.leesStatus()
        if status == 1 and self.loopt == False:
            self.loopt = True
            self.tien = self.master.after(10000,self.alarmAf)
            self.countdown(10)

    def alarmAf(self):
        self.tekstvar.set('HET ALARM GAAT AF! Politie onderweg!')         #Bericht naar andere PI als zijnde Politie?
        self.tekstvar2.set('Voer de alarmcode in om het alarm uit te zetten!')

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
        self.writeStatus('1')
        self.loopt = False
    def login(self):
        print("Inloggen")

class inloggen():
    def __init__(self):
        print("Inloggen")


root = Tk()
numpad = NumPad(root)
root.mainloop()
