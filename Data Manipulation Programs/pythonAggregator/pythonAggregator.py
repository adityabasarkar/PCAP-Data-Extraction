import pyshark
import os
import csv
import socket
import ipapi
import geoip2.webservice
import ipaddress
import json
import urllib
import urllib3


csvreader = csv.reader(open("C:/Users/adity/Documents/aditya docs/Mentorship NCSSM materials/generated CSVs/GeneratedCSV3.csv", 'r'))
rowAccum = []

for row in csvreader:
    rowAccum.append(row)

writtenRows = []
rowAccum.remove(['Source', 'Destination IP', 'Volume', 'Destination Domain', 'Destination Latitude', 'Destination Longitude'])

for row in rowAccum:
    addedToExisting = 0
    for x in writtenRows:
        if x[0] == row[0] and x[4] == row[4] and x[5] == row[5] and 'facebook.com' in x[3] and 'facebook.com' in row[3]:
            x[2] = str(int(row[2]) + int(x[2]))
            addedToExisting = 1
            continue

    if addedToExisting == 1:
        continue
    else:
        writtenRows.append(row)

print(writtenRows)

with open('C:/Users/adity/Documents/aditya docs/Mentorship NCSSM materials/generated CSVs/GeneratedCSV3.csv', 'w', newline='') as f:
    theWriter = csv.writer(f)
    theWriter.writerow(["Source", "Destination IP", "Volume", "Destination Domain", "Destination Latitude", "Destination Longitude"])
    for x in writtenRows:
        theWriter.writerow(x)