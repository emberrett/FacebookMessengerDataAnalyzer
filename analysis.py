import operator
import csv
import os
import json
from datetime import datetime
from datetime import timezone
from tkinter import filedialog
from tkinter import *
from collections import Counter
from visualizing import show_bar_chart, show_line_chart
from config import (
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    TERTIARY_COLOR,
    EXCLUDED_MEMBERS,
    EXCLUDED_WORDS,
    INBOX_FOLDER_PATH
)
root = Tk()
root.withdraw()

folder = INBOX_FOLDER_PATH or filedialog.askdirectory(title="Select Folder")
folder_name = os.path.basename(os.path.normpath(folder)).split("_")[0]


def get_textual_messages(date_range=False, start=None, end=None):
    messages = {}
    x = 0

    if date_range:
        start_datetime = datetime.strptime(start, '%b %d %Y %I:%M%p')
        start_datetime_timestamp = int(start_datetime.replace(
            tzinfo=timezone.utc).timestamp()) * 1000

        end_datetime = datetime.strptime(end, '%b %d %Y %I:%M%p')
        end_datetime_timestamp = int(end_datetime.replace(
            tzinfo=timezone.utc).timestamp()) * 1000

    for sub_folder in os.listdir(folder):
        for file in os.listdir(os.path.realpath(folder) + "/" + sub_folder):
            if file.endswith(".json"):
                file_path = os.path.realpath(
                    folder) + "/" + sub_folder + "/" + str(file)
                with open(file_path, "r") as read_file:
                    data = json.load(read_file)
                for message in data['messages']:
                    if 'content' in message:
                        message_content = message['content']

                        message_timestamp = message['timestamp_ms']

                        if date_range:
                            if (start_datetime_timestamp > message_timestamp or message_timestamp > end_datetime_timestamp):
                                continue

                        message_sender = message['sender_name']

                    message_tuple = message_timestamp, message_sender, message_content
                    messages[x] = message_tuple
                    x += 1
    return messages


def get_all_messages(date_range=False, start=None, end=None):
    messages = {}
    x = 0

    if date_range:
        start_datetime = datetime.strptime(start, '%b %d %Y %I:%M%p')
        start_datetime_timestamp = int(start_datetime.replace(
            tzinfo=timezone.utc).timestamp()) * 1000

        end_datetime = datetime.strptime(end, '%b %d %Y %I:%M%p')
        end_datetime_timestamp = int(end_datetime.replace(
            tzinfo=timezone.utc).timestamp()) * 1000

    for sub_folder in os.listdir(folder):
        for file in os.listdir(os.path.realpath(folder) + "/" + sub_folder):
            if file.endswith(".json"):
                file_path = os.path.realpath(
                    folder) + "/" + sub_folder + "/" + str(file)
                with open(file_path, "r") as read_file:
                    data = json.load(read_file)
                for message in data['messages']:
                    message_timestamp = message['timestamp_ms']
                    if date_range:
                        if (start_datetime_timestamp > message_timestamp or message_timestamp > end_datetime_timestamp):
                            continue

                    message_sender = message['sender_name']

                    message_tuple = message_timestamp, message_sender
                    messages[x] = message_tuple
                    x += 1
    return messages


def view_total_messages_sent_by_each_member(date_range=False, start=None, end=None, topN=50):
    messages = get_all_messages()
    word_count_dict = {}

    if date_range:
        start_datetime = datetime.strptime(start, '%b %d %Y %I:%M%p')
        start_datetime_timestamp = int(start_datetime.replace(
            tzinfo=timezone.utc).timestamp()) * 1000

        end_datetime = datetime.strptime(end, '%b %d %Y %I:%M%p')
        end_datetime_timestamp = int(end_datetime.replace(
            tzinfo=timezone.utc).timestamp()) * 1000

    for x in messages:
        if messages[x][1] not in EXCLUDED_MEMBERS:
            y = messages[x][1]
        if y not in word_count_dict:
            word_count_dict[y] = 0
        if date_range:
            if start_datetime_timestamp <= messages[x][0] <= end_datetime_timestamp:
                word_count_dict[y] += 1
        else:
            word_count_dict[y] += 1

    formatted_count = {}
    for x in word_count_dict.keys():
        name_split = x.split(" ")
        formatted_name = name_split[0] + " " + name_split[-1][:1]
        formatted_count[formatted_name] = word_count_dict[x]

    formatted_count = dict(sorted(formatted_count.items(),
                                  key=operator.itemgetter(1), reverse=True))

    if date_range:
        chart_title = "Number of Messages Sent in " + \
            folder_name + '\n' + " from " + start + " to " + end
    else:
        chart_title = "Number of Messages Sent in " + folder_name + '\n' + " All Time"

    keys = list(formatted_count.keys())[:topN]
    values = list(formatted_count.values())[:topN]
    show_bar_chart(keys, values, PRIMARY_COLOR,
                   SECONDARY_COLOR, TERTIARY_COLOR, chart_title)


