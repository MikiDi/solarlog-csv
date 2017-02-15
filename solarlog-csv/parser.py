#!/usr/bin/python3

#Michaël Dierick
#30/12/2014
#Parse solarlog min*.js files into csv files

import csv
import datetime
import os
import sys

import pytz

def parsefile(filepath, timezone='Europe/Brussels'):
    if (os.path.isfile(filepath)):
        with open(filepath, "r") as recordfile:
            filecache = [] #Files are kept open for improved efficiency
            for line in recordfile:
                if parseline(line, timezone):
                    timestamp, transformers = parseline(line)
                    i = 0
                    while i < len(transformers): # Different file for each transformer, each year.
                        transformers[i]["timestamp"] = int(timestamp.timestamp())
                        # Find the right csv file to write to
                        filename = "W"+str(i+1)+"_"+str(int(timestamp.year))+".csv"
                        existingfile = next((existingfile for existingfile in filecache if existingfile.name == filename), None)
                        needsheader = False
                        if (existingfile): #Target file is already open, write new row.
                            destinationfile = existingfile
                        else: #target file not open.
                            if not os.path.isfile(filename): needsheader = True  #File doesn't exist yet, make sure to give it a csv-header
                            destinationfile = open(filename, 'a')
                            filecache.append(destinationfile)
                        # Write line to csv file
                        writer = csv.DictWriter(destinationfile, fieldnames=["timestamp", "localtime", "Pac", "Pdc", "Eday", "Udc"])
                        if needsheader:
                            writer.writeheader()
                        writer.writerow(transformers[i])
                        i += 1
            for openfile in filecache:
                openfile.close()


def parseline(line, timezone='Europe/Brussels'):
    if line.startswith("m[mi++]="):
        record = line.split("=")[1].strip("\n").strip('\"')
        parts = record.split("|")
        time = parts[0]
        timestamp = datetime.datetime.strptime(time, "%d.%m.%y %H:%M:%S")
        localzone = pytz.timezone(timezone)
        timestamp = localzone.localize(timestamp)
        transformers = []
        for i in range(1, len(parts)):
            values = parts[i].split(";")
            transformer = {"localtime": time,# Keep original time string for reference
                           "Pac": values[0],
                           "Pdc": values[1],
                           "Eday": values[2],
                           "Udc": values[3]}
            transformers.append(transformer)
        return (timestamp, transformers)
    else:
        return None
