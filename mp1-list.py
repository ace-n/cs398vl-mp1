# FOR GRAPH GENERATION: http://networkx.lanl.gov/index.html
import json
import nltk
from nltk.corpus import brown, PlaintextCorpusReader
import cPickle
import copy

freq_threshold = 2

def get_freq_table(chapter, wordlists, rep_words):

   ch_words = wordlists.words('Nopunct/ofk_ch{!s}.txt'.format(str(chapter)))
   ch_freqs = nltk.FreqDist(ch_words) # Frequency dictionary (key = word; value = freq.)
   
   # Normalize frequencies
   ch_freq_table = dict()
   for w in ch_freqs:
      ch_freq_table[w] = ch_freqs[w] / rep_words.get(w,1)
   
   # Done!
   return ch_freq_table

def get_distances_between_words(chapter, wordlists, rel_freq_table):

   # Get words
   ch_words = wordlists.words('Nopunct/ofk_ch{!s}.txt'.format(str(chapter)))
   
   # Get position lists
   ch_positions_nofill = dict()
   pos = 0
   for word in ch_words:
      if word not in ch_positions_nofill:
         ch_positions_nofill[word] = []
      
      ch_positions_nofill[word].append(pos)
      pos += 1
         
   # --> Fill in ch_positions dicts
   # ----> Basically a disjoint set implemented as a dict
   len_ch_words = len(ch_words)
   len_ch_positions_nofill = len(ch_positions_nofill)
     
   # Find average distance between each pair of words
   ch_dists = dict()
   for dbg, word1 in enumerate(ch_positions_nofill):
   
      print "PT 2/2: " + str(dbg) + "/" + str(len_ch_positions_nofill)
   
      # DBG
      posList_a = ch_positions_nofill[word1]
      posLen_a = len(posList_a)
   
      ch_dists[word1] = dict()
   
      for word2 in ch_positions_nofill:
                 
         # Skip identicals
         if word1 is word2:
            continue
                 
         posList_b = ch_positions_nofill[word2]
                 
         # === Get distances ===
         totalDist = 0
         totalSteps = len(posList_a)
         
         # Hand-implemented min for realistic speed
         counter_b = 0
         len_b = len(posList_b)
         for counter_a in range(0,totalSteps):
            pos_a = posList_a[counter_a]
            plusOne = counter_b + 1
            while plusOne < len_b and not (posList_b[counter_b] <= pos_a and posList_b[plusOne] >= pos_a):
               minn = min(abs(pos_a - posList_b[counter_b]), abs(posList_b[plusOne] - pos_a))
               totalDist += minn
               counter_b += 1
               plusOne += 1
            
         # Print dist for now (debug)
         ch_dists[word1][word2] = totalDist/totalSteps
         
         # Averaging
         if ch_dists.get(word2) != None and ch_dists[word2].get(word1) != None :
            if ch_dists[word2][word1] != ch_dists[word1][word2]:
               common = (ch_dists[word2][word1] + ch_dists[word1][word2]) / 2
               
               ch_dists[word1][word2] = common
               ch_dists[word2][word1] = common
               
   return ch_dists

def main():
   wordlists = PlaintextCorpusReader('', 'Nopunct/ofk_ch[123]\.txt')

   rep_words = nltk.FreqDist(brown.words()) # Get representative word counts

   for i in range(1,4): 
      table = get_freq_table(i, wordlists, rep_words)
      cPickle.dump(table, open("ch_" + str(i) + "_table.p", "wb"))
      
      dists = get_distances_between_words(i, wordlists, table)  
      cPickle.dump(dists, open("ch_" + str(i) + "_dists.p", "wb"))

# Do something
main()
