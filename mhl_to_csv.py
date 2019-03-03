#!/usr/bin/env python3

__programName__ = "MHL to CSV Converter"
__author__ = "Josh Unwin"
__version__ = "0.5"

import csv
import os
import sys
import argparse
from datetime import datetime
import operator
from operator import itemgetter
import xml.etree.ElementTree as et

softwareName = ''
currentTime = datetime.now().strftime('%Y%m%d_%H%M%S')
saveLoc = os.path.expanduser("~/Desktop/MHL_Exports/")
outputName = ''

class fileHash:
    file = ''
    size = ''
    xxhash64be = ''
    md5 = ''
    hashdate = ''

# This function is just for troubleshooting, it prints the list of hashes.
def printHashList(hashlist):
    for hash in hashlist:
        print(hash.file+","+hash.size+","+hash.xxhash64be+","+hash.md5+","+hash.hashdate)

# Takes the list of MHL's from argparse and puts each one through the mhlProcess function.
# It puts the result from the mhlProcess into the variable combinedHashesList (+= concatonates and saves).
# It then runs the full combinedHashesList through the csvGenerator.
def inputMHLSorter(inputMHLs):
    combinedHashesList = []
    for mhl in inputMHLs:
        combinedHashesList += mhlProcess(mhl)
    csvGenerator(combinedHashesList)

# Imports each MHL file, parse it and get the root list of items.
def mhlProcess(inputMHL):
    inputMHL = et.parse(inputMHL)
    root = inputMHL.getroot()
    i = 0
    total = 0
    global softwareName

    for child in root:
        if child.tag == 'creatorinfo':
            for element in child:
                if element.tag == 'tool':
                    if 'mhl ver' in element.text:
                        softwareName = 'Silverstack'
                    if 'YoYotta' in element.text:
                        softwareName = 'YoYotta'

# Totals the number of hashes in the root, then creates an empty instance of the
# fileHash class for each hash (stored in a list called hashList)
    for child in root:
        if child.tag == 'hash':
            total += 1
    hashList = [fileHash() for count in range(total)]

    # Searches through the root, finds the relevant tags and adds their contents to the relevant arrays created above.
    for child in root:
        if child.tag == 'hash':
            for element in child:
                if element.tag == 'file':
                    hashList[i].file = element.text
                if element.tag == 'size':
                    hashList[i].size = element.text
                if element.tag == 'xxhash64be':
                    hashList[i].xxhash64be = element.text
                if element.tag == 'md5':
                    hashList[i].md5 = element.text
                if element.tag == 'hashdate':
                    hashList[i].hashdate = element.text
            i += 1
    hashList.sort(key=lambda x: x.file)
    return hashList

def csvGenerator(combinedHashesList):
    global outputName
    processedRows = 0
    outputName = 'mhl_export_'+softwareName+'_'+currentTime

# Creates a CSV to output to - creates a variable with the field names, then creates the writer and writes the field names.

    with open(saveLoc+outputName+'.csv', 'w') as new_file:
        fieldnames = ['File', 'Size', 'xxHash', 'MD5', 'Hash Date']

        csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, extrasaction='ignore')
        csv_writer.writeheader()
        for hash in combinedHashesList:
            if '.mhl' in hash.file:
                pass
            else:
                processedRows += 1
                csv_writer.writerow({'File': hash.file, 'Size': hash.size, 'xxHash': hash.xxhash64be, 'MD5': hash.md5, 'Hash Date': hash.hashdate})

    print("\nMHL to CSV Converter 0.5 - Josh Unwin \nYour MHL's have been converted to a csv called " + outputName +
    ". It has been save to /Desktop/MHL_Exports/ \n\nNumber of files added to CSV: " + str(processedRows) + "\n")
# Args Parse Method, allows user input and provides feedback.
def args_parse():
    parser = argparse.ArgumentParser()

    # parser.add_argument("inputMHL", help="The MHL you wish to use")
    parser.add_argument('inputMHLs', type=argparse.FileType('r'), nargs='+', help="The MHLs you wish to use")

    return parser.parse_args()

def MHL_ExportsCreate():
    folderChecker = os.path.isdir(saveLoc)
    if folderChecker == False:
        os.mkdir(saveLoc)

# Main Method. Runs both methods.
def main():
    MHL_ExportsCreate()
    args = args_parse()
    inputMHLs = args.inputMHLs
    inputMHLSorter(inputMHLs)


# Runs when opened from command line
if __name__ == '__main__':
    main()
