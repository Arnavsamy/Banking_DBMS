from tkinter import*
from tkinter import messagebox
from PIL import ImageTk

def login():
    if usernameEntry.get()=='' or passwordEntry.get()=='':
        messagebox.showerror('Error','Please Enter Details')
    elif usernameEntry.get()=='Arnav' and passwordEntry.get()=='4321':
        messagebox.showinfo('Success', 'Welcome')
        window.destroy()
        import bms
    else:
        messagebox.showerror('Error', 'Please enter correct details')



window = Tk()
window.geometry('1280x700+0+0')
window.title('Bank Login')
window.resizable(False,False)


backgroundImage=ImageTk.PhotoImage(file='whitebg.jpg')
bgLabel=Label(window,image=backgroundImage)
bgLabel.place(x=0, y=0)

loginFrame=Frame(window)
loginFrame.place(x=400, y=150)
logoImage=PhotoImage(file='bank-building.png')

logoLabel=Label(loginFrame,image=logoImage)
logoLabel.grid(row=0, column=0, columnspan=2, pady=10)

usernameImage=PhotoImage(file='user (1).png')
usernameLabel=Label(loginFrame, image=usernameImage, text='Username', compound=LEFT
                    ,font=('times new roman', 20,'bold'))
usernameLabel.grid(row=1, column=0, pady=10, padx=20)

usernameEntry=Entry(loginFrame, font=('times new roman', 20,'bold'), bd=5)
usernameEntry.grid(row=1, column=1, pady=10, padx=20)


passwordImage=PhotoImage(file='password.png')
passwordLabel=Label(loginFrame, image=passwordImage, text='Password', compound=LEFT
                    ,font=('times new roman', 20,'bold'))
passwordLabel.grid(row=2, column=0, pady=10, padx=20)

passwordEntry=Entry(loginFrame, font=('times new roman', 20,'bold'), bd=5)
passwordEntry.grid(row=2, column=1, pady=10, padx=20)

loginButton=Button(loginFrame, text='Login', font=('times new roman', 14,'bold'),width=15
                   , fg='white', bg='Black', activebackground='Black'
                   , activeforeground='white', cursor='hand2', command=login)
loginButton.grid(row=3, column=1,pady=10)

window.mainloop()

