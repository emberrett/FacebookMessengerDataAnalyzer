from datetime import datetime
from datetime import timezone
import matplotlib.pyplot as plt  # library for plotting data
import operator  # to convert dictionary to list
from tkinter import filedialog  # for file selection UI
from tkinter import *  # for UI
import json  # for handling json
import os  # library for handling paths
from collections import Counter  # for counting words
from collections import OrderedDict
import csv  # for exporting data
import numpy as np

# keeps root window closed
root = Tk()
root.withdraw()

# ask user to select file
folder = filedialog.askdirectory(title="Select Folder")
folder_name = os.path.basename(os.path.normpath(folder)).split("_")[0]

# sets data range for results
startDT = 'Jan 1 2021  12:00AM'
endDT = 'Dec 31 2021  11:59PM'

# set color of charts
primaryColor = '#504f4f'
secondaryColor = '#cf8121'
tertiaryColor = 'white'

# people you want to exclude from your data
excludeList = ['Chavis Landman']

# words you want to exclude from you word count data, add new words in lower case
wordExcludeList = ['i', 'really', 'was', 'did', 'im', 'got', 'who', 'hahahahaha', 'one', 'if', 'they', 'do', 'in',
                   'haha', 'at', 'has', 'with', 'me', 'right', 'like', 'will', 'your', 'and', "i've", 'some', 'were',
                   'how', 'not', 'his', 'for', 'you', 'of', 'hahahaha', 'am', 'been', 'by', 'there', 'up', 'my', 'ha!',
                   'when', 'this', 'from', 'an', 'we', 'these', 'them', '.', 'all', 'just', 'hahaha', 'oh', 'are',
                   'because', 'into', 'yeah', 'a', 'can', 'her', "can't", 'than', 'be', 'going', 'now', 'it', 'more',
                   'where', 'he', 'what', "it's", 'as', 'go', "i'm", 'very', 'about', 'have', 'no', 'or', 'it.', 'ha',
                   'had', "don't", 'out', 'on', 'she', 'so', 'get', 'is', 'that', 'him', "that's", 'to', 'i', 'but',
                   'also', 'the', 'our', 'too', 'see', 'would', 'and', 'so']


def showBarChart(keys, values, primaryColor, secondaryColor, tertiaryColor, chartTitle, barWidth=.4):
    # create chart
    fig, ax = plt.subplots()
    # set background color
    fig.patch.set_facecolor(primaryColor)
    ax.set_facecolor(primaryColor)

    # change color of chart borders
    ax.spines['bottom'].set_color(tertiaryColor)
    ax.spines['top'].set_color(tertiaryColor)
    ax.spines['left'].set_color(tertiaryColor)
    ax.spines['right'].set_color(tertiaryColor)

    # set color of labels
    ax.xaxis.label.set_color(tertiaryColor)
    ax.yaxis.label.set_color(tertiaryColor)

    # set color of ticks
    ax.tick_params(axis='x', colors=tertiaryColor)
    ax.tick_params(axis='y', colors=tertiaryColor)

    # set title and styling of title
    plt.title(chartTitle, fontsize=20, color=tertiaryColor)

    # set bars to variable
    bars = plt.bar(keys, values, color=secondaryColor, width=barWidth)

    # get height of largest bar
    highest_bar = max(values)

    # assign your bars to a variable so their attributes can be accessed
    plt.xticks(fontsize=20)
    plt.xticks(rotation=-90)
    plt.yticks(fontsize=20)
    plt.subplots_adjust(bottom=0.3)

    # access the bar attributes to place the text in the appropriate location
    for bar in bars:
        barHeight = bar.get_height()
        labelHeight = barHeight - (.1 * barHeight)
        # if label would not fit in axis, put label above it
        if barHeight < labelHeight - (barHeight - (barHeight * .1)):
            labelHeight = barHeight + (.1 * barHeight)
        plt.text(bar.get_x() + (barWidth / 2), labelHeight, barHeight, color=tertiaryColor,
                 horizontalalignment='center')
    plt.show()


