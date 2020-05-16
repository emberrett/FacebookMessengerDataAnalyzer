#  ask for file path of data file
import tkinter as tk
from tkinter.filedialog import askopenfilename

# filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
# print(filename)


# create window
w = tk.Tk()
w.geometry("600x400")
w.title("Messenger Data Analyzer")
w.configure(background='white')

# create and initialize single group button
groupButton = tk.Button(w, text='Analyze Individual Group', width=25)
groupButton.place(relx=.5, rely=.2, anchor=tk.CENTER)

# create and initialize all data button
allButton = tk.Button(w, text='Analyze All Data', width=25)
allButton.place(relx=.5, rely=.4, anchor=tk.CENTER)

# initialize window
w.mainloop()

""" 
*If user selects specific group *
Create array of group names
Provide list to user and ask user to select a group (with search function)
"""

# if user selects all data, go to date range

# ask for date range

# show list of possible queries based on what user chose above

# run query (switch statement with queries contained in each one)

# Export data to CSV if desired - ask for file path/name
# create visualized data if desired
# export visualized data if desired - ask for file path/name
