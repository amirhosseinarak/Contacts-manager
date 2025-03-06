from tkinter import *
from tkinter import messagebox
import sqlite3
import os

# مسیر ذخیره دیتابیس در دسکتاپ
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
db_path = os.path.join(desktop_path, "project.db")

# ایجاد دیتابیس و جدول جدید در دسکتاپ
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fname TEXT NOT NULL,
    lname TEXT NOT NULL,
    course TEXT,
    password TEXT NOT NULL
)
""")
conn.commit()


counter = 1
def reset_counter():
    global counter
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    if not data:  
        counter = 1  
    else:
        counter = 1  


def add_entry():
    global counter
    if fname_var.get() and lname_var.get() and password_var.get():
        cursor.execute("INSERT INTO students (fname, lname, course, password) VALUES (?, ?, ?, ?)",
                       (fname_var.get(), lname_var.get(), course_var.get(), password_var.get()))
        conn.commit()
        show_entries()
        clear_fields()
    else:
        messagebox.showwarning("error", "pls enter fname lname password.")

# تابع نمایش اطلاعات
def show_entries():
    global counter
    listbox.delete(0, END)
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()

    reset_counter()  # استفاده از تابع برای بازنشانی شمارنده

    for row in data:
        listbox.insert(END, f"{counter} - {row[0]} - {row[1]} {row[2]} - {row[3]}")
        counter += 1  # شمارنده برای هر رکورد افزایش می‌یابد

# تابع حذف اطلاعات انتخاب‌شده
def delete_entry():
    global counter
    try:
        selected = listbox.get(ACTIVE)
        if selected:
            # جدا کردن ID از رکورد انتخاب‌شده
            student_id = selected.split(" - ")[1]
            cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
            conn.commit()

            reset_counter()  # بازنشانی شمارنده بعد از حذف رکورد

            show_entries()
        else:
            messagebox.showwarning("error", "pls choose somthing.")
    except Exception as e:
        messagebox.showerror("error", f"somthing is incorect: {str(e)}")

# تابع خالی کردن ورودی‌ها
def clear_fields():
    fname_var.set("")
    lname_var.set("")
    course_var.set("")
    password_var.set("")

# تابع ورود به سامانه
def login():
    cursor.execute("SELECT * FROM students WHERE password=?", (login_var.get(),))
    user = cursor.fetchone()
    if user:
        messagebox.showinfo("sign in succsesfull", f"welcome {user[1]} {user[2]}!")
    else:
        messagebox.showerror("error", "password is incorect.")

# تابع خروج از برنامه
def exit_program():
    Win.destroy()

# طراحی رابط کاربری
Win= Tk()
Win.title("ثبت نام اموزشگاه")
Win.geometry("830x550+400+110")
Win.configure(bg='#474fbf')


# فیلدهای ورود اطلاعات
Label(Win, text="نام :",bg='#474fbf',fg='black',font= ' ralewey 12 bold').place(x=40,y=20)
Label(Win, text="نام خانوادگی :",bg='#474fbf',fg='black',font= ' ralewey 12 bold').place(x=40,y=70)
Label(Win, text="نام دوره :",bg='#474fbf',fg='black',font= ' ralewey 12 bold').place(x=450,y=20)
Label(Win, text="رمز ورود :",bg='#474fbf',fg='black',font= ' ralewey 12 bold').place(x=450,y=75)

fname_var = StringVar()
lname_var = StringVar()
course_var = StringVar()
password_var = StringVar()
login_var = StringVar()

Entry(Win, textvariable=fname_var,bg='#5e63b3',fg='black',font= ' ralewey 12 bold').place(x=150,y=20)
Entry(Win, textvariable=lname_var,bg='#5e63b3',fg='black',font= ' ralewey 12 bold').place(x=150,y=75)
Entry(Win, textvariable=course_var,bg='#5e63b3',fg='black',font= ' ralewey 12 bold').place(x=550,y=20)
Entry(Win, textvariable=password_var, show="*",bg='#5e63b3',fg='black',font= ' ralewey 12 bold').place(x=550,y=75)
# لیست‌باکس برای نمایش کاربران
listbox = Listbox(Win, width=50,height=15,bg='#5e63b3',fg='black',font= ' ralewey 12 bold')
listbox.place(x=50,y=150)

# دکمه‌ها
Button(Win, text="مشاهده همه", width=20, command=show_entries,bg='black',fg='#474fbf',font= ' ralewey 12 bold').place(x=580,y=140)
Button(Win, text="اضافه کردن", width=20, command=add_entry,bg='black',fg='#474fbf',font= ' ralewey 12 bold').place(x=580,y=170)
Button(Win, text="خالی کردن ورودیها", width=20, command=clear_fields,bg='black',fg='#474fbf',font= ' ralewey 12 bold').place(x=580,y=200)
Button(Win, text="حذف کردن", width=20, command=delete_entry,bg='black',fg='#474fbf',font= ' ralewey 12 bold').place(x=580,y=230)
Button(Win, text="خروج", width=20, command=exit_program,bg='black',fg='#474fbf',font= ' ralewey 12 bold').place(x=580,y=260)

# ورود به سامانه
Label(Win, text="رمز ورود را وارد کنید :",bg='#474fbf',fg='black',font= ' ralewey 12 bold').place(x=50,y=470)
Entry(Win, textvariable=login_var,width=28, show="*",bg='#5e63b3',fg='black',font= ' ralewey 12 bold').place(x=250,y=470)
Button(Win, text="ورود به سامانه",width=20, command=login,bg='black',fg='#474fbf',font= ' ralewey 12 bold').place(x=580,y=290)


Win.mainloop()