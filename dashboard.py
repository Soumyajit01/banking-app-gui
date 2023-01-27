from tkinter import *
import server
from tkinter import messagebox
import datetime
import customtkinter
import os
import keyboard

customtkinter.set_default_color_theme("blue")
customtkinter.set_appearance_mode("dark")
#print(list(server.accounts.keys()))

def viewDashboard(name, money):

    dashboard = customtkinter.CTk()
    dashboard.resizable(0,0)
    dashboard.geometry("900x500")
    dashboard.title(f'Dashboard-{name}')

    bankName=customtkinter.CTkLabel(dashboard, text="IndiaPay",font=("Koulen",50))
    bankName.pack()
    account_frame= customtkinter.CTkFrame(dashboard,border_width=0,width=900,corner_radius=10,fg_color='transparent')
    user_frame = customtkinter.CTkFrame(account_frame,fg_color='transparent',border_width=0,corner_radius=10)
    user_logo = customtkinter.CTkLabel(user_frame, text="")
    user_name = customtkinter.CTkLabel(user_frame, text=f"{name}: Rs.{money}",font=("Cascadia Code",20,'underline'))
    user_logo.grid(row=0,column=0)
    user_name.grid(row=0,column=1,padx=(20,0))
    def logoutClick():
        dashboard.destroy()
        os.startfile('mainscreen.pyw')
        with open(f"logs/{name}.txt",'a') as f:
            f.write(f"[{datetime.datetime.now()}]- Logged out\n")
    logout_frame = customtkinter.CTkButton(account_frame, text="Logout",font=("Cascadia Code",20),command=logoutClick,fg_color="#e36d64",hover_color="#ff0000")
    logout_frame.grid(row=0,column=1, padx=(500,0))
    user_frame.grid(row=0,column=0)
    # user_frame.pack(anchor='nw')

    # balance_frame = customtkinter.CTkFrame(account_frame, fg_color="#6800d4", border_width=0, corner_radius=10)
    # Label(balance_frame, text=f"Rs. {money}",font=("Cascadia Code",20)).grid(row=0,column=0)
    # balance_frame.pack(anchor='n')
    # balance_frame.grid(row=0,column=1)

    account_frame.pack(anchor='nw')

    bankingOptions=customtkinter.CTkFrame(dashboard,width=850,height=250,fg_color="#242424",border_width=2)
    
    global logs_frame
    def payMoney():
        logs_frame.forget()
        operations_frame.forget()
        recharge_frame.forget()
        customise_frame.forget()
        operations_frame.pack(pady=50,padx=120,fill="both")
        
        # form = LabelFrame(operations_frame)
        to_label = Label(operations_frame, text="To:",font=("Cascadia Code",25),bg='#383b40',fg='white')
        to_label.grid(row=0,column=1,padx=(10,0))

        to_label.grid(row=0,column=0,padx=(50,0))
        to_input = customtkinter.CTkEntry(operations_frame, width=300,font=("Cascadia Code",20),placeholder_text='Phone number')
        to_input.grid(row=0,column=1,padx=(50,0),pady=10)

        amount_label = Label(operations_frame, text="Amount:",font=("Cascadia Code",25),bg='#383b40',fg='white').grid(row=2,column=0,padx=(100,0))
        amount_input= customtkinter.CTkEntry(operations_frame, width=300,font=("Cascadia Code",20),placeholder_text='Amount')
        amount_input.grid(row=2,column=1,padx=(50,0),pady=10)

        def payMoney():
            money=server.accounts[name]['money']
            #print('I have rs', money)
            # print(to_input, type(to_input))
            try:
                amtToSend=round(float(amount_input.get()))
            except Exception as e:
                messagebox.showerror('Error!','Enter proper details')
                # operations_frame.destroy()

            # Getting the list of phone numbers
            def getUser(phoneNum=to_input.get()):
                listPhoneNums = []
                for i in list(server.accounts.values()):
                    listPhoneNums.append(i['phonenum'])

                if int(to_input.get()) in listPhoneNums:
                    to_send_index = listPhoneNums.index(int(to_input.get()))
                    to_send_info =(list(server.accounts.items())[to_send_index])
                    sendTo = to_send_info[0] # money receiver
                    return sendTo
                else:
                    pass
                
            sendTo=getUser()
            if(amtToSend>money):
                messagebox.showerror('Failed!','Not enough money!')
                to_input.delete(0,END)
                amount_input.delete(0,END)
            elif(sendTo not in list(server.accounts.keys()) and len(to_input.get())==10):
                messagebox.showerror('Failed!','Sorry, no such account found!')
                to_input.delete(0,END)
                amount_input.delete(0,END)
            elif(len(to_input.get())!=10):
                #print(to_input.get(),len(to_input.get()))
                messagebox.showerror("Failed!","Please enter a proper 10-digit phone number")
                to_input.delete(0,END)
                amount_input.delete(0,END)
            elif(sendTo==name):
                messagebox.showerror('Bruhhh!','You can\'t send money to yourself!')
                to_input.delete(0,END)
                amount_input.delete(0,END)
            elif(amtToSend<0 or str(amtToSend).isdigit()==False):
                messagebox.showinfo("Failed!","Please enter a valid amount!")
                to_input.delete(0,END)
                amount_input.delete(0,END)
            else:
                money = money-int(amtToSend)
                accounts = server.accounts.copy()
                accounts[name]['money']=money
                
                if sendTo in list(server.accounts.keys()):
                    accounts[sendTo]['money'] = int(accounts[sendTo]['money']) +amtToSend
                    #print(accounts[sendTo]['money'])

                    with open('server.py', 'w') as f:
                        f.write(f"accounts = {str(accounts)}")
                    with open(f'logs/{name}.txt','a') as f:
                        f.write(f"[{datetime.datetime.now()}]-Paid Rs.{amtToSend} to {sendTo}\n")
                    with open(f'logs/{sendTo}.txt','a') as f:
                        f.write(f"[{datetime.datetime.now()}]-Received Rs.{amtToSend} from {name}\n")
                    messagebox.showinfo('Success!', f"Rs.{amtToSend} has been sent to {sendTo}!")
                    # form.destroy()
                    # print(name,money)
                    # print(accounts)
                else:
                    messagebox.showinfo(':/', "Sorry, no such account found!")
                    to_input.delete(0, END)
                    amount_input.delete(0,END)
                # user_name = Label(top_left, text=f"{name}: Rs. {money}" font=('Verdana'),bg='#ffffff').grid(row=0, column=1)
                user_name.configure(text=f"{name}: Rs.{money}")

        payMoneyBtn = customtkinter.CTkButton(operations_frame, text="Pay", font=("Cascadia Code",20),command=payMoney, fg_color="#80dcbd",text_color='black',hover_color="#13855e")
        payMoneyBtn.grid(row=3,column=1,pady=(0,5))
        def hideFrame():
            operations_frame.forget()
            logs_frame.forget()
        hideOperationsFrame = customtkinter.CTkButton(operations_frame, text="Hide", font=("Cascadia Code",20), command=hideFrame,fg_color='#858181',hover_color="#675858")
    def viewLog():
        for widget in logs_frame.winfo_children():
            widget.destroy()
        operations_frame.forget()
        customise_frame.forget()
        recharge_frame.forget()
        # logs_frame.forget()
        logs_frame.pack(pady=50,padx=120,fill="both")
        f=open(f'logs/{name}.txt','r')
        data = f.readlines()
        i=0
        body=""
        for log in data:
            i+=1
            body=body+log
        logs_to_display = customtkinter.CTkLabel(logs_frame, text=body, font=("Cascadia Code",15),fg_color='#383b40',height=200).pack()
        ctk_textbox_scrollbar = customtkinter.CTkScrollbar(logs_frame)
        

    pay=customtkinter.CTkButton(bankingOptions,text="Pay",font=("Cascadia Code",20),command=payMoney)
    logs_frame = customtkinter.CTkFrame(dashboard,fg_color='#383b40',height=500,corner_radius=10)
    

    transactions=customtkinter.CTkButton(bankingOptions,text="View Transactions",font=("Cascadia Code",20), command=viewLog)

    def viewRechargeOptions():
        operations_frame.forget()
        customise_frame.forget()
        logs_frame.forget()
        recharge_frame.pack(pady=50,padx=120,fill="both")
        def mobileInputClear():
            amt=server.accounts[name]['money']
            if(int(mobile_recharge_amt.get())>amt):
                messagebox.showerror("Failed!","Not enough money!")
            else:
                accounts = server.accounts.copy()
                amt = amt - int(mobile_recharge_amt.get())
                accounts[name]['money']=amt
                # print(accounts[name]['money'])

                with open('server.py', 'w') as f:
                    f.write(f"accounts = {str(accounts)}")
                messagebox.showinfo("Paid!",f"Recharged Rs.{mobile_recharge_amt.get()} to mobile number {mobile_recharge_input.get()}")
                f=open(f"logs/{name}.txt",'a')
                f.write(f"[{datetime.datetime.now()}]- Recharged Rs.{mobile_recharge_amt.get()} to mobile number {mobile_recharge_input.get()}\n")
                user_name.configure(text=f"{name}: Rs. {amt}")
                mobile_recharge_input.delete(0,END)
                mobile_recharge_amt.delete(0,END)
            # messagebox.showinfo("Paid!",f"Recharged Rs.{mobile_recharge_amt.get()} to {mobile_recharge_input.get()}")
            # mobile_recharge_input.delete(0,END)
            # mobile_recharge_amt.delete(0,END)
        mobile_recharge_label = customtkinter.CTkLabel(recharge_frame, text="Mobile: ",font=("Cascadia Code",20))
        mobile_recharge_input = customtkinter.CTkEntry(recharge_frame, placeholder_text="Number",font=("Cascadia Code",20),width=150)
        mobile_recharge_amt = customtkinter.CTkEntry(recharge_frame,font=("Cascadia Code",20),placeholder_text="Amount(Rs.)",width=150)
        mobile_recharge_btn = customtkinter.CTkButton(recharge_frame,font=("Cascadia Code",20),text="Recharge",fg_color='#4f3930',hover_color='#302824',width=20,command=mobileInputClear)
        mobile_recharge_label.grid(row=0,column=0,padx=(50,0))
        mobile_recharge_input.grid(row=0,column=1,padx=(10,0))
        mobile_recharge_amt.grid(row=0,column=2,padx=(50,0))
        mobile_recharge_btn.grid(row=0,column=3,padx=(30,0),pady=(10,0))
        
        dishtv_recharge_label = customtkinter.CTkLabel(recharge_frame, text="DishTV:",font=("Cascadia Code",20))
        dishtv_recharge_input = customtkinter.CTkEntry(recharge_frame, placeholder_text="TV vc number",font=("Cascadia Code",18),width=150)
        dishtv_recharge_amt = customtkinter.CTkEntry(recharge_frame,font=("Cascadia Code",20),placeholder_text="Amount(Rs.)",width=150)
        def tvInputClear():
            amt=server.accounts[name]['money']
            if(int(dishtv_recharge_amt.get())>amt):
                messagebox.showerror("Failed!","Not enough money!")
            else:
                accounts = server.accounts.copy()
                amt = amt - int(dishtv_recharge_amt.get())
                accounts[name]['money']=amt
                # print(accounts[name]['money'])

                with open('server.py', 'w') as f:
                    f.write(f"accounts = {str(accounts)}")
                messagebox.showinfo("Paid!",f"Recharged Rs.{dishtv_recharge_amt.get()} to TV vc number {dishtv_recharge_input.get()}")
                f=open(f"logs/{name}.txt",'a')
                f.write(f"[{datetime.datetime.now()}]- Recharged Rs.{dishtv_recharge_amt.get()} to TV vc number {dishtv_recharge_input.get()}\n")
                user_name.configure(text=f"{name}: Rs. {amt}")
                dishtv_recharge_input.delete(0,END)
                dishtv_recharge_amt.delete(0,END)
        dishtv_recharge_btn = customtkinter.CTkButton(recharge_frame,font=("Cascadia Code",20),text="Recharge",fg_color='#4f3930',hover_color='#302824',width=20,command=tvInputClear)
                
        dishtv_recharge_label.grid(row=1,column=0,padx=(40,0))
        dishtv_recharge_input.grid(row=1,column=1,padx=(10))
        dishtv_recharge_amt.grid(row=1,column=2,padx=(50,0),pady=(10))
        dishtv_recharge_btn.grid(row=1,column=3,padx=(30,0))

        wifi_recharge_label = customtkinter.CTkLabel(recharge_frame, text="WiFi:",font=("Cascadia Code",20))
        wifi_recharge_input = customtkinter.CTkEntry(recharge_frame, placeholder_text="Number",font=("Cascadia Code",20),width=150)
        wifi_recharge_amt = customtkinter.CTkEntry(recharge_frame,font=("Cascadia Code",20),placeholder_text="Amount(Rs.)",width=150)
        def wifiInputClear():
            amt=server.accounts[name]['money']
            if(int(wifi_recharge_amt.get())>amt):
                messagebox.showerror("Failed!","Not enough money!")
            else:
                accounts = server.accounts.copy()
                amt = amt - int(wifi_recharge_amt.get())
                accounts[name]['money']=amt
                # print(accounts[name]['money'])

                with open('server.py', 'w') as f:
                    f.write(f"accounts = {str(accounts)}")
                messagebox.showinfo("Paid!",f"Recharged Rs.{wifi_recharge_amt.get()} to your wifi number {wifi_recharge_input.get()}")
                f=open(f"logs/{name}.txt",'a')
                f.write(f"[{datetime.datetime.now()}]- Recharged Rs.{wifi_recharge_amt.get()} to wifi {wifi_recharge_input.get()}\n")
                user_name.configure(text=f"{name}: Rs. {amt}")
                wifi_recharge_input.delete(0,END)
                wifi_recharge_amt.delete(0,END)
        wifi_recharge_btn = customtkinter.CTkButton(recharge_frame,font=("Cascadia Code",20),text="Recharge",fg_color='#4f3930',hover_color='#302824',width=20,command=wifiInputClear)
                
        wifi_recharge_label.grid(row=2,column=0,padx=(40,0))
        wifi_recharge_input.grid(row=2,column=1,padx=(10))
        wifi_recharge_amt.grid(row=2,column=2,padx=(50,0),pady=(10))
        wifi_recharge_btn.grid(row=2,column=3,padx=(30,0))
        
        
    def viewCustomise():
        def confirmDeletion():
            if server.accounts[name]['money']==0:
                confirm = messagebox.askyesno('CONFIRM?','Are you sure?')
                if(confirm==True and server.accounts[name]['money']==0):
                    accounts=server.accounts
                    del accounts[name]
                    with open('server.py', 'w') as f:
                            f.write(f"accounts = {str(accounts)}")
                    with open(f'logs/{name}.txt','a') as f:
                        f.write(f"[{datetime.datetime.now()}]-Account deleted\n")
                    dashboard.destroy()
                    os.startfile(fr"logs\{name}.txt")
            else:
                messagebox.showwarning("Alert!","Your account still has balance. Kindly get the balance to 0 in order to delete your account")
        operations_frame.forget()
        logs_frame.forget()
        recharge_frame.forget()
        customise_frame.pack(pady=50,padx=120,fill="both")
        def saveChanges():
            accounts = server.accounts
            # newName=str(newName_input.get())
            newEmail=str(newEmail_input.get())
            newPhonenum=str(newPhonenum_input.get())
            newPassword=str(newPassword_input.get())
            
            # accounts[newName]=accounts.pop(_name)
            accounts[name]['email']=newEmail
            accounts[name]['phonenum']=int(newPhonenum)
            accounts[name]['password']=newPassword
            with open('server.py', 'w') as f:
                f.write(f"accounts = {str(accounts)}")
            messagebox.showinfo('Success!','Changes saved')
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
        save_chances_btn=customtkinter.CTkButton(customise_frame,text="Save preferences",text_color="white",fg_color="#5eafd1",font=('Cascadia Code',18),hover_color="#22424f", command=saveChanges)
        delete_btn=customtkinter.CTkButton(customise_frame,text="Delete account",text_color="white",fg_color="#fc6565",font=('Cascadia Code',12),hover_color="#ff0000", command=confirmDeletion)
        # newName_label = customtkinter.CTkLabel(customise_frame,text="Name: ",font=("Cascadia Code",18))
        # newName_input = customtkinter.CTkEntry(customise_frame,font=("Cascadia Code",18),width=200)
        # newName_input.insert(0, name)

        newEmail_label = customtkinter.CTkLabel(customise_frame,text="Email: ",font=("Cascadia Code",18))
        newEmail_input = customtkinter.CTkEntry(customise_frame,font=("Cascadia Code",18),width=300)
        newEmail_input.insert(0, server.accounts[name]['email'])

        newPhonenum_label = customtkinter.CTkLabel(customise_frame,text="Phone number: ",font=("Cascadia Code",18))
        newPhonenum_input = customtkinter.CTkEntry(customise_frame,font=("Cascadia Code",18),width=300)
        newPhonenum_input.insert(0, server.accounts[name]['phonenum'])

        newPassword_label = customtkinter.CTkLabel(customise_frame,text="Password: ",font=("Cascadia Code",18))
        newPassword_input = customtkinter.CTkEntry(customise_frame,font=("Cascadia Code",18),width=300,show="*")
        newPassword_input.insert(0, decode(server.accounts[name]['password']))

        # newName_label.grid(row=0,column=0,padx=5,pady=(5,0),sticky="w")
        # newName_input.grid(row=0,column=1,pady=2,sticky="w")
        newEmail_label.grid(row=1,column=0,padx=5,pady=(5,0),sticky="w")
        newEmail_input.grid(row=1,column=1,pady=2,sticky="w")
        newPhonenum_label.grid(row=2,column=0,padx=5,pady=(5,0),sticky="w")
        newPhonenum_input.grid(row=2,column=1,pady=2,sticky="w")
        newPassword_label.grid(row=3,column=0,padx=5,pady=(5,0),sticky="w")
        newPassword_input.grid(row=3,column=1,pady=2,sticky="w")
        save_chances_btn.grid(row=4,column=1,padx=5,pady=2)
        delete_btn.grid(row=4,column=3,pady=(2,5),padx=(5,0))

    recharge=customtkinter.CTkButton(bankingOptions,text="Recharge",font=("Cascadia Code",20),command=viewRechargeOptions)
    customise=customtkinter.CTkButton(bankingOptions,text="Customise",font=("Cascadia Code",20),command=viewCustomise)

    pay.grid(row=0,column=0,padx=(20,10),pady=20)
    transactions.grid(row=0,column=1,padx=(10,10)) #,padx=(50,50)
    recharge.grid(row=0,column=2,padx=(10,10))#,padx=(50,50)
    customise.grid(row=0,column=3,padx=(10,20))

    bankingOptions.pack(fill=Y,pady=(20,0),)
    operations_frame = customtkinter.CTkFrame(dashboard,fg_color='#383b40',height=500,corner_radius=10)
    recharge_frame = customtkinter.CTkFrame(dashboard,fg_color='#383b40',height=500,corner_radius=10)
    customise_frame = customtkinter.CTkFrame(dashboard,fg_color='#383b40',height=1000,width=500,corner_radius=10)
    customise_frame.configure()
    dashboard.mainloop()


if __name__ == "__main__":
    viewDashboard('dsafa',1000)