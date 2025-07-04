from tkinter import *
import time
import ttkthemes
from tkinter import ttk, messagebox, filedialog
import pymysql
import pandas

def toplevel_data(title, button_text,command):
    global idEntry,phoneEntry,nameEntry,emailEntry,addressEntry,genderEntry,dobEntry,screen
    screen = Toplevel()
    screen.title(title)
    screen.grab_set()
    screen.resizable(False, False)
    idLabel = Label(screen, text='Id', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=30, pady=15)
    idEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    nameLabel = Label(screen, text='Name', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=30, pady=15)
    nameEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, pady=15, padx=1)

    phoneLabel = Label(screen, text='Phone', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=30, pady=15)
    phoneEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=2, column=1, pady=15, padx=1)

    emailLabel = Label(screen, text='Email', font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=3, column=0, padx=30, pady=15)
    emailEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    emailEntry.grid(row=3, column=1, pady=15, padx=1)

    addressLabel = Label(screen, text='Address', font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, padx=30, pady=15)
    addressEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    addressEntry.grid(row=4, column=1, pady=15, padx=1)

    genderLabel = Label(screen, text='Gender', font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, padx=30, pady=15)
    genderEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    genderEntry.grid(row=5, column=1, pady=15, padx=1)

    dobLabel = Label(screen, text='D.O.B', font=('times new roman', 20, 'bold'))
    dobLabel.grid(row=6, column=0, padx=30, pady=15)
    dobEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    dobEntry.grid(row=6, column=1, pady=15, padx=1)

    student_button = ttk.Button(screen, text=button_text, command=command)
    student_button.grid(row=7, columnspan=2)

    if title=='Update details':
        indexing = BankTable.focus()

        content = BankTable.item(indexing)
        listdata = content['values']
        idEntry.insert(0, listdata[0])
        nameEntry.insert(0, listdata[1])
        phoneEntry.insert(0, listdata[2])
        emailEntry.insert(0, listdata[3])
        addressEntry.insert(0, listdata[4])
        genderEntry.insert(0, listdata[5])
        dobEntry.insert(0, listdata[6])

def Exit():
    result=messagebox.askyesno('Confirm', 'Do you want to exit')
    if result:
        root.destroy()
    else:
        pass


def export_data():
    url=filedialog.asksaveasfilename(defaultextension='.csv')
    indexing=BankTable.get_children()
    newList=[]
    for index in indexing:
        content=BankTable.item(index)
        datlist=content['values']
        newList.append(datlist)

    table=pandas.DataFrame(newList, columns=['Id', 'Name', 'Mobile', 'Email', 'Address', 'Gender', 'D.O.B',' Add Date', 'Added Time' ])
    table.to_csv(url, index=False)
    messagebox.showinfo('Data Exported', 'Successfully data exported')



def update_data():
    query = 'update student set name=%s,mobile=%s,email=%s,address=%s,gender=%s,dob=%s,date=%s,time=%s where id=%s'
    mycursor.execute(query, (nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(),
                             genderEntry.get(), dobEntry.get(), date, currentTime, idEntry.get()))
    con.commit()
    messagebox.showinfo('Success', f'{idEntry.get()} is modified successfully')
    screen.destroy()
    show_data()



def show_data():
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    BankTable.delete(*BankTable.get_children())
    for data in fetched_data:
        BankTable.insert('', END, values=data)


def delete_data():
    indexing = BankTable.focus()
    print(indexing)
    content = BankTable.item(indexing)
    content_id = content['values'][0]
    query = 'delete from student where id=%s'
    mycursor.execute(query, content_id)
    con.commit()
    messagebox.showinfo('deleted', f'this{content_id} is deleted')
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    BankTable.delete(*BankTable.get_children())
    for data in fetched_data:
        BankTable.insert('', END, values=data)



def search_data():
    query = 'select * from student where id=%s or name=%s or email=%s or mobile=%s or address=%s or gender=%s or dob=%s'
    mycursor.execute(query, (idEntry.get(), nameEntry.get(), emailEntry.get(), phoneEntry.get(), addressEntry.get(), genderEntry.get(),dobEntry.get()))
    BankTable.delete(*BankTable.get_children())
    fetched_data = mycursor.fetchall()
    for data in fetched_data:
        BankTable.insert('', END, values=data)


