from tkinter import *

def main():
    root = Tk()
    numpad = NumPad(root)
    root.mainloop()

btn_list = [
    '1',  '2',  '3',
    '4',  '5',  '6',
    '7',  '8',  '9',
    'Log in',  '0',  '#',]


class NumPad(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.grid()
        self.numpad_create()

    def numpad_create(self):
        r = 1
        c = 0
        for b in btn_list:
            cmd=
            self.b= Button(self, text=b,width=5,command=cmd).grid(row=r,column=c)
            print(b)
            c += 1
            if c > 2:
                c = 0
                r += 1

main()
