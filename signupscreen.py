import string
from tkinter import *
from tkinter import messagebox
import server
import random
import datetime
import dashboard
import customtkinter
import pass_auth
customtkinter.set_default_color_theme("dark-blue")
customtkinter.set_appearance_mode("dark")

total_ids = server.accounts

signup = customtkinter.CTk()
signup.title('Create new account form')
signup.geometry("900x500")
signup.resizable(0,0)
heading = customtkinter.CTkLabel(master=signup,
                               text="IndiaPay- CREATE ACCOUNT",
                               fg_color=('#67abe5'),
                               width=840,
                               height=25,
                               corner_radius=50,
                               font=("Koulen",50))
heading.pack(pady=10)
form = customtkinter.CTkFrame(signup, width=1000,height=400,corner_radius=20)


letters = string.ascii_lowercase
# print(letters,type(letters))

def createAccount():
    phoneNumList  = []
    for i in list(server.accounts.values()):
        print(i)
        phoneNumList.append(i['phonenum'])
        # we got the phonenumber list
    if (len(phonenum_input.get())==10 and len(name_input.get())>0 and len(password_input.get())>0 and len(email_input.get())>5 and email_input.get().find('@')>0 and len(aadhar_card_input.get())==12 ):
        if((name_input.get().lower()) not in server.accounts.keys() and int(phonenum_input.get()) not in phoneNumList):
            total_ids.update({name_input.get().lower():{
                'email': email_input.get(),
                'phonenum': int(phonenum_input.get()),
                'aadhar card': aadhar_card_input.get(),
                'accountnum': random.randint(1000000000000000,9999999999999999),
                'password': pass_auth.hash(password_input.get()),
                'money': 0
            }})
            with open('server.py', 'w') as f:
                f.write(f"accounts = {str(total_ids)}")
                with open(f"logs/{name_input.get().lower()}.txt",'w') as f:
                    f.write(f"[{datetime.datetime.now()}]- Account created\n")
            messagebox.showinfo("Success!", "Account created successfully!")
            signup.withdraw()
            dashboard.viewDashboard(name_input.get().lower(), server.accounts[name_input.get().lower()]['money'])
            phonenum_input.delete(0,END)
            name_input.delete(0,END)
            email_input.delete(0,END)
            password_input.delete(0,END)
            aadhar_card_input.delete(0,END)
            #print(name_input.get())
        else:
            messagebox.showerror('Failed','This name or phone number has already been taken, kindly use another one :)')
    else:
        messagebox.showerror('Failed','Please enter valid detail(s)')



name_label = customtkinter.CTkLabel(form,text="Name: ", font=("Cascadia Code",25))
name_input=customtkinter.CTkEntry(form, width=250,font=("Cascadia Code",20))
email_label = customtkinter.CTkLabel(form,text="Email: ", font=("Cascadia Code",25))
email_input=customtkinter.CTkEntry(form, width=250,font=("Cascadia Code",20))
passw_label= customtkinter.CTkLabel(form,text="Password: ", font=("Cascadia Code",25))
password_input = customtkinter.CTkEntry(form,width=250, show='*', font=("Cascadia Code",20))
phonenum_label= customtkinter.CTkLabel(form,text="Phone number: ",font=("Cascadia Code",25))
phonenum_input = customtkinter.CTkEntry(form, width=250,font=("Cascadia Code",20))
aadhar_card_label= customtkinter.CTkLabel(form,text="Aadhar card number: ", font=("Cascadia Code",25))
aadhar_card_input = customtkinter.CTkEntry(form, width=250,font=("Cascadia Code",20))

button_create_account = customtkinter.CTkButton(signup, text="Create account", command=createAccount,font=("Cascadia Code",25), corner_radius=20)

form.pack(pady=20)
name_label.grid(row=0,column=0)
name_input.grid(row=0,column=1, pady=(10,0),padx=20)
email_label.grid(row=1,column=0)
email_input.grid(row=1, column=1, pady=10)
phonenum_label.grid(row=2,column=0)
phonenum_input.grid(row=2,column=1)
aadhar_card_label.grid(row=3, column=0)
aadhar_card_input.grid(row=3, column=1, pady=10)
passw_label.grid(row=4,column=0)
password_input.grid(row=4,column=1,pady=(0,10))
button_create_account.pack(pady=10)
signup.mainloop()