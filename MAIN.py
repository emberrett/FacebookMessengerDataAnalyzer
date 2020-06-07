#  import libraries
import tkinter as tk
from tkinter.filedialog import askopenfilename
import os
from bs4 import BeautifulSoup as bs
import re
from datetime import datetime

# QUERY - FIND MOST USED WORDS


file = "/home/ethan/Desktop/facebook-ethanberrett23/messages/inbox/2016marchmadness_6aeoefufua/message_1.html"


# write a function that takes the file name as a parameter
def getmessages(messageFile):
    with open(messageFile, 'r') as f:
        html_string = f.read()

    parsedFile = str(bs(html_string, 'html.parser'))
    print(parsedFile)

    # div class that always precedes a message
    DivClass = "_3-96 _2pio _2lek _2lel"

    # skip first message since it isn't an actual message
    messages = re.finditer(DivClass, parsedFile)
    next(messages)

    # create dictionary to store messages
    messDict = {}
    # starting number for dictionary
    x = 0
    for m in messages:
        # find date of message
        DateEnd = m.start() - 79
        CutDate = parsedFile[:DateEnd]
        DateStart = CutDate.rfind("2lem") + 6
        DateTime = CutDate[DateStart:]

        # convert to standard date time
        DateTime = datetime.strptime(DateTime, "%b %d, %Y, %I:%M %p")
        DateTime = str(DateTime)

        # find name of message sender
        NameStart = m.start() + 25
        CutName = parsedFile[NameStart:]
        NameEnd = CutName.find("</div>")
        Name = CutName[0:NameEnd]

        # find message
        CutMessage = CutName[NameEnd + 52:]
        MessageEnd = CutMessage.find("</div>")
        Message = CutMessage[:MessageEnd]

        MessageTuple = DateTime, Name, Message
        messDict[x] = MessageTuple
        x += 1


getmessages(file)

