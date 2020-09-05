# FB-Messenger-Data-Analyzer
This Python script runs analysis on Facebook Messenger, based on JSON files provided by Facebook.

You must download your Facebook data in JSON format before running this script. To download your Facebook data:

1. Go to your **facebook.com**
2. Go to **Settings** \&gt; **Your Facebook Information**
3. Click **Download Your Information**
4. Under **Date Range** select **All of my data**
5. Under **Format** select **JSON**
6. Under **Media Quality** select **Low**
7. Select **Create File**
  1. Facebook will notify you via email when your data is ready for download. This usually takes about 24 hours.

The script begins by asking the user to select a folder with JSON data within to run queries on. The messenger files are in your **Facebook data folder** > **messages** > **inbox**.

Run specific queries by uncommenting them at the bottom of  MessengerAnalyzer.py.

Modify the date ranges, appearance, and excluded data which are passed to the query functions at the beginning of the script (see commented code for more details).<br /><br />

**Non-Query Functions**

- **get\_textual\_messages()**
  - Retrieves the timestamp, sender, and mess content from all textual messages in the selected folder and passes them into a dictionary as a tuple.
- **get\_all\_messages()**
  - Retrieves the timestamp and sender from all messages in the selected folder and passes them into a dictionary as a tuple.<br /><br />
  
**Query Functions**

- **find\_sender\_count\_total()**
  - Finds total messages sent by each user in selected message thread and shows the results as a bar graph.
- **find\_sender\_count\_date\_range()**
  - Finds total messages sent by each user in selected message thread within the selected date range **(start, end)** and shows the results as a bar graph.
- **find\_character\_count\_total()**
  - Finds total characters sent by each user in selected message thread and shows the results as a bar graph.
- **find\_character\_count\_date\_range(start,end)**
  - Finds total characters sent by each user in selected message thread within the selected date range **(start, end)** and shows the results as a bar graph.
- **find\_most\_used\_words(most\_common\_count)**
  - Finds most used words in a messenger thread (sorted by most to least). Specify **most\_common\_count** as integer for how many words you want to include in the results. Exports data to csv in user-specified location.
- **single\_word\_usage(chosen\_word)**
  - Finds total uses of specified word **(chosen\_word)** by each user and shows the results as a bar graph.
- **find\_average\_message\_length()**
  - Finds average message length of messages sent by each user and shows the results as a bar graph.
- **message\_count\_by\_month()**
  - Finds the total number of messages sent over time, grouped by month, shown as a line graph with ticks every 3 months starting from the creation of the message thread. <br /><br />

**Required Libraries**

- Datetime
  - datetime
  - timezone
- pyplot
- perator
- tkinter
  - filedialog
- json
- os
- collections
  - Counter
- csv
-numpy
