from tkinter import *
from tkinter import ttk, messagebox
from db import Database

# ایجاد پنجره اصلی
win = Tk()
win.title("Contact")
win.geometry('800x400')
win.resizable(0, 0)
win.configure(bg='#007e1b')
db = Database('contacts.db')
selected_item = None

# توابع برنامه
def populate_list():
    print("Fetch button clicked!")  
    contact_list.delete(0, END)
    for row in db.fetch():
        contact_list.insert(END, row)

def clear_text():
    name_entry.delete(0, END)
    family_entry.delete(0, END)
    address_entry.delete(0, END)
    phone_entry.delete(0, END)
    name_entry.focus_set()

def add_item():
    if name_text.get() == "" or family_text.get() == "" or address_text.get() == "":
        messagebox.showerror('خطا', 'تمام فیلدها باید پر شوند!')
        return
    db.insert(name_text.get(), family_text.get(), address_text.get(), phone_text.get())
    clear_text()
    

def remove_item():
    global selected_item
    if selected_item is None:
        messagebox.showerror("خطا", "لطفاً یک مخاطب را انتخاب کنید!")
        return
    db.remove(selected_item[0])
    selected_item = None
    clear_text()
    

def select_item(event):
    global selected_item
    try:
        index = contact_list.curselection()
        if not index:
            return
        selected_item = contact_list.get(index[0])
        name_entry.delete(0, END)
        name_entry.insert(END, selected_item[1])
        family_entry.delete(0, END)
        family_entry.insert(END, selected_item[2])
        address_entry.delete(0, END)
        address_entry.insert(END, selected_item[3])
        phone_entry.delete(0, END)
        phone_entry.insert(END, selected_item[4])
    except IndexError:
        pass

def update_item():
    global selected_item
    if selected_item is None:
        messagebox.showerror("خطا", "لطفاً یک مخاطب را انتخاب کنید!")
        return
    db.update(selected_item[0], name_text.get(), family_text.get(), address_text.get(), phone_text.get())
    selected_item = None
    

def search_item():
    contact_list.delete(0, END)
    for row in db.search(search_text.get()):
        contact_list.insert(END, row)
    search_entry.delete(0, END)

def cancel():

    win.destroy()


name_text = StringVar()
Label(win, text="Name:",bg=('#007e1b') ,font=('Tahoma', 14)).place(x=10, y=5)
name_entry = Entry(win, textvariable=name_text, bd=3, relief=GROOVE)
name_entry.place(x=90, y=10)

family_text = StringVar()
Label(win, text="Family:",bg=('#007e1b'), font=('Tahoma', 14)).place(x=10, y=35)
family_entry = Entry(win, textvariable=family_text, bd=3, relief=GROOVE)
family_entry.place(x=90, y=35)

address_text = StringVar()
Label(win, text="Address:",bg=('#007e1b'), font=('Tahoma', 14)).place(x=275, y=5)
address_entry = Entry(win, textvariable=address_text, bd=3, relief=GROOVE)
address_entry.place(x=360, y=5)

phone_text = StringVar()
Label(win, text="Phone:",bg=('#007e1b'), font=('Tahoma', 14)).place(x=275, y=35)
phone_entry = Entry(win, textvariable=phone_text, bd=3, relief=GROOVE)
phone_entry.place(x=360, y=35)

fetch_btn=Button(win,text='fetch',command=populate_list,width=18 ,bg="#bababa")
fetch_btn.place(x=650,y=90)


# دکمه‌ها
Button(win, text="Insert", width=18,bg="#bababa", command=add_item ).place(x=500, y=20)
Button(win, text="Delete",  width=18,bg="#bababa", command=remove_item).place(x=500, y=55)
Button(win, text="Update",  width=18,bg="#bababa", command=update_item).place(x=650, y=20)
Button(win, text="Clear Inputs", width=18,bg="#bababa", command=clear_text).place(x=650, y=55)
Button(win, text="Cancel", width=18,bg="#bababa", command=cancel).place(x=500, y=90)

contact_list = Listbox(win, height=10, width=120, bd=3)
contact_list.place(x=10, y=180)
contact_list.bind('<<ListboxSelect>>', select_item)

scrollbar = Scrollbar(win)
scrollbar.place(x=750, y=180, height=165)
contact_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=contact_list.yview)

# جستجو
search_text = StringVar()
search_entry = Entry(win, textvariable=search_text, bd=3, relief=GROOVE)
search_entry.place(x=275, y=100)
Button(win, text="Search", width=18, command=search_item,bg="#bababa").place(x=120, y=100)

win.mainloop()