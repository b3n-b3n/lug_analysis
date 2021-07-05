import tkinter
import os

def show_table(dname):
    new_window = tkinter.Tk()
    new_window.title('curves1')
    img = tkinter.PhotoImage(master=new_window, file=os.path.join(dname, r'images/curve_materials1.png'))
    w = tkinter.Label(new_window, image=img)
    w.pack()
    new_window.mainloop()


def show_table2(dname):
    new_window2 = tkinter.Tk()
    new_window2.title('curves2')
    img = tkinter.PhotoImage(master=new_window2, file=os.path.join(dname, r'images/curve_materials2.png'))
    w = tkinter.Label(new_window2, image=img)
    w.pack()
    new_window2.mainloop()


def show_materials(dname):
    new_window3 = tkinter.Tk()
    new_window3.title('materials')
    img = tkinter.PhotoImage(master=new_window3, file=os.path.join(dname, r'images/material_data.png'))
    w = tkinter.Label(new_window3, image=img)
    w.pack()
    new_window3.mainloop()


def show_load_types(dname):
    new_window4 = tkinter.Tk()
    new_window4.title('load_types')
    img = tkinter.PhotoImage(master=new_window4, file=os.path.join(dname, r'images/druh_zatazenia2.png'))
    w = tkinter.Label(new_window4, image=img)
    w.pack()
    new_window4.mainloop()
    