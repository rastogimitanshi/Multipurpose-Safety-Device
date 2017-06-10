from Tkinter import *
import time
root= Tk()
time1=''
clock= Label(root, font=('times',20,'bold'), bg='white')
clock.pack(fill=BOTH, expand=1)

def tick():
    global time1
    time2= time.strftime('%H:%M:%S')
    if time2!=time1:
        time1=time2
        clock.config(text=time2)
    clock.after(200, tick)

tick()
root.mainloop()
