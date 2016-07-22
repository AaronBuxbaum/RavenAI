import csv
from itertools import izip

with file("RawKnownData.csv", "r") as rawdata, file("ProblemResults.csv", "r") as results, file("KnownData.csv", "a") as write:
    rawdata = csv.reader(rawdata)
    results = csv.reader(results)
    writer = csv.writer(write)

    next(results)  # skip the headers

    for row, results_row in izip(rawdata, results):
        print row
        print results_row
        if row[2] is not results_row[1]:
            raise ValueError("ERROR: THERE WAS A PROBLEM")
        row.append(results_row[2])
        writer.writerow(row)