def showLineChart(keys, values, primaryColor, tertiaryColor, chartTitle):
    # create chart
    fig, ax = plt.subplots()
    # set background color
    fig.patch.set_facecolor(primaryColor)
    ax.set_facecolor(primaryColor)

    # change color of chart borders
    ax.spines['bottom'].set_color(tertiaryColor)
    ax.spines['top'].set_color(tertiaryColor)
    ax.spines['left'].set_color(tertiaryColor)
    ax.spines['right'].set_color(tertiaryColor)

    # set color of labels
    ax.xaxis.label.set_color(tertiaryColor)
    ax.yaxis.label.set_color(tertiaryColor)

    # set color of ticks
    ax.tick_params(axis='x', colors=tertiaryColor)
    ax.tick_params(axis='y', colors=tertiaryColor)

    # set title and styling of title
    plt.title(chartTitle, fontsize=20, color=tertiaryColor)

    # set bars to variable
    plt.plot(keys, values, color=tertiaryColor)

    # assign your bars to a variable so their attributes can be accessed
    plt.xticks(fontsize=20)
    plt.xticks(rotation=-90)
    plt.xticks(size=15)
    plt.yticks(fontsize=20)
    plt.subplots_adjust(bottom=0.3)
    plt.xticks(np.arange(0, len(keys), 3))

    # access the bar attributes to place the text in the appropriate location
    plt.show()


# write a function that takes the file name as a parameter
def getTextualMessages():
    messDict = {}
    x = 0
    # finds all files in selected folder that have json extensions
    for file in os.listdir(folder):
        if file.endswith(".json"):
            # add file name to location to create full path
            filePath = os.path.realpath(folder) + "\\" + str(file)
            # open json file in read mode
            with open(filePath, "r") as read_file:
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
                messDict[x] = message_tuple
                x += 1
    return messDict


def getAllMessages():
    messDict = {}
    x = 0
    # finds all files in selected folder that have json extensions
    for file in os.listdir(folder):
        # add file name to location to create full path
        if file.endswith(".json"):
            filePath = os.path.realpath(folder) + "\\" + str(file)
            # open json file in read mode
            with open(filePath, "r") as read_file:
                data = json.load(read_file)
            # starting number for dictionary
            for message in data['messages']:
                # find time of message
                message_timestamp = message['timestamp_ms']

                # find message sender
                message_sender = message['sender_name']

                message_tuple = message_timestamp, message_sender
                messDict[x] = message_tuple
                x += 1
    return messDict


def findSenderCount(dateRange=False, start=None, end=None):
    messDict = getAllMessages()
    countDict = {}

    if dateRange:
        # convert start date+time to datetime, then timestamp as integer
        startDatetimeDT = datetime.strptime(start, '%b %d %Y %I:%M%p')
        startDatetimeTS = int(startDatetimeDT.replace(tzinfo=timezone.utc).timestamp()) * 1000

        # convert end date+time to datetime, then timestamp as integer
        endDatetimeDT = datetime.strptime(end, '%b %d %Y %I:%M%p')
        endDatetimeTS = int(endDatetimeDT.replace(tzinfo=timezone.utc).timestamp()) * 1000

    # put names here that you want to exclude
    # get unique names in messages
    for x in messDict:
        if messDict[x][1] not in excludeList:
            y = messDict[x][1]
        # if name is not in name list, add it and set the value to 0
        if y not in countDict:
            countDict[y] = 0
            # check if message is in date range
        if dateRange:
            if startDatetimeTS <= messDict[x][0] <= endDatetimeTS:
                countDict[y] += 1
        else:
            countDict[y] += 1

    # creates nwe formatted dict with first name and last initial
    formattedCount = {}
    for x in countDict.keys():
        nameSplit = x.split(" ")
        formattedName = nameSplit[0] + " " + nameSplit[-1][:1]
        formattedCount[formattedName] = countDict[x]

    # sort dictionary by descending order
    formattedCount = dict(sorted(formattedCount.items(), key=operator.itemgetter(1), reverse=True))

    if dateRange:
        chartTitle = "Number of Messages Sent in " + folder_name + '\n' + " from " + start + " to " + end
    else:
        chartTitle = "Number of Messages Sent in " + folder_name + '\n' + " All Time"

    # set x axis
    keys = formattedCount.keys()

    # set y axis
    values = formattedCount.values()

    showBarChart(keys, values, primaryColor, secondaryColor, tertiaryColor, chartTitle)


