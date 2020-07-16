import os
import json
import datetime

website_dir = os.path.abspath(os.path.dirname(__file__) + os.path.sep + '..') + os.path.sep

# Get from https://etalab.github.io/jours-feries-france-data/json/metropole.json
cache_json = None
with open(website_dir + os.sep + 'days' + os.sep + 'holiday.json', 'r') as fp:
    cache_json = json.load(fp)

def nb_day_between_date(date1 : datetime.date, date2 : datetime.date):
    delta = (date2 - date1).days
    diff_weekdays = (delta - (delta // 7) * 2)
    if cache_json:
        for x in cache_json.keys():
            date = datetime.datetime.strptime(x, '%Y-%m-%d').date()
            if date.isoweekday() < 6 and date > date1 and date < date2:
                diff_weekdays -= 1

    return diff_weekdays + 1
