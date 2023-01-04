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
    if 'r.cloudfront.net' in row[3]:
        row[3] = 'r.cloudfront.net'
    elif 'compute.amazonaws.com' in row[3] or 'compute-1.amazonaws.com' in row[3]:
        row[3] = 'compute.amazonaws.net'
    elif 'bc.googleusercontent.com' in row[3]:
        row[3] = 'bc.googleusercontent.com'
    elif 'unity.ncsu.edu' in row[3]:
        row[3] = 'unity.ncsu.edu'
    elif 'eos.ncsu.edu' in row[3]:
        row[3] = 'eos.ncsu.edu'
    elif '1e100.net' in row[3]:
        row[3] = '1e100.net'
    elif 'facebook.com' in row[3]:
        row[3] = 'facebook.com'
    elif 'yahoo.com' in row[3]:
        row[3] = 'yahoo.com'
    elif 'akamaitechnologies.com' in row[3]:
        row[3] = 'akamaitechnologies.com'
    elif 'amazon.com' in row[3]:
        row[3] = 'amazon.com'
    elif 'zip.zayo.com' in row[3]:
        row[3] = 'zip.zayo.com'
    elif 'fbcdn.net' in row[3]:
        row[3] = 'fbcdn.net'
    elif 'static.steadfastdns.net' in row[3]:
        row[3] = 'static.steadfastdns.net'
    elif 's3-1-w.amazonaws.com' in row[3]:
        row[3] = 'amazonaws.com'
    elif 'upcloud.host' in row[3]:
        row[3] = 'upcloud.host'
    elif 'a-msedge.net' in row[3]:
        row[3] = 'a-msedge.net'
    elif 'adnexus.net' in row[3]:
        row[3] = 'adnexus.net'
    elif 'rtbhouse.net' in row[3]:
        row[3] = 'rtbhouse.net'
    elif 'siteground.com' in row[3]:
        row[3] = 'siteground.com'
    elif 'adfarm1.adition.com' in row[3]:
        row[3] = 'adfarm1.adition.com'
    elif 'instances.scw.cloud' in row[3]:
        row[3] = 'instances.scw.cloud'
    elif 'novotelecom.ru' in row[3]:
        row[3] = 'novotelecom.ru'

    if not (row[3] == 'igmp.mcast.net'):
        writtenRows.append(row)

print(writtenRows)

with open('C:/Users/adity/Documents/aditya docs/Mentorship NCSSM materials/generated CSVs/GeneratedCSV4.csv', 'w', newline='') as f:
    theWriter = csv.writer(f)
    theWriter.writerow(["Source", "Destination IP", "Volume", "Destination Domain", "Destination Latitude", "Destination Longitude"])
    for x in writtenRows:
        theWriter.writerow(x)