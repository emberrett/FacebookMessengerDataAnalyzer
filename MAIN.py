#  ask for file path of data file
from tkinter import Tk
from tkinter.filedialog import askopenfilename

filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
print(filename)

# ask if user wants to analyze all data or a single group


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
