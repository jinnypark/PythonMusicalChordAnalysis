#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
Created on 2021-11-05

@author: Jinny Park
"""
# this program takes in csv file of chord and metadata of songs, takes Nashville notation of the chord progression,
# and determines chord-loop type if known.

import csv
from collections import Counter

# read-in raw chord data to process

path = "~/JP_meta_corpus_demo_aggregate.csv"
eachSong = []
# index = ""  # [0]
# year = ""  # [1]
# artist = ""  # [2]
# title = ""  # [3]
# data = ""  # [4]. Includes Overall song form as well.
# absChords = ""  # [5]
# section = ""  # [6]
# formType = ""  # [7]
# loopType = ""  # [8]
# chordsOnly = ""  # [9]
# key = ""  # not included. Include by looking at absolute chords.

with open(path) as data_file:
    reader = csv.reader(data_file, delimiter=',', lineterminator='\n')
    a = 0
    for row in reader:
        if a == 0:  # skip header
            a = a + 1
        else:
            eachSong.append(row)
            #print(row)
newData = []
# loopData = []
leftover = []
leftover_chords =[]

for song in eachSong:
    loopType = ""
    chordsOnly = song[9].strip()
    if chordsOnly == "" or chordsOnly[0] == "$":
        pass
    if chordsOnly == "1 5 6- 4":
        loopType = "Axis-C"
    if chordsOnly == "6- 4 1 5":
        loopType = "Axis-A"
    if chordsOnly == "6- 4 1 3-":
        loopType = "Axis-A-sub3-"
    if chordsOnly == "4 1 5 6-":
        loopType = "Axis-F"
    if chordsOnly == "5 6- 4 1":
        loopType = "Axis-G"
    if chordsOnly == "1 6- 4 5":
        loopType = "Doo-wop"
    if chordsOnly == "1 6- 2 5":
        loopType = "Doo-wop-2"
    if chordsOnly == "5 4 1":
        loopType = "Double Plagal"
    if chordsOnly == "4 1 5":
        loopType = "Closed Double Plagal"
    if chordsOnly == "2- 6- 1 5":
        loopType = "minor and major one-fives"
    if chordsOnly == "4 5 6-":
        loopType = "Plateau: open passing loop"
    if chordsOnly == "4 5 6- 5":
        loopType = "Plateau: circular passing loop"
    if chordsOnly == "4 5 6- 1":
        loopType = "Plateau: ascending passing loop"
    if chordsOnly == "4 6- 1":
        loopType = "Plateau: ascending passing loop"
    if chordsOnly == "4 6- 1 3-":
        loopType = "Plateau: closed neighboring loop"
    if chordsOnly == "4 5":
        loopType = "Plateau Shuttle"
    if chordsOnly == "2- 5":
        loopType = "Dorian Shuttle"
    if chordsOnly == "2- 4 6- 5":
        loopType = "Get Lucky-d"
    if chordsOnly == "4 6- 5 2-":
        loopType = "Get Lucky-F"
    if chordsOnly == "6- 5 2- 4":
        loopType = "Get Lucky-a"
    if chordsOnly == "5 2- 4 6-":
        loopType = "Get Lucky-G"
    if chordsOnly == "2- 6-":
        loopType = "Dorian-Aeolian shuffle"
    if chordsOnly == "6- 2-":
        loopType = "Aeolian-Dorian shuffle"
    if chordsOnly == "6- 4 2- 5":
        loopType = "Aeolian-Dorian Four Chords"
    if chordsOnly == "4 6-":
        loopType = "Major-minor Plateau"
    if chordsOnly == "6- 4":
        loopType = "minor-major Plateau"
    if chordsOnly == "4 2- 6- 5":
        loopType = "Lydian-Aeolian Four Chords"
    if loopType == "":
        leftover.append(song)
        if chordsOnly != "":
            if chordsOnly[0] != "$":
                leftover_chords.append(chordsOnly)
    thisSong=song[0:8]
    thisSong.append(loopType)
    newData.append(thisSong)
    # if loopType != "":
    #     thisSong = song[0:8]
    #     thisSong.append(loopType)
    #     newData.append(thisSong)

## count most common chord loops

Counts = Counter(leftover_chords)   #changed bigramResult to revised_bigram
sorted_counts = Counts.most_common()
print(sorted_counts)

## Import Metadata of each song, MBID, etc. accessible by index.
path2 = "/Users/jinnypark/OneDrive - Indiana University/dissertation/SMT2021/Testing/JP_metadata.csv"
eachEntry = {}
# index = ""  # [0]
# year = ""  # [1]
# artist = ""  # [2]
# title = ""  # [3]
# MBID = ""  # [4]
# source = ""  # [5]
# MusicID ranking = ""  # [6]
# form = ""  # [7]

with open(path2) as data_file:
    reader = csv.reader(data_file, delimiter=',', lineterminator='\n')
    a = 0
    for row in reader:
        if a == 0:  # skip header
            a = a + 1
        else:
            eachEntry[row[0]] = [row[1],row[2],row[3],row[4],row[5],row[6],row[7]]
metadata = []

output_name = "aggregate_data.csv"
# #output_name = "chord_loop_identified-Axis.csv"
# #output_name = "chord_loop_identified-Plateau.csv"
with open(output_name, 'w') as csvfile1:
    fieldnames = ['Index', 'Artist', 'title', 'year', 'data', 'Absolute Chords', 'section', 'formtype', 'looptype',
                  'MBID', 'source']
    writer = csv.writer(csvfile1)
    writer.writerow(fieldnames)
    # a = 0
    for song in newData:
        data = [song[0], eachEntry[song[0]][1], eachEntry[song[0]][2], eachEntry[song[0]][0], song[4], song[5], song[6], song[7], song[8],
                eachEntry[song[0]][3], eachEntry[song[0]][4]]
        writer.writerow(data)