def add_data():
    if idEntry.get() == '' or nameEntry.get() == '' or phoneEntry.get() == '' or emailEntry.get() == '' or addressEntry.get() == '' or genderEntry.get() == '' or dobEntry.get() == '':
        messagebox.showerror('Error', 'Fill all Details', parent=screen)

    else:
        try:
            query = 'insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(query,(idEntry.get(), nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(),
            genderEntry.get(), dobEntry.get(), date, currentTime))
            con.commit()
            result = messagebox.askyesno('Confirm', 'Data added successfully.do you want to clean the form?',parent=screen)
            if result:
                idEntry.delete(0, END)
                nameEntry.delete(0, END)
                phoneEntry.delete(0, END)
                emailEntry.delete(0, END)
                addressEntry.delete(0, END)
                genderEntry.delete(0, END)
                dobEntry.delete(0, END)
            else:
                pass
        except:
            messagebox.showerror('Error', 'Id cannot be replaced', parent=screen)
            return
        query = 'select *from student'
        mycursor.execute(query)
        fetched_data = mycursor.fetchall()
        BankTable.delete(*BankTable.get_children())
        for data in fetched_data:
            BankTable.insert('', END, values=data)

def connectDatabase():
    def connect():
        global mycursor, con
        try:
            con = pymysql.connect(host=hostEntry.get(), user=usernameEntry.get(), password=PasswordnameEntry.get())
            mycursor = con.cursor()

        except:
            messagebox.showerror('Error', 'Invalid', parent=connectWindow)
            return

        try:
            query = 'create database Bms'
            mycursor.execute(query)
            query = 'use Bms'
            mycursor.execute(query)
            query = 'create table student (id int not null primary key, name varchar(30), mobile varchar(10), email varchar(30),' \
                    'address varchar(100), gender varchar(20), dob varchar(20), date varchar(50), time varchar(50))'
            mycursor.execute(query)

        except:
            query = 'use Bms'
            mycursor.execute(query)
        messagebox.showinfo('Success', 'Database connection is successful', parent=connectWindow)
        connectWindow.destroy()
        addbankbutton.config(state=NORMAL)
        searchbankbutton.config(state=NORMAL)
        updatebankbutton.config(state=NORMAL)
        showbankbutton.config(state=NORMAL)
        deletebankbutton.config(state=NORMAL)
        exportbankbutton.config(state=NORMAL)

    connectWindow = Toplevel()
    connectWindow.geometry('570x250+930+230')
    connectWindow.title('Database Connection')
    connectWindow.resizable(False, False)

    hostnameLabel = Label(connectWindow, text='Host Name', font=('arial', 20, 'bold'))
    hostnameLabel.grid(row=0, column=0, padx=20)

    hostEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    hostEntry.grid(row=0, column=1, padx=40, pady=20)

    usernameLabel = Label(connectWindow, text='User Name', font=('arial', 20, 'bold'))
    usernameLabel.grid(row=1, column=0, padx=20)

    usernameEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    usernameEntry.grid(row=1, column=1, padx=40, pady=20)

    PasswordnameLabel = Label(connectWindow, text='Password Name', font=('arial', 20, 'bold'))
    PasswordnameLabel.grid(row=2, column=0, padx=20)

    PasswordnameEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    PasswordnameEntry.grid(row=2, column=1, padx=40, pady=20)

    connectButton = ttk.Button(connectWindow, text='CONNECT', command=connect)
    connectButton.grid(row=3, columnspan=2)


count = 0
text = ''


def slider():
    global text, count
    if count == len(s):
        count = 0
        text = ''
    text = text + s[count]
    sliderLabel.config(text=text)
    count += 1
    sliderLabel.after(300, slider)


def clock():
    global date, currentTime
    date = time.strftime('%d/%m/%y')
    currentTime = time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'  Date: {date}\n  Time: {currentTime}')
    datetimeLabel.after(1000, clock)


