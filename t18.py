from tkinter import *
from threading import Thread
from tkinter import messagebox
from tkinter.messagebox import showinfo
import time
import ctypes

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
ancho, alto = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
xuno = ancho - 480

t=None
sec=None
root=Tk()
root.title("Timer")
root.iconbitmap('tiempo.ico')
root.geometry(f"480x140+{xuno}+0")
root.resizable(1,1)
respuesta = ''

root.bind('<<pop>>',lambda event=None: showinfo('Oh!','Time is over!'))

e1=StringVar()
e2=StringVar()

class Timer(Thread):
    over=False
    pause=False
    def __init__(self,func):
        Thread.__init__(self)
        self.func=func
        #self.setDaemon(True)
    def run(self):
        global t,root
        time.sleep(1)
        finish=False
        while not self.over and not finish:
            if not self.pause:
                finish=self.func()
            time.sleep(1)
        if finish:
            #root.focus_force()
            root.event_generate('<<pop>>',when='tail')
        t=None   


def show():
    global e1,e2,sec
    e1.set('%.2d'%(sec/60))
    e2.set('%.2d'%(sec%60))
def down():
    global sec
    if sec: 
        sec-=1;show()
        return False
    else: return True

def cd():
    global sec,t
    if t:t.cont();return
    sec=0
    try: sec=int(e1.get())*60
    except Exception:pass
    try: sec+=int(e2.get())
    except Exception:pass
    if not sec: return
    show()
    t=Timer(down)
    t.start()
    pass

en1 = Label(root, textvariable = e1, justify=RIGHT, width=2, fg="blue", font=("Helvetica", 100))
en2 = Label(root, textvariable = e2, justify=RIGHT, width=2, fg="blue", font=("Helvetica", 100))
lb = Label (root, width=2,text = ':', fg="blue", font=("Helvetica", 80))

en1.grid(row = 0 ,column = 0,)
lb .grid(row = 0 ,column = 1)
en2.grid(row = 0 ,column = 2)

e1.set(18)
cd()

root.mainloop ()