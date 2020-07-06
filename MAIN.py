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

# keeps root window closed
root = Tk()
root.withdraw()

# ask user to select file
file = filedialog.askopenfilename()

start_date = 1593578720
end_date = 1585102129512


# write a function that takes the file name as a parameter
def get_messages():
    # open json file in read mode
    with open(file, "r") as read_file:
        data = json.load(read_file)

    # create dictionary to store messages
    mess_dict = {}
    # starting number for dictionary
    x = 0
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

    return mess_dict


def find_sender_count():
    mess_dict = get_messages()
    print(mess_dict)
    name_list = {}
    # get unique names in messages
    for x in mess_dict:
        y = mess_dict[x][1]
        if y not in name_list:
            name_list[y] = 0
            # check if message is in date range
        if start_date <= mess_dict[x][0] <= end_date:
            name_list[y] += 1
    print(name_list)

    # sort dictionary by descending order
    name_list = dict(sorted(name_list.items(), key=operator.itemgetter(1), reverse=True))

    group_name = input("What is the name of this group? ")
    string_start_date = str(start_date)
    string_end_date = str(end_date)
    chart_title = "Number of Messages Sent in " + group_name + '\n' + " from " + str(start_date) + " to " + \
                  str(end_date)
    # set x axis
    keys = name_list.keys()
    # set y axis
    values = name_list.values()

    # create chart
    plt.figure(figsize=(15, 15))
    plt.title(chart_title, fontsize=20)
    plt.bar(keys, values)
    plt.xticks(fontsize=20)
    plt.xticks(rotation=-70)
    plt.yticks(fontsize=20)
    plt.subplots_adjust(bottom=0.3)
    plt.show()


# add all unique values to tuples

find_sender_count()
