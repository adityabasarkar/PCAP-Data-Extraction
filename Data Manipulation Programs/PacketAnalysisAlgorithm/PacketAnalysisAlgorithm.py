
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
Aggregated2DList = []
#Domains of validated IPs are paired with IPs
collectedDstDomain = {}
#Latitude of validated IPs are paired with IPs
collectedDstLatitude = {}
#Longitude of validated IPs are paired with IPs
collectedDstLongitude = {}
#Collects domains that have been invalidated by socket
specialCaseDestinationIPs = []

specialCases = 0

directory = 'C:/Users/adity/Documents/aditya docs/Mentorship NCSSM materials/ncsu_iotlab_testFiles'
for file in os.listdir(directory):
    currentFile = ""

    # Set the current file path. 
    if file.endswith('.pcap'):
        currentFile = directory + "/" + file
    else:
        continue

    #pcap file is extracted using pyshark for analysis
    pcap = pyshark.FileCapture(currentFile, use_json=True)
    for pckt in pcap:
        try:
            if not pckt.ip.dst == '192.168.1.1':

                if not pckt.ip.src in IPdict:
                    continue

                lengthAppended = 0
                for x in Aggregated2DList:
                    if x[0] == IPdict[pckt.ip.src] and x[1] == pckt.ip.dst:
                        x[5] = int(x[5]) + int(pckt.length)
                        print(file[0:13] + " | " + pckt.number + " | " )#+ "A similar source-destinatino pair has been found: adding to packet length [Source: " + pckt.ip.src + " | Destination: " + pckt.ip.dst + "]")
                        lengthAppended = 1
                        continue

                if lengthAppended == 1:
                    continue

                if pckt.ip.dst in specialCaseDestinationIPs:
                    print("Special case")
                    specialCases += 1
                    continue

                currentDstDom = ""
                currentDstLat = ""
                currentDstLong = ""

                if pckt.ip.dst in IPdict:
                    currentDstDom = IPdict[pckt.ip.dst]
                    currentDstLat = "35.7847"
                    currentDstLong = "-78.6821"
                elif ipaddress.ip_address(pckt.ip.dst).is_private:
                    continue
                elif pckt.ip.dst in collectedDstDomain:
                    currentDstDom = collectedDstDomain[pckt.ip.dst]
                    currentDstLat = collectedDstLatitude[pckt.ip.dst]
                    currentDstLong = collectedDstLongitude[pckt.ip.dst]
                else:
                    try:
                        currentDstDom = (socket.gethostbyaddr(pckt.ip.dst))[0]
                        response = DbIpCity.get(pckt.ip.dst, api_key='free')
                        currentDstLat = response.latitude
                        currentDstLong = response.longitude
                        collectedDstDomain[pckt.ip.dst] = currentDstDom
                        collectedDstLatitude[pckt.ip.dst] = currentDstLat
                        collectedDstLongitude[pckt.ip.dst] = currentDstLong
                        print("Domain, Latitude, and Longitude have been found for destination ip: " + pckt.ip.dst)
                    except:
                        print("Either the domain, latitude, or longitude have not been validated. Adding " + pckt.ip.dst + " to specialCaseDestinationIPs")
                        specialCaseDestinationIPs.append(pckt.ip.dst)
                        continue
                
                Aggregated2DList.append([IPdict[pckt.ip.src], pckt.ip.dst, currentDstDom, currentDstLat, currentDstLong, pckt.length])
                print("A packet has been appended")
        except:
            continue


print(Aggregated2DList)

with open('C:/Users/adity/Documents/aditya docs/Mentorship NCSSM materials/generated CSVs/GeneratedCSV1.csv', 'w', newline='') as f:
    theWriter = csv.writer(f)
    theWriter.writerow(["Source", "Destination IP", "Destination Domain", "Destination Latitude", "Destination Longitude", "Packet Length"])
    for x in Aggregated2DList:
        theWriter.writerow(x)