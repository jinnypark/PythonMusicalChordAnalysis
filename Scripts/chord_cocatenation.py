#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
Created on Thu Sept  1 2018

@author: Jinny Park
"""
import csv
from collections import Counter

#change path
path = "~/n-grams_chord_frequency_by_genre/TopSixCountryDataset.csv"

eachSongs = []

        
with open(path) as data_file:
    reader = csv.reader(data_file, delimiter=',', lineterminator ='\n')
    a = 0
    for row in reader:
        chords = row[1].split(',')
        eachSongs.append(chords)
                
#print(eachSongs) 
    #eachSongs contain chords of each song separately.

# First merge n-gram as one list to count them
def mergeNgram(nested_input_list):
    newList = []
    for each in nested_input_list:
        newList.extend(each)
    return newList 

chords = mergeNgram(eachSongs)
sortedCounts = Counter(chords).most_common()
#print(sortedCounts)

### write the gigantic list of unique chords to a .csv file ##############3
# only needs to have the chord names, not the frequency.
output_name = "AllChords.csv"
with open(output_name, 'w') as csvfile:
    fieldnames=['chords']
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)
    for key, value in sortedCounts:
        writer.writerow(list([key]))
