#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  31 2018

@author: Jinny Park
"""
import csv

# import chord dictionary csv data to create python dictionary.
dict_path = "~/Data/AllChords_dictionary.csv"
my_dict = {}

with open(dict_path, "r") as f:
    cr = csv.reader(f, delimiter=',', lineterminator='\n')
    for row in cr:

        key = row[0].strip("'")
        newrow = row[1].replace(" ", "")
        value = newrow.split(',')
        
        my_dict[key]=value


#read-in raw chord data to process. Change path.
path = "~/Data/2000_toprated_noduplicates_chordsonly.csv"


eachSongs = []
eachTitle = []
with open(path) as data_file:
    reader = csv.reader(data_file, delimiter=',', lineterminator ='\n')
    a = 0
    for row in reader:
        if a == 0:
            a = a + 1
        else:
            title = row[0] #title is URL
            eachTitle.append(title)
            chords = row[1].split(',') #for non duplicate data
            eachSongs.append(chords)

#check to make sure 
#print(eachSongs)        
#print(eachTitle)


           
#this funciton returns pc integer value list of given song, based on the given dictionary.        
def integefy (songList, dictionary):
    newList = [] 
    for chord in songList:
        newList.append(dictionary[chord])
    return newList

#Testing integefy
#print(integefy(['G', 'C', 'G', 'C', 'G', 'Em', 'G', 'Em', 'Bm7', 'C', 'C9', 'G', 'Bm', 'C', 'G', 'Bm', 'C9', 'Am', 'Am7', 'Am7', 'B', 'C/G', 'F', 'C/G', 'G', 'G', 'Em', 'G', 'Em', 'Bm7', 'C', 'C9', 'G', 'Bm', 'C', 'G', 'Bm', 'C9', 'Am', 'Am7', 'Am7', 'B', 'C/G', 'F', 'C/G', 'G', 'Em', 'F', 'C', 'G', 'Bm7', 'C', 'G', 'Bm7', 'C', 'Am', 'Am7', 'Am7', 'B', 'C/G', 'F', 'C/G', 'G', 'F', 'C/G', 'Am7', 'C/G', 'G'], my_dict))


#this function helps merging nested list, such as list of chords within a song. 
#Creates a single list of letters instead of 3 or 4 note values for traids.   

def mergeLists(nested_input_list):
    newList = []
    for each in nested_input_list:
        newList.extend(each)
    return newList   

pcChords = [] #build a nested list of chords into pc integers

for song in eachSongs:
    #integefy the song and append it to pcChords.
    x = mergeLists(integefy(song, my_dict))
    y = []
    # processing string into integer: first get rid of quotes
    for i in x:
        j = i.strip()
        y.append(j)
    #turning string into integers
    y2 = []
    for item in y:
        if (item) == '' or (item) == 'N/A':
            #accounting for empty string
            item = y2.append(item)
        else:
            item = y2.append(int(item))
    #turn list of pitch classes into sets
    y2 = set(y2)
    pcChords.append(y2)

#print(pcChords)


# diatonic dictionary here
diatonic_dict = {"0sharp":(0, 2, 4, 5, 7, 9, 11),	# 0 sharp/flat
"7sharps/5flats": (1, 3, 5, 6, 8, 10, 0),	# 7 sharps/5 flats (C#/Db)
"2sharps/10flats":(2, 4, 6, 7, 9, 11, 1),	# 2 sharps/10 flats D Major/Eb Major
"9sharps/3flats": (3, 5, 7, 8, 10, 0, 2),	# 9 sharps/3 flats D#/Eb Major
"4sharps/8flats": (4, 6, 8, 9, 11, 1, 3),	# 4 sharps/8 flats E/Fb Major
"11sharps/1flat": (5, 7, 9, 10, 0, 2, 4),	# 11 sharps/1 flat F Major
"6sharps/6flat": (6, 8, 10, 11, 1, 3, 5),	# 6 sharps/6 flat F#/Gb Major
"1sharp/11flat": (7, 9, 11, 0, 2, 4, 6),	# 1 sharp/11 flat G/Abb Major
"8sharp/4flats": (8, 10, 0, 1, 3, 5, 7),	# 8 sharp/4 flats G#/Ab Major
"3sharps/9flats": (9, 11, 1, 2, 4, 6, 8),	# 3 sharps/9 flats A/Bbb Major
"10sharps/2flats": (10, 0, 2, 3, 5, 7, 9),	# 10 sharps/2 flats A#/Bb Major
"5sharps/7flats": (11, 1, 3, 4, 6, 8, 10)	# 5 sharps/7 flats B/Cb Major
}


#determine whether given chord sequence is a subset of any of diatonic_sets
# input chord-list of each songs and desired dictionary (either diatonic or pentatonic)
# returns boolean value of wheter the song is subset of any diatonic scale. 
# if true, it also returns its intersectin, a new set wih elements common to song and diatonic scale.
# if false, it returns difference.

def diatonicIndex(chords, dictionary):
    indexList = []
    #stores diatonic index of the song in all possible keys
    for i in range(len(dictionary)):
        #if the set of chords used in the song is subset of any single diatonic collection
        #for python 3.6, need to change dict.value() as list by list(dict_value()) so it becomes iterable.
        if chords.issubset(list(dictionary.values())[i]): 
            indexList.append([True, list(dictionary.items())[i], chords.intersection(list(dictionary.values())[i])])
        else:
            indexList.append([False, list(dictionary.items())[i], chords.difference(list(dictionary.values())[i])])
    return indexList

output_name = "2000_toprated_DI_noduplicates_ver2.csv"
with open(output_name, 'w') as csvfile:
   
    fieldnames=['song URL', list(diatonic_dict.keys())[0],list(diatonic_dict.keys())[1], list(diatonic_dict.keys())[2], list(diatonic_dict.keys())[3], list(diatonic_dict.keys())[4], list(diatonic_dict.keys())[5], list(diatonic_dict.keys())[6], list(diatonic_dict.keys())[7], list(diatonic_dict.keys())[8], list(diatonic_dict.keys())[9], list(diatonic_dict.keys())[10], list(diatonic_dict.keys())[11] ]
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)
    a = 0
    for song in pcChords:
        data = diatonicIndex(song, diatonic_dict)
        writer.writerow([eachTitle[a]]+data)
        #data[0]+data[1]+data[2]+data[3]+data[4]+data[5]+data[6]+data[7]+data[8]+data[9]+data[10]+data[11]
        a = a+1
output_name2 = "2000_toprated_DI_shortVer_noduplicates_ver2.csv"
with open(output_name2, 'w') as csvfile:
    fieldnames = ['song URL']
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)
    a = 0
    for song in pcChords:
        data = diatonicIndex(song, diatonic_dict)
        
        condensed = []
        #only write diatonic collections that belong to the song.
        for item in data:
            if item[0] == True:
                condensed.append(item)
            else:   #if not, simply write out boolean value of False to not crowd the space of csv file.
                condensed.append(False)
        writer.writerow([eachTitle[a]]+condensed)
        a = a+1
output_name3 = "2000_toprated_onlyDiatonic_noduplicates_ver2.csv"
with open(output_name3, 'w') as csvfile:
    fieldnames = ['song URL']
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)
    a = 0   #counter for eachTitle
    for song in pcChords:
        data = diatonicIndex(song, diatonic_dict)
        condensed = []
        #only write diatonic collections that belong to the song.
        for item in data:
            if item[0] == True:
                condensed.append(item)
               #if not, simply write out boolean value of False to not crowd the space of csv file.

        if len(condensed) == 0:
            del eachTitle[a]
            del eachSongs[a]
        else:
            writer.writerow([eachTitle[a]]+condensed+[eachSongs[a]])
            #write out each song title, data of diatonic index, and song chord data. skip the first line because it's a header.
            a = a + 1

