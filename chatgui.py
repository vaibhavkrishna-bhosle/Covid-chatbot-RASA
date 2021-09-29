#Creating GUI with tkinter
import tkinter
from utils import *
from tkinter import *

def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)

    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="black", font=("Verdana", 10 ),  bg="#ffffff")

        res = chatbot_response(msg)
        ChatLog.insert(END, "Bot: " + res + '\n\n')

        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)

base = Tk()
base.title("COVID-19 Queries - Ready to help 24/7")
base.geometry("550x500")
base.resizable(width=FALSE, height=FALSE)

#Create Chat window
ChatLog = Text(base, bd=0, bg="#ffffff", height="8", width="50", font=("Verdana",10))

ChatLog.config(state=DISABLED)

#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview)
ChatLog['yscrollcommand'] = scrollbar.set

#Create Button to send message
SendButton = Button(base, font=("Verdana",11,'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#4e9525", activebackground="#4e9525",fg='#000000',
                    command= send )

#Create the box to enter message
EntryBox = Text(base, bd=0, bg="lightgrey",width="29", height="4", font=("Verdana",11))
#EntryBox.bind("<Return>", send)

#Place all components on the screen
scrollbar.place(x=536,y=6, height=407)
ChatLog.place(x=6,y=6, height=407, width=532)
EntryBox.place(x=6, y=422, height=72, width=404)
SendButton.place(x=416, y=422, height=72)

base.mainloop()
