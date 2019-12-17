#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24  2018

@author: Jinny Park
"""
#using diatonic chord dictionary, transpose diatonic chord symbols (e.g., "GM") into white-key scale ("CM"). Use the data from diatonic index, and figure out how many sharps/flats are in each. if zero, do nothing. export newly transposed data.

#givn chords in non-zero sharp collection, convert the chord into integers using dictionary, and transpose down/up by necessary steps according to its key collection information.


#helpful function for dealing with nested list, giving merged ver.
def mergeLists(nested_input_list):
    newList = []
    for each in nested_input_list:
        newList.extend(each)
    return newList

#helpful function for finding dictionary keys, given its values.
def get_dict_keys(d, val):
        return [k for k in d.keys() if d[k] == val]

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
#print(my_dict)

#read in data to process

#change path
path = "~/Data/1990_toprated_onlyDiatonic_noduplicates.csv"

eachSongs = []
eachTitle = []
eachKey1 = []
eachKey2 = []
with open(path) as data_file:
    reader = csv.reader(data_file, delimiter=',', lineterminator ='\n')
    a = 0
    for row in reader:
        if a == 0:#acounting for the top header; skip if it's the first line.
            a = a + 1
        else:
            title = row[0] #title is URL
            eachTitle.append(title)
            key1 = row[1].split(',') #first diatonic collection recognized
            realkey1 = key1[1]
            realkey1 = realkey1.strip()
            realkey1 = realkey1.strip("(")
            realkey1 = realkey1.lstrip("'")
            realkey1 = realkey1.rstrip("'")
            eachKey1.append(realkey1)
            key2 = row[2].split(',')
            if len(key2) > 1:#if there is a secondary diatonic collection
                realkey2 = key2[1]
                realkey2 = realkey2.strip()
                realkey2 = realkey2.strip("(")
                realkey2 = realkey2.lstrip("'")
                realkey2 = realkey2.rstrip("'")
                eachKey2.append(realkey2)
            else: #if there is no secondary diaonic collection
                eachKey2.append(key2)
             #not many have secondary key. mostly pentatonic ones.
            chords = row[4].split(',')
            a = 0
            for i in chords:
                newchord = i.strip()
                newchord = newchord.rstrip("]")
                newchord = newchord.lstrip("[")
                newchord = newchord.rstrip("'")
                newchord = newchord.lstrip("'")
               # print(newchord)
                chords[a] = newchord
                a = a +1
            #print(chords)
            eachSongs.append(chords)

print(eachSongs)
#print(eachKey2)
#print(eachTitle)


#this funciton returns pc integer value list of given song, based on the given dictionary.        
def integefy (songList, dictionary):
    newList = [] 
    for chord in songList:
        newList.append(dictionary[chord])
    return newList

#Testing integefy
#print(integefy(['G', 'C', 'G', 'C', 'G', 'Em', 'G', 'Em', 'Bm7', 'C', 'C9', 'G', 'Bm', 'C', 'G', 'Bm', 'C9', 'Am', 'Am7', 'Am7', 'B', 'C/G', 'F', 'C/G', 'G', 'G', 'Em', 'G', 'Em', 'Bm7', 'C', 'C9', 'G', 'Bm', 'C', 'G', 'Bm', 'C9', 'Am', 'Am7', 'Am7', 'B', 'C/G', 'F', 'C/G', 'G', 'Em', 'F', 'C', 'G', 'Bm7', 'C', 'G', 'Bm7', 'C', 'Am', 'Am7', 'Am7', 'B', 'C/G', 'F', 'C/G', 'G', 'F', 'C/G', 'Am7', 'C/G', 'G'], my_dict))
#print(integefy(eachSongs[0],my_dict))
#print(eachKey1)
#print(eachKey2)

# transposition diatonic dictionary here. key gives number of semitones to be added, mod 12
diatonic_dict = {"0sharp": 0, #(0, 2, 4, 5, 7, 9, 11),	# 0 sharp/flat
                 "7sharps/5flats": 11, #(1, 3, 5, 6, 8, 10, 0),	# 7 sharps/5 flats (C#/Db)
                 "2sharps/10flats": 10, #(2, 4, 6, 7, 9, 11, 1),# 2 sharps/10 flats D Major/Eb Major
                 "9sharps/3flats": 9, #(3, 5, 7, 8, 10, 0, 2),	# 9 sharps/3 flats D#/Eb Major
                 "4sharps/8flats": 8, # (4, 6, 8, 9, 11, 1, 3),	# 4 sharps/8 flats E/Fb Major
                 "11sharps/1flat": 7, # (5, 7, 9, 10, 0, 2, 4),	# 11 sharps/1 flat F Major
                 "6sharps/6flat": 6, #(6, 8, 10, 11, 1, 3, 5),	# 6 sharps/6 flat F#/Gb Major
                 "1sharp/11flat": 5, #(7, 9, 11, 0, 2, 4, 6),	# 1 sharp/11 flat G/Abb Major
                 "8sharp/4flats": 4, #(8, 10, 0, 1, 3, 5, 7),	# 8 sharp/4 flats G#/Ab Major
                 "3sharps/9flats": 3, #(9, 11, 1, 2, 4, 6, 8),	# 3 sharps/9 flats A/Bbb Major
                 "10sharps/2flats": 2, # (10, 0, 2, 3, 5, 7, 9),# 10 sharps/2 flats A#/Bb Major
                 "5sharps/7flats": 1, #(11, 1, 3, 4, 6, 8, 10)	# 5 sharps/7 flats B/Cb Major
}

a = 0 # counter
transposed_int = []
for song in eachSongs:
    x = integefy(song, my_dict)#nested list of integeefied chords of songs. [[1, 3, 5], [1, 3, 5]..]

    #Based on diatonic_dict, add appropriate number of semitones to chords 
    transposedSong = []#where we will store transposed notes
    semitones = diatonic_dict.get(eachKey1[a])
    for eachChord in x:
        newChord = []
        for eachNote in eachChord:
            newChord.append((int(eachNote) + semitones)%12)
        transposedSong.append(newChord)
    a = a+1
    #print(transposedSong)
    transposed_int.append(transposedSong)
#print(transposed_int)

#now turn integers back to chord symbols, from our chord dictionary
#j = 0 #counter
transposed_chordified = []

for song in transposed_int:
    chordifiedSong = []
    for eachChord in song:
        #newChord = []
        #print(eachChord, "type is: ", type(eachChord))
        
        g = []
        for pitch in eachChord:
            pitch = str(pitch)
            g.append(pitch)
        #print(g)
        z = get_dict_keys(my_dict, g)
        if len(z) < 1:
            print("no key for this chord: ", g)#error detection
        else:
            chordifiedSong.append(z[0])
        #    print(z[0])#gotta clean this up to actually match different suspensions and what not.
        #also turn dictionary values as sets, so i don't have duplicates with rotations.
       
            
    transposed_chordified.append(chordifiedSong)
   # j = j+1
#print(transposed_chordified)

output_name = "1990_transposed_diatonic_chords_noduplicates.csv"
with open(output_name, 'w') as csvfile:
    fieldnames=['song URL', 'chords' ]
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)
    a = 0
    for song in transposed_chordified:
        #data = diatonicIndex(song, diatonic_dict)
        writer.writerow([eachTitle[a]]+[song])
        #data[0]+data[1]+data[2]+data[3]+data[4]+data[5]+data[6]+data[7]+data[8]+data[9]+data[10]+data[11]
        a = a+1
