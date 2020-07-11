from datetime import datetime  # for handling dates and time
from datetime import timezone  # for handling timezones
import matplotlib.pyplot as plt  # library for plotting data
import operator  # to convert dictionary to list
from tkinter import filedialog  # for file selection UI
from tkinter import *  # for UI
import json  # for handling json
import os  # library for handling paths
from MAIN import get_messages, find_sender_count

# keeps root window closed
root = Tk()
root.withdraw()

# ask user to select file
folder = filedialog.askdirectory(title="Select Folder")
folder_name = os.path.basename(os.path.normpath(folder)).split("_")[0]
start_datetime = 'Jan 1 2020  12:00AM'
end_datetime = 'Jan 1 2021  12:00AM'

find_sender_count(start_datetime, end_datetime)


