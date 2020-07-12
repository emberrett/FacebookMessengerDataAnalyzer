from datetime import datetime  # for handling dates and time
from datetime import timezone  # for handling timezones
import matplotlib.pyplot as plt  # library for plotting data
import operator  # to convert dictionary to list
from tkinter import filedialog  # for file selection UI
from tkinter import *  # for UI
import json  # for handling json
import os  # library for handling paths
from collections import Counter  # for counting words
import csv  # for exporting data

# keeps root window closed
root = Tk()
root.withdraw()

# ask user to select file
folder = filedialog.askdirectory(title="Select Folder")
folder_name = os.path.basename(os.path.normpath(folder)).split("_")[0]
start_datetime = 'Jul 12 2019  12:00AM'
end_datetime = 'Jul 12 2020  12:59PM'

# set color of charts
primary_color = '#343837'
secondary_color = '#001146'
tertiary_color = 'white'

# people you want to exclude from your data
exclude_list = []

# words you want to exclude from you word count data
word_exclude_list = ["I", "You", "the", "to", "a", "is", "and", "of", "that", "you", "in", "it", "so", "for", "my",
                     "this", "are", "on", "just", "have", "was", "like", "we", "be", "Oh", "at", "with", "but", "he",
                     "all", "And", "about", "me", "So", "not", "not", "one", "they", "what", "The", ".", "get", "I",
                     "from", "will", "up", "I'm", "an", "your", "do", "really", "out", "it's", "as", "Hahahahaha",
                     "his", "or", "if", "i", "going", "We", "there", "Hahahaha", "has", "our", "when",
                     "some", "can", "Ha", "oh", "had", "see", "that's", "Hahaha", "This", "would", "ha", "no",
                     "got", "That", "how", "What", "But", "were", "him", "more", "now", "did", "right", "been", "Yeah",
                     "don't", "It", "them", "by", "It's", "too", "ha!", "HAHAHAHA", "because", "That's", "her", "who",
                     "Haha", "haha", "He", "go", "Just", "I've", "Iâm", "it.", "she", "HAHAHA", "where", "very",
                     "HAHAHAHAHA", "into", "these", "than", "A", "They", "can't", "am", "Also"]
# how many words to show in the most used words functions
most_common_count = 100


# write a function that takes the file name as a parameter
def get_textual_messages():
    mess_dict = {}
    x = 0
    for file in os.listdir(folder):
        if file.endswith(".json"):
            file_path = os.path.realpath(folder) + "\\" + str(file)
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
    return mess_dict


def get_all_messages():
    mess_dict = {}
    x = 0
    for file in os.listdir(folder):
        if file.endswith(".json"):
            file_path = os.path.realpath(folder) + "\\" + str(file)
            # open json file in read mode
            with open(file_path, "r") as read_file:
                data = json.load(read_file)
            # starting number for dictionary
            for message in data['messages']:
                # find time of message
                message_timestamp = message['timestamp_ms']

                # find message sender
                message_sender = message['sender_name']

                message_tuple = message_timestamp, message_sender
                mess_dict[x] = message_tuple
                x += 1
    print(mess_dict)
    return mess_dict


