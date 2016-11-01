from threading import Timer
from tkinter import *
from tkinter import simpledialog
from functools import partial
import subprocess




class NumPad():
    def __init__(self, master):
        self.beweeg = 0
        self.master = master
        status = self.leesStatus()
        aanuit = StringVar()
        if status == 1:
            aanuit.set("Het systeem in ingeschakeld")
        else:
            aanuit.set("Het systeem in uitgeschakeld")
        self.tien = NONE
        entryFrame = LabelFrame(master, text="Entry Frame", bd=3)
        entryFrame.pack(padx=15, pady=10)

        self.tekstvar = StringVar(value="Voer uw alarm code in!")
        self.tekst = Label(entryFrame, font=('Courier',14), textvariable=self.tekstvar, width=60).pack()

        self.tekstvar2 = StringVar(value=aanuit.get())
        self.tekst2 = Label(entryFrame, font=('Courier',14), textvariable=self.tekstvar2, width=60).pack()

        self.entrybox = StringVar()
        self.inputBox = Entry(entryFrame, font=('Courier',20),textvariable=self.entrybox, width=38).pack()

        self.moveButton = Button(entryFrame,bg="black", fg="white", text="!!!!", width=3, font=('Courier',20), command=self.beweging).pack()

        kp = LabelFrame(master, text="Keypad", bd=3)
        kp.pack(padx=15, pady=10, side=BOTTOM)
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
            self.btn[n] = Button(kp,bg="black", fg="white", text=label, width=12, height=6, font=('Courier',20), command=cmd)
            self.btn[9] = Button(kp,bg="red", fg="white", text=label, width=12, height=6, font=('Courier',20), command=self.printen)
            self.btn[11] = Button(kp,bg="red", fg="white", text=label, width=12, height=6, font=('Courier',20), command=self.clear)
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
                self.tekstvar.set('Voer de alarmcode in om systeem uit te schakelen!')
                self.tekstvar2.set("Het systeem is ingeschakeld!")
                self.writeStatus('1')
                self.clear()
            else:
                self.master.after_cancel(self.tien)
                self.tekstvar.set('Voer de alarmcode in om het alarm in te schakelen!')
                self.tekstvar2.set("Het systeem is uitgeschakeld!")         #niet echt nodig
                self.writeStatus('0')
                self.clear()
        elif nu == "5678":
            if status == 0:
                self.master.after_cancel(self.tien)
                self.tekstvar2.set("STIL ALARM")
                self.clear()
            else:
                self.master.after_cancel(self.tien)
                self.tekstvar2.set("STIL ALARM")
                self.clear()

    def beweging(self):
        self.beweeg = 1
        print("Er beweegt iets!")
        status = self.leesStatus()
        if status == 1:
                self.tien = self.master.after(10000,self.alarmAf)                                            #Start de timer van 10 seconden om de alarmcode in te voeren
                self.tekstvar2.set('Voer binnen 10 seconden de alarmcode in!')

    def alarmAf(self):
        self.tekstvar2.set('HET ALARM GAAT AF! Politie onderweg!')         #Bericht naar andere PI als zijnde Politie?
        self.tekstvar.set('Voer de alarmcode in om het alarm uit te zetten!')
    def printen(self):
        new = login()


class login(simpledialog.Dialog):
    def __init__(self):
        print('Hello')
        self.toggleKeyboard()
        #self.createWidgets()
    def toggleKeyboard(self):
        p = subprocess.Popen(['florence show'], shell=True, stdout= subprocess.PIPE, stderr= subprocess.PIPE, universal_newlines=True)
        if not "" == p.stderr.readline():
            subprocess.Popen(['florence'], shell=True)


root = Tk()
numpad = NumPad(root)
root.mainloop()
