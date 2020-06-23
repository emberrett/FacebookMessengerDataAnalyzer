#  import libraries
from bs4 import BeautifulSoup as bs
import re
from datetime import datetime
import matplotlib.pyplot as plt
import operator
import time

# QUERY - FIND MOST USED WORDS


file = "/home/ethan/Desktop/facebook-ethanberrett23/messages/inbox/2016marchmadness_6aeoefufua/message_1.html"

with open(file, 'r') as f:
    html_string = f.read()

parsed_file = str(bs(html_string, 'html.parser'))

start_date = '2016-03-17 10:55:00'
end_date = '2016-03-17 10:56:00'


# write a function that takes the file name as a parameter
def get_messages(html_file):
    # div class that always precedes a message
    div_class = "_3-96 _2pio _2lek _2lel"

    # skip first message since it isn't an actual message
    messages = re.finditer(div_class, html_file)
    next(messages)

    # create dictionary to store messages
    mess_dict = {}
    # starting number for dictionary
    x = 0
    for m in messages:
        # find date of message
        date_end = m.start() - 79
        cut_date = parsed_file[:date_end]
        date_start = cut_date.rfind("2lem") + 6
        date_time = cut_date[date_start:]

        # convert to standard date time
        date_time = datetime.strptime(date_time, "%b %d, %Y, %I:%M %p")
        date_time = str(date_time)

        # find name of message sender
        name_start = m.start() + 25
        cut_name = parsed_file[name_start:]
        name_end = cut_name.find("</div>")
        name = cut_name[0:name_end]

        # find message
        cut_message = cut_name[name_end + 52:]
        message_end = cut_message.find("</div>")
        message = cut_message[:message_end]

        message_tuple = date_time, name, message
        mess_dict[x] = message_tuple
        x += 1
    return mess_dict


def find_sender_count():
    mess_dict = get_messages(parsed_file)
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

    print(parsed_file.title())

    chart_title = re.search('<title>(.*)</title>', parsed_file)
    chart_title = (chart_title.group(1))
    chart_title = "Number of Messages Sent in " + chart_title + '\n' + " from " + start_date.split(' ')[0] + " to " + end_date.split(' ')[0]
    # set x access
    keys = name_list.keys()
    # set y access
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
