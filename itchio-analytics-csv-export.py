import sys
import os
import json
import csv
from bs4 import BeautifulSoup

"""
This script is a workaround for https://github.com/itchio/itch.io/issues/479
It will take itch.io analytics data from the bar graph on the dashboard and create a csv.

Download html of last 30 days from https://itch.io/dashboard/analytics
Run this script with the path to that page as the first parameter
It will create a itch-analytics.csv in the working directory.
"""

filename = os.path.join(os.getcwd(), "Analytics - itch.io.html")
if len(sys.argv) > 1:
    filename = sys.argv[1]
if not os.path.isfile(filename):
    print(filename +" not found. Download your last 30 days from https://itch.io/dashboard/analytics and pass that html file path into this script.")
    exit(1)

with open(filename, "r") as f:
    html_doc = f.read()
    soup = BeautifulSoup(html_doc, 'html.parser')

    row_info = {}
    game_bar_classes = soup.find_all("rect", class_="game_bar hitbox link")
    for tag in game_bar_classes:
        # the contents of this is something like:
        # data-popup="{"date":"2022-03-12","label":"Downloads: 94","group":"Sudd City Adventures"}"
        str_data = tag.attrs["data-popup"]
        hover_data = json.loads(str_data)
        key = str(hover_data["date"]) + str(hover_data["group"])
        curr_row = {}
        if key in row_info:
            curr_row = row_info[key]
        else:
            curr_row["Name"] = str(hover_data["group"])
            curr_row["Date"] = str(hover_data["date"])
            curr_row["Views"] = "0"
            curr_row["Downloads"] = "0"
            curr_row["Browser Plays"] = "0"
        if "label" in hover_data:
            arr_split = hover_data["label"].split(":")
            category_name = arr_split[0].strip()
            category_value = arr_split[1].strip()
            curr_row[category_name] = category_value
            row_info[key] = curr_row

    with open('itch-analytics.csv', 'w', newline='') as csvfile:
        fieldnames = ['Date', 'Name', 'Views','Downloads','Browser Plays']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row_key in row_info:
            writer.writerow(row_info[row_key])
