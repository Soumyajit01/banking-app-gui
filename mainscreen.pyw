from tkinter import *
from tkinter import messagebox
import server
import dashboard
import otp
import customtkinter
import datetime
from PIL import Image

total_entries = server.accounts
ids = list(total_entries.keys())
#print(ids)
# passwords = list(total_entries.values())
# print(total_entries.values())

root = customtkinter.CTk()
root.geometry("700x500")
root.resizable(0,0)
# root.configure(background='#ffe1a6')
root.title('IndiaPay')
root.geometry("900x500")
# root.resizable(0,0 )
heading = customtkinter.CTkLabel(root,text="IndiaPay",font=("Koulen",50),corner_radius=20)
heading.pack()
# Creating a new frame and it's parts
form = customtkinter.CTkFrame(root, width=400,height=200, corner_radius=20)
form.pack(pady=50)
login_id = customtkinter.CTkLabel(form,text="ID: ",font=("Cascadia Code",25))
login_input=customtkinter.CTkEntry(form, placeholder_text="ID",font=('Cascadia Code',19),width=300)
login_passw= customtkinter.CTkLabel(form,text="Password: ", font=("Cascadia Code",25))
login_password_input = customtkinter.CTkEntry(form,placeholder_text="Password",font=("Cascadia Code",19),show="*",width=300)

def signin():
    def decode(passw):
        characters = ['!','@','#','$','%','^','&','*','_','.',"+"]
        nums = [0,1,2,3,4,5,6,7,8,9]
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        passw = passw[3:-3] #removing first 3 and last 3 characters
        passw = passw[::2] # slicing
        passw = passw[::-1] #reversing 
        password = ''
        for i in list(passw):
            # print(i,type(i))
            if i in letters:
                i_index = letters.index(i)
                newIndex = i_index-1
                newLetter = letters[newIndex]
                password = password+newLetter
            elif i in characters:
                i_index = characters.index(i)
                newIndex = i_index-1
                newChar = characters[newIndex]
                password = password+newChar
            elif int(i) in nums:
                i_index = nums.index(int(i))
                newIndex = i_index-1
                newNum = nums[newIndex]
                password = password+str(newNum)
            
        return password
        
    
    login_user = login_input.get().lower()
    login_pwd = login_password_input.get()
    if (login_user in ids) and (login_pwd == decode(server.accounts[login_user]['password'])):
        messagebox.showinfo('CORRECT PASSWORD', 'CORRECT PASSWORD ENTERED!')
        accountnum = server.accounts[login_user]['accountnum']
        money = server.accounts[login_user]['money']
        # root.withdraw()
        otp_=otp.otp
        #print(otp_)

        otp.sendOTP(server.accounts[login_user]['email'])
        otp_screen=customtkinter.CTkToplevel()
        otp_screen.title('OTP')
        
        # otp_screen._max_height(200)
        otp_screen.resizable(0,0)
        # otp_screen.config(bg="#f2cf6d")
        customtkinter.CTkLabel(otp_screen, text="An OTP has been sent to your email").grid(row=0,column=0)
        otp_label = customtkinter.CTkLabel(otp_screen, text='Enter the OTP: ').grid(row=1,column=0, pady=5)
        otp_input = customtkinter.CTkEntry(otp_screen)
        otp_input.grid(row=1,column=1)
        def confirmOTP():
            if otp_input.get()==str(otp_):
                root.withdraw()
                otp_screen.withdraw()
                with open(f"logs/{login_user}.txt",'a') as f:
                    f.write(f"[{datetime.datetime.now()}]- Signed in\n")
                dashboard.viewDashboard(login_user, money)
            else:
                retry = messagebox.showerror('OTP',"INCORRECT OTP ENTERED!")
                otp_input.delete(0,END)
                #print(retry)
        btn_check = customtkinter.CTkButton(otp_screen,text='Confirm',command=confirmOTP).grid(row=2,column=1,pady=5)
        

        otp_screen.mainloop()
    else:
        messagebox.showerror('INCORRECT PASSWORD', 'Incorrect password entered or no account found')
    login_password_input.delete(0,END)
authenticate = customtkinter.CTkFrame(root, corner_radius=20,fg_color='#1a1a1a')
# authenticate.config( borderwidth=0)
authenticate.pack()
signin_btn = customtkinter.CTkButton(authenticate, text="Login",corner_radius=10,font=("Cascadia Code",18), command=signin)
# signin_btn.pack(pady=10)
signin_btn.grid(row=0,column=1,pady=10)

def signUp():
    root.withdraw()
    import signupscreen

signup_btn = customtkinter.CTkButton(authenticate,corner_radius=10,text="Create a new account", font=("Cascadia Code",18), command=signUp)
# signup_btn.pack()
signup_btn.grid(row=2,column=1, padx=15,pady=5)
customtkinter.CTkLabel(authenticate, text='or',font=("Cascadia Code",20)).grid(row=1,column=1)

login_id.grid(row=0,column=0)
login_input.grid(row=0, column=1, padx=20)
login_password_input.grid(row=1, column=1, pady=10)
login_passw.grid(row=1,column=0)

root.mainloop()