#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 2018

@author: Jinny Park
"""
import csv
from collections import Counter

#change path
path = "~/Data/1990_transposed_diatonic_chords_noduplicates.csv"

eachSongs = []

        
with open(path) as data_file:
    reader = csv.reader(data_file, delimiter=',', lineterminator ='\n')
    a = 0
    for row in reader:
        chords = row[1].split(',')
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
        eachSongs.append(chords)

#print(eachSongs) 
    #eachSongs contain chords of each song separately.
#in order to create accurate n-grams, gotta keep chord boundaries within each pieces.           

#### n-gram generator ############################
#to get result of zip object, use list
    #(list(find_bigrams(input_list)))

def find_ngrams(input_list, n):
  return zip(*[input_list[i:] for i in range(n)])

bigramResult = []
for song in eachSongs:
    bigramResult.append(list(find_ngrams(song,2)))
    
trigramResult = []
for song in eachSongs:
    trigramResult.append(list(find_ngrams(song,3)))
    
quadrigramResult = []
for song in eachSongs:
    quadrigramResult.append(list(find_ngrams(song,4)))
#print(bigramResult)


### count n-gram results ###
#
# First merge n-gram as one list to count them
def mergeNgram(nested_input_list):
    newList = []
    for each in nested_input_list:
        newList.extend(each)
    return newList   
#print(mergeNgram(bigramResult))

## count unique n-gram possibilities within a song ##
revised_bigram = []
for song in eachSongs:
    revised_bigram.append(list(set(find_ngrams(song,2))))
    
revised_trigram = []
for song in eachSongs:
    revised_trigram.append(list(set(find_ngrams(song,3))))

revised_quadrigram = []
for song in eachSongs:
    revised_quadrigram.append(list(set(find_ngrams(song,4))))
    
# Then Count ngram in the order of most frequency
bigramCounts = Counter(mergeNgram(revised_bigram))   #changed bigramResult to revised_bigram
sorted_bigram = bigramCounts.most_common()

trigramCounts = Counter(mergeNgram(revised_trigram))
sorted_trigram = trigramCounts.most_common()

quadrigramCounts = Counter(mergeNgram(revised_quadrigram))
sorted_quadrigram = quadrigramCounts.most_common()

#   merge eachSongs to one gigantic list to create basic frequency counts of each chord type#
#   there needs to be a way of sorting through duplicates or 'synonyms'

chords = mergeNgram(eachSongs)
sortedCounts = Counter(chords).most_common()
print(sortedCounts)
### write basic statsictics to a .csv file ##############3
output_name = "1990_mostCommon_n-grams_noduplicates.csv"
with open(output_name, 'w') as csvfile:
    fieldnames=['chords', 'count']
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)
    for key, value in sortedCounts:
        writer.writerow(list([key] + [value]))

##########################################################

output_name2 = "1990_transposed_n-grams_noduplicates.csv"

with open(output_name2, "w") as csvfile:
    fieldnames=['bigram Result']
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)
    for key,value in sorted_bigram:
        writer.writerow(list([key] + [value]))
    writer.writerow(['trigram Result'])
    for key,value in sorted_trigram:
        writer.writerow(list([key] + [value]))
    writer.writerow(['quadrigram Result'])
    for key,value in sorted_quadrigram:
        writer.writerow(list([key] + [value]))