root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('clearlooks')

root.geometry('1474x750+0+0')
root.resizable(False, False)
root.title('Bank Management System')

datetimeLabel = Label(root, font=('times new roman', 18, 'bold'))
datetimeLabel.place(x=5, y=5)
clock()

s = 'Bank Management System'
sliderLabel = Label(root, font=('arial', 28, 'italic bold'), width=45)
sliderLabel.place(x=200, y=0)
slider()

connectButton = ttk.Button(root, text='Connect DataBase', command=connectDatabase)
connectButton.place(x=1290, y=0)

leftFrame = Frame(root)
leftFrame.place(x=50, y=90, width=350, height=750)

BmsImage = PhotoImage(file='bms.png')
BmsLabel = Label(leftFrame, image=BmsImage)
BmsLabel.grid(row=0, column=0)

addbankbutton = ttk.Button(leftFrame, text='Add details', width=35, state=DISABLED, command=lambda: toplevel_data('Add details', 'Add Employee', add_data))
addbankbutton.grid(row=1, column=0, pady=20)

searchbankbutton = ttk.Button(leftFrame, text='Search details', width=35, state=DISABLED, command=lambda: toplevel_data('Search details', 'Search Employee', search_data))
searchbankbutton.grid(row=2, column=0, pady=20)

deletebankbutton = ttk.Button(leftFrame, text='Delete details', width=35, state=DISABLED, command=delete_data)
deletebankbutton.grid(row=3, column=0, pady=20)

updatebankbutton = ttk.Button(leftFrame, text='Update details', width=35, state=DISABLED, command=lambda: toplevel_data('Update details', 'Update Employee', update_data))
updatebankbutton.grid(row=4, column=0, pady=20)

showbankbutton = ttk.Button(leftFrame, text='Show details', width=35, state=DISABLED, command=show_data)
showbankbutton.grid(row=5, column=0, pady=20)

exportbankbutton = ttk.Button(leftFrame, text='Export details', width=35, state=DISABLED, command=export_data)
exportbankbutton.grid(row=6, column=0, pady=20)

exitbankbutton = ttk.Button(leftFrame, text='Exit', width=35, command=Exit)
exitbankbutton.grid(row=7, column=0, pady=20)

rightFrame = Frame(root)
rightFrame.place(x=350, y=90, width=1130, height=660)

scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)

BankTable = ttk.Treeview(rightFrame, columns=('Id', 'Name', 'Mobile No', 'Email', 'Address', 'Gender', 'D.O.B',
                                              'Added Date', 'Added Time'), xscrollcommand=scrollBarX.set
                         , yscrollcommand=scrollBarY.set)

scrollBarX.config(command=BankTable.xview)
scrollBarY.config(command=BankTable.yview)

scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)

BankTable.pack(fill=BOTH, expand=1)

BankTable.heading('Id', text='Id')
BankTable.heading('Name', text='Name')
BankTable.heading('Mobile No', text='Mobile')
BankTable.heading('Email', text='Email Address')
BankTable.heading('Address', text='Address')
BankTable.heading('Gender', text='Gender')
BankTable.heading('D.O.B', text='D.O.B')
BankTable.heading('Added Date', text='Added Date')
BankTable.heading('Added Time', text='Added Time')

BankTable.column('Id', width=50, anchor=CENTER)
BankTable.column('Name', width=300, anchor=CENTER)
BankTable.column('Mobile No', width=300, anchor=CENTER)
BankTable.column('Email', width=200, anchor=CENTER)
BankTable.column('Address', width=300, anchor=CENTER)
BankTable.column('Gender', width=100, anchor=CENTER)
BankTable.column('D.O.B', width=100, anchor=CENTER)
BankTable.column('Added Date', width=200, anchor=CENTER)
BankTable.column('Added Time', width=200, anchor=CENTER)

style = ttk.Style()
style.configure('Treeview', rowheight=40, font=('arial', 12))
style.configure('Treeview.Heading', font=('arial', 14, 'bold'))

BankTable.config(show='headings')

root.mainloop()
