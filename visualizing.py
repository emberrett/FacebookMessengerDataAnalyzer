import matplotlib.pyplot as plt
import numpy as np


def show_bar_chart(keys, values, PRIMARY_COLOR, SECONDARY_COLOR, TERTIARY_COLOR, chart_title, bar_width=.4):
    fig, ax = plt.subplots()
    fig.patch.set_facecolor(PRIMARY_COLOR)
    ax.set_facecolor(PRIMARY_COLOR)

    ax.spines['bottom'].set_color(TERTIARY_COLOR)
    ax.spines['top'].set_color(TERTIARY_COLOR)
    ax.spines['left'].set_color(TERTIARY_COLOR)
    ax.spines['right'].set_color(TERTIARY_COLOR)

    ax.xaxis.label.set_color(TERTIARY_COLOR)
    ax.yaxis.label.set_color(TERTIARY_COLOR)

    ax.tick_params(axis='x', colors=TERTIARY_COLOR)
    ax.tick_params(axis='y', colors=TERTIARY_COLOR)

    plt.title(chart_title, fontsize=20, color=TERTIARY_COLOR)

    bars = plt.bar(keys, values, color=SECONDARY_COLOR, width=bar_width)

    plt.xticks(fontsize=20)
    plt.xticks(rotation=-90)
    plt.yticks(fontsize=20)
    plt.subplots_adjust(bottom=0.3)

    for bar in bars:
        bar_height = bar.get_height()
        label_height = bar_height - (.1 * bar_height)

        if bar_height < label_height - (bar_height - (bar_height * .1)):
            label_height = bar_height + (.1 * bar_height)
        plt.text(bar.get_x() + (bar_width / 2), label_height, bar_height, color=TERTIARY_COLOR,
                 horizontalalignment='center')
    plt.show()


def show_line_chart(keys, values, PRIMARY_COLOR, TERTIARY_COLOR, chart_title):
    fig, ax = plt.subplots()

    fig.patch.set_facecolor(PRIMARY_COLOR)
    ax.set_facecolor(PRIMARY_COLOR)

    ax.spines['bottom'].set_color(TERTIARY_COLOR)
    ax.spines['top'].set_color(TERTIARY_COLOR)
    ax.spines['left'].set_color(TERTIARY_COLOR)
    ax.spines['right'].set_color(TERTIARY_COLOR)

    ax.xaxis.label.set_color(TERTIARY_COLOR)
    ax.yaxis.label.set_color(TERTIARY_COLOR)

    ax.tick_params(axis='x', colors=TERTIARY_COLOR)
    ax.tick_params(axis='y', colors=TERTIARY_COLOR)

    plt.title(chart_title, fontsize=20, color=TERTIARY_COLOR)

    plt.plot(keys, values, color=TERTIARY_COLOR)

    plt.xticks(fontsize=20)
    plt.xticks(rotation=-90)
    plt.xticks(size=15)
    plt.yticks(fontsize=20)
    plt.subplots_adjust(bottom=0.3)
    plt.xticks(np.arange(0, len(keys), 3))

    plt.show()
