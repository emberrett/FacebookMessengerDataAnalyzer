from analysis import (
    view_most_used_words, 
    view_total_messages_sent_by_each_member, 
    view_total_characters_sent_by_each_member,
    message_count_by_month,
    find_total_usage_for_each_specified_word,
    find_average_message_length_for_each_member
    
    )
from config import START_DATETIME, END_DATETIME

# view_total_messages_sent_by_each_member(date_range=True, start=START_DATETIME, end=END_DATETIME)

# view_total_characters_sent_by_each_member(date_range=True,start=START_DATETIME,end=END_DATETIME)

# view_most_used_words(100)

# find_total_usage_for_each_specified_word(['damn'],date_range=True,start=START_DATETIME,end=END_DATETIME)

# find_average_message_length_for_each_member(date_range=True,start=START_DATETIME,end=END_DATETIME)

message_count_by_month(date_range=True, start=START_DATETIME, end=END_DATETIME)

