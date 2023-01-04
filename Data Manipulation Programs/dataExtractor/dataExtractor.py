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

csvreader = csv.reader(open("C:/Users/adity/Documents/aditya docs/Mentorship NCSSM materials/generated CSVs/GeneratedCSV1.csv", 'r'))
rowAccum = []
ip2domain = {}
ip2Lat = {}
ip2Long = {}
unable = {}

for row in csvreader:
    rowAccum.append(row)

writtenRows = []
rowAccum.remove(['Source', 'Destination IP', 'Packet Length'])
i = 0
for row in rowAccum:
    try:
        if row[1] in unable:
            print('same ip - unable to append')
            continue
        if row[1] in ip2domain:
            row.append(ip2domain[row[1]])
            row.append(ip2Lat[row[1]])
            row.append(ip2Long[row[1]])
            writtenRows.append(row)
            print("appended with existing")
        else:
            try:
                ip2domain[row[1]] = (socket.gethostbyaddr(row[1]))[0]
                url = 'https://api.ipapi.com/' + row[1] + '?access_key=f3753b6e981ef4255a7b23669492465f'
                http = urllib3.PoolManager()
                r = http.request('GET', url)
                data = json.loads(r.data)
                ip2Lat[row[1]] = data['latitude']
                ip2Long[row[1]] = data['longitude']
            except:
                unable[row[1]] = ""
                print("unable to append")
                continue
            row.append(ip2domain[row[1]])
            row.append(ip2Lat[row[1]])
            row.append(ip2Long[row[1]])
            writtenRows.append(row)
            i += 1
            print(str(i) + " | appended new succesfully")
    except:
        continue


with open('C:/Users/adity/Documents/aditya docs/Mentorship NCSSM materials/generated CSVs/GeneratedCSV2.csv', 'w', newline='') as f:
    theWriter = csv.writer(f)
    theWriter.writerow(["Source", "Destination IP", "Volume", "Destination Domain", "Destination Latitude", "Destination Longitude"])
    for x in writtenRows:
        theWriter.writerow(x)