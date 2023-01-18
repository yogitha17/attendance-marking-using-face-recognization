import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from tkinter import *

import pandas as pd
from datetime import datetime


import os
#
# def fun1():
#     root.destroy()

class App:
    # 'what' and 'why' should probably be fetched in a different way, suitable to the app
    id = ''

    def __init__(self, parent):
        # self.parent.geometry("400x200")
        self.parent = parent
        self.parent.title("enter email id:")
        self.label = Label(self.parent, text="Enter Email Id")
        self.label.pack()
        self.entry = Entry(self.parent,width=50)
        self.entry.pack()
        self.button = Button(parent, text='OK', command=self.use_entry)
        self.button.pack()

    def use_entry(self):
        contents = self.entry.get()
        self.id=contents
        # do stuff with contents
        self.parent.destroy()  # if you must


root = Tk()
root.geometry("400x200")
r = App(root)
root.mainloop()
recmail=r.id

if str(recmail) != '':
    mail_content = '''Hello,
    Today's Attendance sheet:
    '''
    # The mail addresses and password
    # recmail=input('enter your mail address:')
    print('Sending Mail to ' + recmail)
    sender_address = 'palukuri.17.it@anits.edu.in'
    sender_pass = 'yogitha@2000'
    receiver_address = recmail
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = "Today's Attendance. Date: "+ str(datetime.now().date())+"."
    # xlsx to csv conversion
    # data_xls = pd.read_excel(os.getcwd() + "/firebase/attendance_files/attendance" + str(datetime.now().date()) + '.xls', 'class1',index_col=None)
    # '/firebase/attendance_files/attendance'+str(datetime.now().date())+'.xls'
    # data_xls.to_csv('attendence.csv', encoding='utf-8')
    # The subject line
    # The body and the attachments for the mail

    filename = "firebase/attendance_files/attendance" + str(datetime.now().date()) + '.xls'  # In same directory as script

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    # text = message.as_string()

    # message.attach(MIMEText(mail_content, 'plain'))
    # attach_file_name = 'firebase/attendance_files/attendance2021-05-10.xls'
    # payload = MIMEBase('application', 'octate-stream')
    # payload.set_payload(open('firebase/attendance_files/attendance2021-05-10.xls', "rb").read())
    # encoders.encode_base64(payload)  # encode the attachment
    # # add payload header with filename
    # payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
    # message.attach(payload)
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent Successfully')
    # # root = Tk()
    # # root.geometry("400x200")
    # label = Label(root, text="Mail Sent Successfully")
    # label.pack()
    # button = Button(root, text='OK', command=fun1)
    # button.pack()
else:
    print("Please enter a valid mail id")