def findCharacterCount(dateRange=False, start=None, end=None):
    messDict = getTextualMessages()
    countDict = {}

    if dateRange:
        # convert start date+time to datetime, then timestamp as integer
        startDatetimeDT = datetime.strptime(start, '%b %d %Y %I:%M%p')
        startDatetimeTS = int(startDatetimeDT.replace(tzinfo=timezone.utc).timestamp()) * 1000

        # convert end date+time to datetime, then timestamp as integer
        endDatetimeDT = datetime.strptime(end, '%b %d %Y %I:%M%p')
        endDatetimeTS = int(endDatetimeDT.replace(tzinfo=timezone.utc).timestamp()) * 1000

    # put names here that you want to exclude
    # get unique names in messages
    for x in messDict:
        if messDict[x][1] not in excludeList:
            y = messDict[x][1]
        # if name is not in name list, add it and set the value to 0
        if y not in countDict:
            countDict[y] = 0
            # check if message is in date range
        if dateRange:
            if startDatetimeTS <= messDict[x][0] <= endDatetimeTS:
                countDict[y] += len(messDict[x][2])
        else:
            countDict[y] += len(messDict[x][2])

    # creates nwe formatted dict with first name and last initial
    formattedCount = {}
    for x in countDict.keys():
        nameSplit = x.split(" ")
        formattedName = nameSplit[0] + " " + nameSplit[-1][:1]
        formattedCount[formattedName] = countDict[x]

    # sort dictionary by descending order
    formattedCount = dict(sorted(formattedCount.items(), key=operator.itemgetter(1), reverse=True))

    if dateRange:
        chartTitle = "Number of Characters Sent in " + folder_name + '\n' + " from " + start + " to " + end
    else:
        chartTitle = "Number of Characters Sent in " + folder_name + '\n' + " All Time"
    # set x axis
    keys = formattedCount.keys()
    print(keys)
    # set y axis
    values = formattedCount.values()
    print(values)

    showBarChart(keys, values, primaryColor, secondaryColor, tertiaryColor, chartTitle)


def findMostUserWords(mostCommonCount, dateRange=False, start=None, end=None):
    messDict = getTextualMessages()
    # get unique names in messages
    allWords = []

    if dateRange:
        # convert start date+time to datetime, then timestamp as integer
        startDatetimeDT = datetime.strptime(start, '%b %d %Y %I:%M%p')
        startDatetimeTS = int(startDatetimeDT.replace(tzinfo=timezone.utc).timestamp()) * 1000

        # convert end date+time to datetime, then timestamp as integer
        endDatetimeDT = datetime.strptime(end, '%b %d %Y %I:%M%p')
        endDatetimeTS = int(endDatetimeDT.replace(tzinfo=timezone.utc).timestamp()) * 1000

    for x in messDict:
        if dateRange:
            if not (startDatetimeTS <= messDict[x][0] <= endDatetimeTS):
                continue
        if messDict[x][1] not in excludeList:
            split_words = messDict[x][2].split()
            for w in split_words:
                if "âs" in str(w):
                    w = w.replace("â", "'")
                allWords.append(w)

    # count words in word list
    countedWords = Counter(allWords)

    # remove words that are in the exclude list
    for w in wordExcludeList:
        if w.lower() in countedWords:
            del countedWords[w]

    # get top (specified number) of most common words
    mostOccur = countedWords.most_common(mostCommonCount)

    # convert to standard dict
    mostOccur = dict(mostOccur)

    # set default file to csv
    fileTypes = [('CSV', '*.csv')]
    # open dialog to safe file
    csvFile = filedialog.asksaveasfile(type='a', filetypes=fileTypes, defaultextension=csv)
    # set file path to variable
    csvFile = csvFile.name
    # create header:
    if dateRange:
        header = f"Top {mostCommonCount} Words Used in {folder_name} from {start} to  {end}"
    else:
        header = f"Top {mostCommonCount} Words Used in {folder_name} All Time"
    # write dictionary of words to csv file
    with open(csvFile, 'w', newline='', encoding="utf-8") as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(header)
        for key, value in mostOccur.items():
            print(key, value)
            writer.writerow([key, value])