def view_total_characters_sent_by_each_member(date_range=False, start=None, end=None, topN=50):
    messages = get_textual_messages()
    character_count_dict = {}
    if date_range:
        start_datetime = datetime.strptime(start, '%b %d %Y %I:%M%p')
        start_datetime_timestamp = int(start_datetime.replace(
            tzinfo=timezone.utc).timestamp()) * 1000

        end_datetime = datetime.strptime(end, '%b %d %Y %I:%M%p')
        end_datetime_timestamp = int(end_datetime.replace(
            tzinfo=timezone.utc).timestamp()) * 1000

    for x in messages:
        if messages[x][1] not in EXCLUDED_MEMBERS:
            y = messages[x][1]
        if y not in character_count_dict:
            character_count_dict[y] = 0
        if date_range:
            if start_datetime_timestamp <= messages[x][0] <= end_datetime_timestamp:
                character_count_dict[y] += len(messages[x][2])
        else:
            character_count_dict[y] += len(messages[x][2])

    formatted_count = {}
    for x in character_count_dict.keys():
        name_split = x.split(" ")
        formatted_name = name_split[0] + " " + name_split[-1][:1]
        formatted_count[formatted_name] = character_count_dict[x]

    formatted_count = dict(sorted(formatted_count.items(),
                                  key=operator.itemgetter(1), reverse=True))

    if date_range:
        chart_title = "Number of Characters Sent in " + \
            folder_name + '\n' + " from " + start + " to " + end
    else:
        chart_title = "Number of Characters Sent in " + folder_name + '\n' + " All Time"

    keys = list(formatted_count.keys())[:topN]
    values = list(formatted_count.values())[:topN]

    show_bar_chart(keys, values, PRIMARY_COLOR,
                   SECONDARY_COLOR, TERTIARY_COLOR, chart_title)


def view_most_used_words(limit, date_range=False, start=None, end=None):
    messages = get_textual_messages()
    all_words = []

    if date_range:
        start_datetime = datetime.strptime(start, '%b %d %Y %I:%M%p')
        start_datetime_timestamp = int(start_datetime.replace(
            tzinfo=timezone.utc).timestamp()) * 1000

        end_datetime = datetime.strptime(end, '%b %d %Y %I:%M%p')
        end_datetime_timestamp = int(end_datetime.replace(
            tzinfo=timezone.utc).timestamp()) * 1000

    for x in messages:
        if date_range:
            if not (start_datetime_timestamp <= messages[x][0] <= end_datetime_timestamp):
                continue
        if messages[x][1] not in EXCLUDED_MEMBERS:
            split_words = messages[x][2].split()
            for w in split_words:
                if "âs" in str(w):
                    w = w.replace("â", "'")
                all_words.append(w)

    counted_words = Counter(all_words)

    for w in EXCLUDED_WORDS:
        if w.lower() in counted_words:
            del counted_words[w]

    most_common_words = counted_words.most_common(limit)

    most_common_words = dict(most_common_words)

    fileTypes = [('CSV', '*.csv')]
    csvFile = filedialog.asksaveasfile(
        type='a', filetypes=fileTypes, defaultextension=csv)
    csvFile = csvFile.name
    if date_range:
        header = f"Top {limit} Words Used in {folder_name} from {start} to  {end}"
    else:
        header = f"Top {limit} Words Used in {folder_name} All Time"
    with open(csvFile, 'w', newline='', encoding="utf-8") as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(header)
        for key, value in most_common_words.items():
            writer.writerow([key, value])


def find_total_usage_for_each_specified_word(chosed_words, date_range=False, start=None, end=None):
    messages = get_textual_messages()
    count_dict = {}

    if date_range:
        start_datetime = datetime.strptime(start, '%b %d %Y %I:%M%p')
        start_datetime_timestamp = int(start_datetime.replace(
            tzinfo=timezone.utc).timestamp()) * 1000

        end_datetime = datetime.strptime(end, '%b %d %Y %I:%M%p')
        end_datetime_timestamp = int(end_datetime.replace(
            tzinfo=timezone.utc).timestamp()) * 1000

    for x in messages:
        if date_range:
            if not (start_datetime_timestamp <= messages[x][0] <= end_datetime_timestamp):
                continue
        if messages[x][1] not in EXCLUDED_MEMBERS:
            y = messages[x][1]
        if y not in count_dict:
            count_dict[y] = 0
        for w in chosed_words:
            if w.lower() in messages[x][2].lower():
                count_dict[y] += 1

    formatted_count = {}
    for x in count_dict.keys():
        name_split = x.split(" ")
        formatted_name = name_split[0] + " " + name_split[-1][:1]
        formatted_count[formatted_name] = count_dict[x]

    formatted_count = dict(sorted(formatted_count.items(),
                                  key=operator.itemgetter(1), reverse=True))

    if date_range:
        chart_title = "Total Usage of the Following Words " + " in " + folder_name + '\n' + " from " \
            + start + " to " + end + ":" + '\n' + str(chosed_words)
    else:
        chart_title = "Total Usage of the Following Words " + " in " + \
            folder_name + " All Time:" + '\n' + str(chosed_words)
    keys = formatted_count.keys()
    values = formatted_count.values()

    show_bar_chart(keys, values, PRIMARY_COLOR,
                   SECONDARY_COLOR, TERTIARY_COLOR, chart_title)


