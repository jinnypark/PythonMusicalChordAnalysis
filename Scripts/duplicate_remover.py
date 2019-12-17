#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 2018

@author: Jinny Park
"""
#this program takes in csv file of chord and metadata of songs, and checks meta title and description to make sure there duplicates are removed. If there are duplicates, I keep highest rated version (the one that came first  is highest rated.)
# output reproduces URL and chords data.

import csv


#read-in raw chord data to process

path = "~/Data/top1990.csv"
eachURL = []
eachTitle = []
eachSong = []
with open(path) as data_file:
    reader = csv.reader(data_file, delimiter=',', lineterminator ='\n')
    a = 0
    for row in reader:
        if a == 0:
            a = a + 1
        else:
            URL = row[0] 
            eachURL.append(URL)
            #title = row[2]
            title = row[4]
            eachTitle.append(title)
            #song = row[4]
            song = row[1]
            eachSong.append(song)
#print(eachTitle)


#this function helps merging nested list, such as list of chords within a song. 
#Creates a single list of letters instead of 3 or 4 note values for traids.   

def mergeLists(nested_input_list):
    newList = []
    for each in nested_input_list:
        newList.extend(each)
    return newList   

#clean the data, only save content information for the format of :
#'<meta property="og:title" content="Third Day - God Of Wonders (Chords)">'
#into "Third Day - God Of Wonders (Chords)"
#save them as content only list, to be compared later.

p = 0
contentOnly = []
for title in eachTitle:
    beginat = 35
    endat = len(title) - 2
    #print(type(title))
    content = title[beginat:endat]
    #eachTitle[p] = content
    contentOnly.append(content)
    p = p+1
#print(eachTitle)
#print(contentOnly)

#go through contentonly list, and if it's a duplicate, remove from list of title and songs as well.
seen = set([])
j = 0 #iterating variable
#print("length of contentonlylist is: ", len(contentOnly), "length of eachTitle is: ", len(eachTitle))
for content in contentOnly:
   
    if content in seen: #if duplicate, remove from data.
        #print(content + "is a duplicate. will remove.")
       # print("length of j is: ", j, "length of eachTitle is: ", len(eachTitle))
        del eachTitle[j]
        del eachSong[j]
        del eachURL[j]
    else:
    #    print("content is not in seen")
        seen.add(content)
        j = j + 1

#print(seen)
#print(eachTitle)

output_name = "1990_toprated_noduplicates_chordsonly2.csv"
with open(output_name, 'w') as csvfile:
    fieldnames=['song URL', 'title', 'chords' ]
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)
    a = 0
    for title in eachTitle:
        writer.writerow([eachURL[a]]+[eachSong[a]]+[eachTitle[a]])
        a = a+1