def wordUsage(chosenWords, dateRange=False, start=None, end=None):
    messDict = getTextualMessages()
    countDict = {}
    lowerList = []

    if dateRange:
        # convert start date+time to datetime, then timestamp as integer
        startDatetimeDT = datetime.strptime(start, '%b %d %Y %I:%M%p')
        startDatetimeTS = int(startDatetimeDT.replace(tzinfo=timezone.utc).timestamp()) * 1000

        # convert end date+time to datetime, then timestamp as integer
        endDatetimeDT = datetime.strptime(end, '%b %d %Y %I:%M%p')
        endDatetimeTS = int(endDatetimeDT.replace(tzinfo=timezone.utc).timestamp()) * 1000

    # get unique names in messages
    for x in messDict:
        if dateRange:
            if not (startDatetimeTS <= messDict[x][0] <= endDatetimeTS):
                continue
        if messDict[x][1] not in excludeList:
            y = messDict[x][1]
        # if name is not in name list, add it and set the value to 0
        if y not in countDict:
            countDict[y] = 0
        for w in chosenWords:
            if w.lower() in messDict[x][2].lower():
                countDict[y] += 1

    # creates nwe formatted dict with first name and last initial
    formattedCount = {}
    for x in countDict.keys():
        nameSplit = x.split(" ")
        formattedName = nameSplit[0] + " " + nameSplit[-1][:1]
        formattedCount[formattedName] = countDict[x]

    # sort dictionary by descending order
    formattedCount = dict(sorted(formattedCount.items(), key=operator.itemgetter(1), reverse=True))

    if dateRange:
        chartTitle = "Total Usage of the Following Words " + " in " + folder_name + '\n' + " from " \
                     + start + " to " + end + ":" + '\n' + str(chosenWords)
    else:
        chartTitle = "Total Usage of the Following Words " + " in " + folder_name + " All Time:" + '\n' + str(chosenWords)
    # set x axis
    keys = formattedCount.keys()
    # set y axis
    values = formattedCount.values()

    showBarChart(keys, values, primaryColor, secondaryColor, tertiaryColor, chartTitle)


def findAverageMessageLength(dateRange=False, start=None, end=None):
    messDict = getTextualMessages()
    character_countDict = {}
    message_countDict = {}

    if dateRange:
        # convert start date+time to datetime, then timestamp as integer
        startDatetimeDT = datetime.strptime(start, '%b %d %Y %I:%M%p')
        startDatetimeTS = int(startDatetimeDT.replace(tzinfo=timezone.utc).timestamp()) * 1000

        # convert end date+time to datetime, then timestamp as integer
        endDatetimeDT = datetime.strptime(end, '%b %d %Y %I:%M%p')
        endDatetimeTS = int(endDatetimeDT.replace(tzinfo=timezone.utc).timestamp()) * 1000

    # get unique names in messages
    for x in messDict:
        if dateRange:
            if not (startDatetimeTS <= messDict[x][0] <= endDatetimeTS):
                continue
        if messDict[x][1] not in excludeList:
            y = messDict[x][1]
        # if name is not in name list, add it and set the value to 0
        if y not in character_countDict:
            character_countDict[y] = 0
            message_countDict[y] = 0
            # check if message is in date range
        character_countDict[y] += len(messDict[x][2])
        message_countDict[y] += 1
    average_character_count = {}
    for c in character_countDict.keys():
        average_key = c
        average_value = character_countDict[c] / message_countDict[c]
        average_value = round(average_value, 2)
        average_character_count[average_key] = average_value
    # creates nwe formatted dict with first name and last initial
    formattedCount = {}
    for x in average_character_count.keys():
        nameSplit = x.split(" ")
        formattedName = nameSplit[0] + " " + nameSplit[-1][:1]
        formattedCount[formattedName] = average_character_count[x]

    # sort dictionary by descending order
    formattedCount = dict(sorted(formattedCount.items(), key=operator.itemgetter(1), reverse=True))

    if dateRange:
        chartTitle = "Average Length of Message Per Person in " + folder_name + '\n' + " from" \
                     + start + " to " + end
    else:
        chartTitle = "Average Length of Message Per Person in " + folder_name + '\n' + " All Time"
    # set x axis
    keys = formattedCount.keys()
    # set y axis
    values = formattedCount.values()

    showBarChart(keys, values, primaryColor, secondaryColor, tertiaryColor, chartTitle)