def find_average_message_length_for_each_member(date_range=False, start=None, end=None, topN=50, minMessages=10):
    messages = get_textual_messages()
    character_count_dict = {}
    message_count_dict = {}

    if date_range:
        # convert start date+time to datetime, then timestamp as integer
        start_datetime = datetime.strptime(start, '%b %d %Y %I:%M%p')
        start_datetime_timestamp = int(start_datetime.replace(
            tzinfo=timezone.utc).timestamp()) * 1000

        # convert end date+time to datetime, then timestamp as integer
        end_datetime = datetime.strptime(end, '%b %d %Y %I:%M%p')
        end_datetime_timestamp = int(end_datetime.replace(
            tzinfo=timezone.utc).timestamp()) * 1000

    # get unique names in messages
    for x in messages:
        if date_range:
            if not (start_datetime_timestamp <= messages[x][0] <= end_datetime_timestamp):
                continue
        if messages[x][1] not in EXCLUDED_MEMBERS:
            y = messages[x][1]
        # if name is not in name list, add it and set the value to 0
        if y not in character_count_dict:
            character_count_dict[y] = 0
            message_count_dict[y] = 0
            # check if message is in date range
        character_count_dict[y] += len(messages[x][2])
        message_count_dict[y] += 1
    average_character_count = {}
    for c in character_count_dict.keys():
        if message_count_dict[c] < minMessages:
            continue

        average_key = c
        average_value = character_count_dict[c] / message_count_dict[c]
        average_value = round(average_value, 2)
        average_character_count[average_key] = average_value
    # creates nwe formatted dict with first name and last initial
    formatted_count = {}
    for x in average_character_count.keys():
        name_split = x.split(" ")
        formatted_name = name_split[0] + " " + name_split[-1]
        formatted_count[formatted_name] = average_character_count[x]

    formatted_count = dict(sorted(formatted_count.items(),
                                  key=operator.itemgetter(1), reverse=True))

    if date_range:
        chart_title = "Average Length of Message Per Person in " + folder_name + '\n' + " from" \
            + start + " to " + end
    else:
        chart_title = "Average Length of Message Per Person in " + \
            folder_name + '\n' + " All Time"

    keys = list(formatted_count.keys())[:topN]
    values = list(formatted_count.values())[:topN]

    show_bar_chart(keys, values, PRIMARY_COLOR,
                   SECONDARY_COLOR, TERTIARY_COLOR, chart_title)


def message_count_by_month(date_range=False, start=None, end=None):
    messages = get_all_messages(date_range, start, end)
    month_list = []

    if date_range:
        start_datetime = datetime.strptime(start, '%b %d %Y %I:%M%p')
        start_datetime_timestamp = int(start_datetime.replace(
            tzinfo=timezone.utc).timestamp()) * 1000

        end_datetime = datetime.strptime(end, '%b %d %Y %I:%M%p')
        end_datetime_timestamp = int(end_datetime.replace(
            tzinfo=timezone.utc).timestamp()) * 1000

    if messages == {}:
        print("No messages found")
        return

    for x in messages:
        if date_range:
            if not (start_datetime_timestamp <= messages[x][0] <= end_datetime_timestamp):
                continue
        timestamp = int(messages[x][0]) / 1000
        dt = datetime.fromtimestamp(timestamp)
        message_date = f"{dt.year}-{dt.month}"
        if message_date not in month_list:
            month_list.append(message_date)

    month_list = sorted(month_list, key=lambda x: (
        int(x.split("-")[0]), int(x.split("-")[-1])))

    firstMonth = month_list[0]
    last_month = month_list[-1]
    end_month = int(month_list[-1].split("-")[-1])
    end_year = int(last_month.split("-")[0])

    year_iter = int(firstMonth.split("-")[0])
    month_iter = int(firstMonth.split("-")[-1])

    new_month_list = []
    while year_iter <= end_year:
        added_date = str(year_iter) + "-" + str(month_iter)
        new_month_list.append(added_date)
        month_iter += 1
        if month_iter > 12:
            year_iter += 1
            month_iter = 1
        if month_iter > end_month and year_iter >= end_year:
            break

    month_counts = []

    for m in new_month_list:
        month_counts.append(0)

    for x in messages:
        timestamp = int(messages[x][0]) / 1000
        dt = datetime.fromtimestamp(timestamp)
        message_date = f"{dt.year}-{dt.month}"
        month_counts[(new_month_list.index(message_date))] += 1

    if date_range:
        chart_title = "Messages Sent in " + folder_name + '\n' + " from " \
            + start + " to " + end
    else:
        chart_title = "Messages Sent in " + folder_name + '\n' + " All Time"

    keys = new_month_list
    values = month_counts
    show_bar_chart(keys, values, PRIMARY_COLOR,
                   SECONDARY_COLOR, TERTIARY_COLOR, chart_title)
