# sending emails with python 
# -*- coding: utf-8 -*-
 
import win32com.client as win32
import psutil
import os
import subprocess
 
# Drafting and sending email notification to senders. You can add other senders' email in the list
def send_notification(recipient: str, textbody: str):
    outlook = win32.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)
    mail.To = recipient
    mail.Subject = 'Certificate warnining'
    mail.body = textbody
    mail.send
     
# Open Outlook.exe. Path may vary according to system config
# Please check the path to .exe file and update below
     
def open_outlook():
    try:
        subprocess.call(['C:\Program Files (x86)\Microsoft Office\root\Office16\Outlook.exe'])
        os.system("C:\Program Files (x86)\Microsoft Office\root\Office16\Outlook.exe")
    except:
        print("Outlook didn't open successfully")
 
# Checking if outlook is already opened. If not, open Outlook.exe and send email
def check_and_send_mail(recipient: str, textbody: str):
    # loops through all processes and breaks if outlook runs already
    for item in psutil.pids():
        p = psutil.Process(item)
        if p.name() == "OUTLOOK.EXE":
            flag = 1
            break
        else:
            flag = 0
    
    if (flag == 1):
        send_notification(recipient, textbody)
    else:
        open_outlook()
        send_notification(recipient, textbody)
        