def find_sender_count_date_range(start, end):
    mess_dict = get_all_messages()
    count_dict = {}

    # convert start date+time to datetime, then timestamp as integer
    start_datetime_dt = datetime.strptime(start, '%b %d %Y %I:%M%p')
    start_datetime_ts = int(start_datetime_dt.replace(tzinfo=timezone.utc).timestamp()) * 1000

    # convert end date+time to datetime, then timestamp as integer
    end_datetime_dt = datetime.strptime(end, '%b %d %Y %I:%M%p')
    end_datetime_ts = int(end_datetime_dt.replace(tzinfo=timezone.utc).timestamp()) * 1000

    # put names here that you want to exclude
    # get unique names in messages
    for x in mess_dict:
        if mess_dict[x][1] not in exclude_list:
            y = mess_dict[x][1]
        # if name is not in name list, add it and set the value to 0
        if y not in count_dict:
            count_dict[y] = 0
            # check if message is in date range
        if start_datetime_ts <= mess_dict[x][0] <= end_datetime_ts:
            count_dict[y] += 1

    # creates nwe formatted dict with first name and last initial
    formatted_count = {}
    for x in count_dict.keys():
        name_split = x.split(" ")
        formatted_name = name_split[0] + " " + name_split[-1][:1]
        formatted_count[formatted_name] = count_dict[x]

    # sort dictionary by descending order
    formatted_count = dict(sorted(formatted_count.items(), key=operator.itemgetter(1), reverse=True))

    chart_title = "Number of Messages Sent in " + folder_name + '\n' + " from " + start + " to " + end
    # set x axis
    keys = formatted_count.keys()
    print(keys)
    # set y axis
    values = formatted_count.values()
    print(values)

    # create chart
    # set width of bars
    bar_width = .4
    # create chart
    fig, ax = plt.subplots()
    # set background color
    fig.patch.set_facecolor(primary_color)
    ax.set_facecolor(primary_color)

    # change color of chart borders
    ax.spines['bottom'].set_color(tertiary_color)
    ax.spines['top'].set_color(tertiary_color)
    ax.spines['left'].set_color(tertiary_color)
    ax.spines['right'].set_color(tertiary_color)

    # set color of labels
    ax.xaxis.label.set_color(tertiary_color)
    ax.yaxis.label.set_color(tertiary_color)

    # set color of ticks
    ax.tick_params(axis='x', colors=tertiary_color)
    ax.tick_params(axis='y', colors=tertiary_color)

    # set title and styling of title
    plt.title(chart_title, fontsize=20, color=tertiary_color)

    # set bars to variable
    bars = plt.bar(keys, values, color=secondary_color, width=bar_width)

    # get height of largest bar
    highest_bar = max(values)

    # assign your bars to a variable so their attributes can be accessed
    plt.xticks(fontsize=20)
    plt.xticks(rotation=-90)
    plt.yticks(fontsize=20)
    plt.subplots_adjust(bottom=0.3)

    # access the bar attributes to place the text in the appropriate location
    for bar in bars:
        bar_height = bar.get_height()
        label_height = bar_height - (.1 * bar_height)
        # if label would not fit in axis, put label above it
        if bar_height < label_height - (bar_height - (bar_height * .1)):
            label_height = bar_height + (.1 * bar_height)
        plt.text(bar.get_x() + (bar_width / 2), label_height, bar_height, color=tertiary_color,
                 horizontalalignment='center')
    plt.show()


def find_sender_count_total():
    mess_dict = get_all_messages()
    count_dict = {}

    # get unique names in messages
    for x in mess_dict:
        if mess_dict[x][1] not in exclude_list:
            y = mess_dict[x][1]
        # if name is not in name list, add it and set the value to 0
        if y not in count_dict:
            count_dict[y] = 0
            # check if message is in date range
        count_dict[y] += 1

    # creates nwe formatted dict with first name and last initial
    formatted_count = {}
    for x in count_dict.keys():
        name_split = x.split(" ")
        formatted_name = name_split[0] + " " + name_split[-1][:1]
        formatted_count[formatted_name] = count_dict[x]

    # sort dictionary by descending order
    formatted_count = dict(sorted(formatted_count.items(), key=operator.itemgetter(1), reverse=True))

    chart_title = "Number of Messages Sent in " + folder_name + '\n' + " All Time"
    # set x axis
    keys = formatted_count.keys()
    # set y axis
    values = formatted_count.values()

    # set width of bars
    bar_width = .4
    # create chart
    fig, ax = plt.subplots()
    # set background color
    fig.patch.set_facecolor(primary_color)
    ax.set_facecolor(primary_color)

    # change color of chart borders
    ax.spines['bottom'].set_color(tertiary_color)
    ax.spines['top'].set_color(tertiary_color)
    ax.spines['left'].set_color(tertiary_color)
    ax.spines['right'].set_color(tertiary_color)

    # set color of labels
    ax.xaxis.label.set_color(tertiary_color)
    ax.yaxis.label.set_color(tertiary_color)

    # set color of ticks
    ax.tick_params(axis='x', colors=tertiary_color)
    ax.tick_params(axis='y', colors=tertiary_color)

    # set title and styling of title
    plt.title(chart_title, fontsize=20, color=tertiary_color)

    # set bars to variable
    bars = plt.bar(keys, values, color=secondary_color, width=bar_width)

    # get height of largest bar
    highest_bar = max(values)

    # assign your bars to a variable so their attributes can be accessed
    plt.xticks(fontsize=20)
    plt.xticks(rotation=-90)
    plt.yticks(fontsize=20)
    plt.subplots_adjust(bottom=0.3)

    # access the bar attributes to place the text in the appropriate location
    for bar in bars:
        bar_height = bar.get_height()
        label_height = bar_height - (.1 * bar_height)
        # if label would not fit in axis, put label above it
        if bar_height < label_height - (bar_height - (bar_height * .1)):
            label_height = bar_height + (.1 * bar_height)
        plt.text(bar.get_x() + (bar_width / 2), label_height, bar_height, color=tertiary_color,
                 horizontalalignment='center')
    plt.show()