def messageCountByMonth(dateRange=False, start=None, end=None):
    messDict = getAllMessages()
    monthList = []

    if dateRange:
        # convert start date+time to datetime, then timestamp as integer
        startDatetimeDT = datetime.strptime(start, '%b %d %Y %I:%M%p')
        startDatetimeTS = int(startDatetimeDT.replace(tzinfo=timezone.utc).timestamp()) * 1000

        # convert end date+time to datetime, then timestamp as integer
        endDatetimeDT = datetime.strptime(end, '%b %d %Y %I:%M%p')
        endDatetimeTS = int(endDatetimeDT.replace(tzinfo=timezone.utc).timestamp()) * 1000

    for x in messDict:
        if dateRange:
            if not (startDatetimeTS <= messDict[x][0] <= endDatetimeTS):
                continue
        # get timestamp from message
        timestamp = int(messDict[x][0]) / 1000
        # convert time stamp to date time
        dt = datetime.fromtimestamp(timestamp)
        # get month and year from time stamp, and combine them
        messageYear = int(dt.year)
        messageMonth = int(dt.month)
        messageDate = str(messageYear) + "-" + str(messageMonth)
        # add month and year combo to month list if they are not in there already
        if messageDate not in monthList:
            monthList.append(messageDate)

    # the monthList will miss months that had no messages sent, so we need to add them in

    # sort list by year, then month
    monthList = sorted(monthList, key=lambda x: (int(x.split("-")[0]), int(x.split("-")[-1])))
    print(monthList)
    # get the last and first month
    firstMonth = monthList[0]
    # add all months in range
    last_month = monthList[-1]

    # get first/last month/year as integers, to be used for conditionals
    firstMonthOnly = int(firstMonth.split("-")[-1])
    lastMonthOnly = int(last_month.split("-")[-1])
    firstYearOnly = int(firstMonth.split("-")[0])
    lastYearOnly = int(last_month.split("-")[0])

    yearIter = firstYearOnly
    monthIter = firstMonthOnly

    # new month list that will have all months, even ones where no messages are sent
    newMonthList = []
    while yearIter <= lastYearOnly:
        # need to find way to break on last year and month
        added_date = str(yearIter) + "-" + str(monthIter)
        newMonthList.append(added_date)
        monthIter += 1
        if monthIter > 12:
            yearIter += 1
            monthIter = 1
        if monthIter > lastMonthOnly and yearIter >= lastYearOnly:
            break

    monthCounts = []

    # create list with as many entries as there are months in the new month list
    for m in newMonthList:
        monthCounts.append(0)

    # for each message, find the month/year and add it to the month counts relative to where it is in the month list
    for x in messDict:
        # get timestamp from message
        timestamp = int(messDict[x][0]) / 1000
        # convert time stamp to date time
        dt = datetime.fromtimestamp(timestamp)
        # get month and year from time stamp, and combine them
        messageYear = int(dt.year)
        messageMonth = int(dt.month)
        messageDate = str(messageYear) + "-" + str(messageMonth)
        monthCounts[(newMonthList.index(messageDate))] += 1

    # we want the counts to be the total up to that point, not just the total for the month
    # so for each month count after the first, we need to add the value from the previous month
    if dateRange:
        chartTitle = "Messages Sent in " + folder_name + '\n' + " from " \
                     + start + " to " + end
    else:
        chartTitle = "Messages Sent in " + folder_name + '\n' + " All Time"

    # set x axis
    keys = newMonthList
    # set y axis
    values = monthCounts
    showBarChart(keys, values, primaryColor, secondaryColor,tertiaryColor, chartTitle)

# uncomment a function below to run it

# findSenderCount(dateRange=True,start=startDT,end=endDT)

# findCharacterCount(dateRange=True,start=startDT,end=endDT)

# findMostUserWords(100)

# wordUsage(['damn'],dateRange=True,start=startDT,end=endDT)


# findAverageMessageLength(dateRange=True,start=startDT,end=endDT)

# messageCountByMonth(dateRange=True,start=startDT,end=endDT)
