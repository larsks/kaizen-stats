import sys
import csv
import json


with open("stats.json") as fd:
    stats = json.load(fd)
    first = True
    for project, data in stats.items():
        if first:
            writer = csv.DictWriter(sys.stdout, data.keys())
            writer.writeheader()
            first = False

        writer.writerow(data)
