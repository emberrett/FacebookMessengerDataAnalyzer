# library for handling dates and time
from datetime import datetime
# library for plotting data
import matplotlib.pyplot as plt
# library to convert dictionary to list
import operator
# library for UI
from tkinter import filedialog
from tkinter import *
# library for handling json
import json
import os

# keeps root window closed
root = Tk()
root.withdraw()

# create GUI
"""
window = Tk()

window.title('Messenger Data Analyzer')
window.geometry("300x300+10+20")
window.mainloop()

"""

# ask user to select file
folder = filedialog.askdirectory(title="Select Folder")

start_date = 1593578720
end_date = 1585102129512


# write a function that takes the file name as a parameter

# create dictionary to store messages
mess_dict = {}
x = 0
for file in os.listdir(folder):
    if file.endswith(".json"):
        file_path = os.path.realpath(folder) + "\\" + str(file)
        print(file_path)
        # open json file in read mode
        with open(file_path, "r") as read_file:
            data = json.load(read_file)
        # starting number for dictionary
        for message in data['messages']:
            # if message is a generic textual message
            if 'content' in message:
                # find content of message
                message_content = message['content']

                # find time of message
                message_timestamp = message['timestamp_ms']

                # find message sender
                message_sender = message['sender_name']

            message_tuple = message_timestamp, message_sender, message_content
            mess_dict[x] = message_tuple
            x += 1
print(mess_dict)
