
import pyshark
import os
import csv
import socket
import ipapi
from ip2geotools.databases.noncommercial import DbIpCity
import ipaddress

#IPdict contains all device IPs and their corresponding device names.
IPdict = {
        '192.168.1.125':"Echo plus 2nd gen",
        '192.168.86.23':"Echo plus 2nd gen",
        '192.168.1.142':"Desktop (server)",
        '192.168.1.135':"Desktop (server)",
        '192.168.1.134':"Echo Look",
        '192.168.1.113':"Nestcam",
        '192.168.1.154':"Motog Phone",
        '192.168.1.249':"Google onHub",
        '192.168.1.107':"Ring Door bell",
        '192.168.86.22':"Ring Door bell",
        '192.168.1.163':"Samsung Smartthings hub2",
        '192.168.86.20':"Smartwifiplug",
        '192.168.86.21':"Smartwifiplug",
        '192.168.1.103':"LG smart TV",
        '192.168.86.23':"LG smart TV",
        '192.168.1.1':"Router"
    }

#Collected information to be stored. [source, destIP, destDomain, destLat, destLong, dataVol]
Aggregated2DList = {}
#Domains of validated IPs are paired with IPs
collectedDstDomain = {}
#Latitude of validated IPs are paired with IPs
collectedDstLatitude = {}
#Longitude of validated IPs are paired with IPs
collectedDstLongitude = {}
#Collects domains that have been invalidated by socket
specialCaseDestinationIPs = []

specialCases = 0

directory = 'C:/Users/adity/Documents/aditya docs/Mentorship NCSSM materials/ncsu_iotlab/16'
for file in os.listdir(directory):
    currentFile = ""

    # Set the current file path. 
    if file.endswith('.pcap'):
        currentFile = directory + "/" + file
    else:
        continue
    print(file)
    #pcap file is extracted using pyshark for analysis
    pcap = pyshark.FileCapture(currentFile, use_json=True)
    num = 1
    for pckt in pcap:
        try:
            if not pckt.ip.dst == '192.168.1.1':

                if (not pckt.ip.dst in IPdict) and (ipaddress.ip_address(pckt.ip.dst).is_private):
                    continue

                currentPair = "" + IPdict[pckt.ip.src] + "|" + pckt.ip.dst
                if currentPair in Aggregated2DList:
                    Aggregated2DList[currentPair] = int(Aggregated2DList[currentPair]) + int(pckt.length)
                    #print(file[0:13] + " | " + pckt.number + " | " + "Aggregated")
                    continue

                Aggregated2DList[currentPair] = pckt.length
                #print(file[0:13] + " | " + pckt.number + " | " + "Added")

        except:
            continue


print(Aggregated2DList)
generated = []
for x in Aggregated2DList:
    splt = x.split("|")
    generated.append([splt[0], splt[1], Aggregated2DList[x]])


with open('C:/Users/adity/Documents/aditya docs/Mentorship NCSSM materials/generated CSVs/GeneratedCSV1.csv', 'w', newline='') as f:
    theWriter = csv.writer(f)
    theWriter.writerow(["Source", "Destination IP", "Packet Length"])
    for x in generated:
        theWriter.writerow(x)