def find_character_count_total():
    mess_dict = get_textual_messages()
    count_dict = {}

    # get unique names in messages
    for x in mess_dict:
        if mess_dict[x][1] not in exclude_list:
            y = mess_dict[x][1]
        # if name is not in name list, add it and set the value to 0
        if y not in count_dict:
            count_dict[y] = 0
            # check if message is in date range
        count_dict[y] += len(mess_dict[x][2])

    # creates nwe formatted dict with first name and last initial
    formatted_count = {}
    for x in count_dict.keys():
        name_split = x.split(" ")
        formatted_name = name_split[0] + " " + name_split[-1][:1]
        formatted_count[formatted_name] = count_dict[x]

    # sort dictionary by descending order
    formatted_count = dict(sorted(formatted_count.items(), key=operator.itemgetter(1), reverse=True))

    chart_title = "Number of Characters Sent in " + folder_name + '\n' + " All Time"
    # set x axis
    keys = formatted_count.keys()
    # set y axis
    values = formatted_count.values()

    # set width of bars
    bar_width = .4
    # create chart
    fig, ax = plt.subplots()
    # set background color
    fig.patch.set_facecolor(primary_color)
    ax.set_facecolor(primary_color)

    # change color of chart borders
    ax.spines['bottom'].set_color(tertiary_color)
    ax.spines['top'].set_color(tertiary_color)
    ax.spines['left'].set_color(tertiary_color)
    ax.spines['right'].set_color(tertiary_color)

    # set color of labels
    ax.xaxis.label.set_color(tertiary_color)
    ax.yaxis.label.set_color(tertiary_color)

    # set color of ticks
    ax.tick_params(axis='x', colors=tertiary_color)
    ax.tick_params(axis='y', colors=tertiary_color)

    # set title and styling of title
    plt.title(chart_title, fontsize=20, color=tertiary_color)

    # set bars to variable
    bars = plt.bar(keys, values, color=secondary_color, width=bar_width)

    # get height of largest bar
    highest_bar = max(values)

    # assign your bars to a variable so their attributes can be accessed
    plt.xticks(fontsize=20)
    plt.xticks(rotation=-90)
    plt.yticks(fontsize=20)
    plt.subplots_adjust(bottom=0.3)

    # access the bar attributes to place the text in the appropriate location
    for bar in bars:
        bar_height = bar.get_height()
        label_height = bar_height - (.1 * bar_height)
        # if label would not fit in axis, put label above it
        if bar_height < label_height - (bar_height - (bar_height * .1)):
            label_height = bar_height + (.1 * bar_height)
        plt.text(bar.get_x() + (bar_width / 2), label_height, bar_height, color=tertiary_color,
                 horizontalalignment='center')
    plt.show()


