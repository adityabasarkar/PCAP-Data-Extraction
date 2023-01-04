
import pyshark
import os
import csv
import socket
import ipapi

cap = pyshark.FileCapture('C:/Users/adity/Documents/aditya docs/Mentorship NCSSM materials/ncsu_iotlab/16/capture_00004_20200316185515.pcap')
CSVfilename = 'C:/Users/adity/Documents/aditya docs/Mentorship NCSSM materials/generated CSVs/GeneratedCSV1.csv'
FileCaptureSummary = []
collectedDomains = {}
specialCaseIPs = []
added = 0
specialCases = 0
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
for p in cap:
    errorNumber = 0
    try:
        if not p.ip.dst == '192.168.1.1':
            added = 0
            currentdomain = ''
            if p.ip.dst in specialcaseips:
                specialcases += 1
                print("special case (cannot add "  + p.ip.dst + " to file capture list)")
                continue

            if not (p.ip.dst in collectedDomains or p.ip.dst in IPdict):
                try:
                    domainTuple = socket.gethostbyaddr(p.ip.dst)
                    collectedDomains[p.ip.dst] = domainTuple[0]
                except:
                    specialCases += 1
                    specialCaseIPs.append(p.ip.dst)
                    print("special case (cannot add to file capture list), added " + p.ip.dst + " to special case IPs list")
                    continue

            if p.ip.dst in collectedDomains:
                currentDomain = collectedDomains[p.ip.dst]
            if p.ip.dst in IPdict:
                currentDomain = IPdict[p.ip.dst]

            for x in FileCaptureSummary:
                if currentDomain == x[1] and IPdict[p.ip.src] == x[0]:
                    x[2] = str(int(x[2]) + int(p.length))
                    added = 1
            if added == 0:
                FileCaptureSummary.append([IPdict[p.ip.src], currentDomain, p.length])
                print("Added Source: " + IPdict[p.ip.src] + " | Destination: " + currentDomain + " | Volume: " + p.length)
            elif added == 1:
                print("Added to volume (not appended) at: Source - " + IPdict[p.ip.src] + " | Destination - " + currentDomain)
    except:
        continue

print(FileCaptureSummary)


    

