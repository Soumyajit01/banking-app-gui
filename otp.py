import customtkinter
from email.message import EmailMessage
import ssl
import smtplib
import random
from tkinter import messagebox
customtkinter.set_default_color_theme("dark-blue")
customtkinter.set_appearance_mode("dark")
otp = random.randint(1000,9999) #generating the 4-digit otp
def sendOTP(receiver):
    email_sender = 'senderEmail@example.com'
    f=open('email_pass.txt','r')
    email_pass = f.read()
    f.close()
    email_receiver = receiver
    subject = "OTP for login to IndiaPay."
    
    body = f"""Thank you for using IndiaPay. Here's the OTP to sign in to access your account: {otp}"""
    em=EmailMessage()
    em['From'] =email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)
    context = ssl.create_default_context()
    messagebox.showinfo('OTP','Please wait for a few seconds...You will receive an OTP on your email')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_pass)
            smtp.sendmail(email_sender,email_receiver, em.as_string())