# itchio-analytics-csv-export
Tiny script that I wrote and was helpful to me. It exports the analytics bar graph from html to csv from itch.io dashboard.

This script is a workaround for https://github.com/itchio/itch.io/issues/479
It will take itch.io analytics data from the bar graph on the dashboard and create a csv.

Download html of last 30 days from https://itch.io/dashboard/analytics
Run this script with the path to that page as the first parameter
A itch-analytics.csv file will be created in the working directory.