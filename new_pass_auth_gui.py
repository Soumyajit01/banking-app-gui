import pass_auth
import pyperclip,time
from tkinter import *

root = Tk()
root.title("Password authentication GUI")
root.geometry("800x500")
root.resizable(0,0)

passInputFrame = Frame(root)
enter_pass_label = Label(passInputFrame, text="Enter your password: ",font=('Cascadia Code',20))
enter_pass_input = Entry(passInputFrame,font=('Cascadia Code',20))
enter_pass_label.grid(row=0,column=0)
enter_pass_input.grid(row=0,column=1)
passInputFrame.pack()
def viewHashedPass():
    hash_text.delete(0,END)
    enteredPassword=str(enter_pass_input.get())
    hash_text.pack()
    copy_btn.pack()
    hash_text.insert(0,pass_auth.hash(enteredPassword))

hash_btn = Button(root,text="Hash password",font=("cascadia code",15),fg='White',bg='blue',command=viewHashedPass)
hash_text = Entry(root,font=("Cascadia code",15),width=30)
def copy():
    pyperclip.copy(hash_text.get())
    success = Label(root,text='TEXT COPIED TO CLIPBOARD!').pack()
copy_btn = Button(root,text="Copy hashed password",pady=5,command=copy)
hash_btn.pack(pady=10)
root.mainloop()