def find_character_count_date_range(start, end):
    mess_dict = get_textual_messages()
    count_dict = {}

    # convert start date+time to datetime, then timestamp as integer
    start_datetime_dt = datetime.strptime(start, '%b %d %Y %I:%M%p')
    start_datetime_ts = int(start_datetime_dt.replace(tzinfo=timezone.utc).timestamp()) * 1000

    # convert end date+time to datetime, then timestamp as integer
    end_datetime_dt = datetime.strptime(end, '%b %d %Y %I:%M%p')
    end_datetime_ts = int(end_datetime_dt.replace(tzinfo=timezone.utc).timestamp()) * 1000

    # put names here that you want to exclude
    # get unique names in messages
    for x in mess_dict:
        if mess_dict[x][1] not in exclude_list:
            y = mess_dict[x][1]
        # if name is not in name list, add it and set the value to 0
        if y not in count_dict:
            count_dict[y] = 0
            # check if message is in date range
        if start_datetime_ts <= mess_dict[x][0] <= end_datetime_ts:
            count_dict[y] += len(mess_dict[x][2])

    # creates nwe formatted dict with first name and last initial
    formatted_count = {}
    for x in count_dict.keys():
        name_split = x.split(" ")
        formatted_name = name_split[0] + " " + name_split[-1][:1]
        formatted_count[formatted_name] = count_dict[x]

    # sort dictionary by descending order
    formatted_count = dict(sorted(formatted_count.items(), key=operator.itemgetter(1), reverse=True))

    chart_title = "Number of Characters Sent in " + folder_name + '\n' + " from " + start + " to " + end
    # set x axis
    keys = formatted_count.keys()
    print(keys)
    # set y axis
    values = formatted_count.values()
    print(values)

    # create chart
    # set width of bars
    bar_width = .4
    # create chart
    fig, ax = plt.subplots()
    # set background color
    fig.patch.set_facecolor(primary_color)
    ax.set_facecolor(primary_color)

    # change color of chart borders
    ax.spines['bottom'].set_color(tertiary_color)
    ax.spines['top'].set_color(tertiary_color)
    ax.spines['left'].set_color(tertiary_color)
    ax.spines['right'].set_color(tertiary_color)

    # set color of labels
    ax.xaxis.label.set_color(tertiary_color)
    ax.yaxis.label.set_color(tertiary_color)

    # set color of ticks
    ax.tick_params(axis='x', colors=tertiary_color)
    ax.tick_params(axis='y', colors=tertiary_color)

    # set title and styling of title
    plt.title(chart_title, fontsize=20, color=tertiary_color)

    # set bars to variable
    bars = plt.bar(keys, values, color=secondary_color, width=bar_width)

    # get height of largest bar
    highest_bar = max(values)

    # assign your bars to a variable so their attributes can be accessed
    plt.xticks(fontsize=20)
    plt.xticks(rotation=-90)
    plt.yticks(fontsize=20)
    plt.subplots_adjust(bottom=0.3)

    # access the bar attributes to place the text in the appropriate location
    for bar in bars:
        bar_height = bar.get_height()
        label_height = bar_height - (.1 * bar_height)
        # if label would not fit in axis, put label above it
        if bar_height < label_height - (bar_height - (bar_height * .1)):
            label_height = bar_height + (.1 * bar_height)
        plt.text(bar.get_x() + (bar_width / 2), label_height, bar_height, color=tertiary_color,
                 horizontalalignment='center')
    plt.show()


def find_most_used_words():
    mess_dict = get_textual_messages()
    count_dict = {}
    # get unique names in messages
    all_words = []
    for x in mess_dict:
        if mess_dict[x][1] not in exclude_list:
            split_words = mess_dict[x][2].split()
            for w in split_words:
                if "âs" in str(w):
                    w = w.replace("â", "'")
                all_words.append(w)

    # count words in word list
    counted_words = Counter(all_words)

    # remove words that are in teh exclude list
    for w in word_exclude_list:
        if w in counted_words:
            del counted_words[w]

    # get top (specified number) of most common words
    most_occur = counted_words.most_common(most_common_count)

    # convert to standard dict
    most_occur = dict(most_occur)

    # set default file to csv
    file_types = [('CSV', '*.csv')]
    # open dialog to safe file
    csv_file = filedialog.asksaveasfile(type='a', filetypes=file_types, defaultextension=csv)
    # set file path to variable
    csv_file = csv_file.name
    # write dictionary of words to csv file
    with open(csv_file, 'w', newline='', encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        for key, value in most_occur.items():
            print(key, value)
            writer.writerow([key, value])


# uncomment a function below to run it

# find_sender_count_date_range(start_datetime, end_datetime)

# find_sender_count_total()


# find_character_count_total()

# find_character_count_date_range(start_datetime, end_datetime)

find_most_used_words()
