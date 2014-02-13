# FOR GRAPH GENERATION: http://networkx.lanl.gov/index.html
import json
import nltk
from nltk.corpus import brown, PlaintextCorpusReader
import cPickle
import copy

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
   for pos, word in enumerate(ch_words):
      if word not in ch_positions_nofill:
         ch_positions_nofill[word] = dict()
      
      ch_positions_nofill[word][pos] = pos
         
   # --> Fill in ch_positions dicts
   # ----> Basically a disjoint set implemented as a dict
   ch_positions = dict()
   len_ch_words = len(ch_words)
   len_ch_positions_nofill = len(ch_positions_nofill)
   for dbg, word in enumerate(ch_positions_nofill):
      
      #print "PT 1/2: " + str(dbg) + "/" + str(len_ch_positions_nofill)
      
      ch_poses = ch_positions_nofill[word].keys()
      for i in range(0,len_ch_words):
      
         minn = min(ch_poses, key=lambda x:abs(i - x))
         if ch_positions.get(word) is None:
            ch_positions[word] = dict()
         ch_positions[word][i] = minn
      
   # Find average distance between each pair of words
   ch_dists = dict()
   for dbg, word1 in enumerate(ch_positions_nofill):
  
      #print "PT 2/2: " + str(dbg) + "/" + str(len_ch_positions_nofill)
   
      # DBG
      posList_a = ch_positions_nofill[word1]
      posLen_a = len(posList_a)
   
      ch_dists[word1] = dict()
   
      for word2 in ch_positions_nofill:
                 
         # === Get distances ===
         totalDist = 0
         vals = ch_positions_nofill[word2].values()
         totalSteps = len(vals)
         
         for pos_b in vals:        
            added = ch_positions[word1][pos_b]
            totalDist += added
            
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
   wordlists = PlaintextCorpusReader('', 'Nopunct/ofk_ch[1234]\.txt')

   rep_words = nltk.FreqDist(brown.words()) # Get representative word counts

   for i in range(1,2): 
      table = get_freq_table(i, wordlists, rep_words)
      print " === FREQ ==="
      print table
      cPickle.dump(table, open("ch" + str(i) + "_table.p", "wb"))
      
      dists = get_distances_between_words(i, wordlists, table)  
      print " === DIST ==="
      print dists
      cPickle.dump(dists, open("ch" + str(i) + "_dists.p", "wb"))

# Do something
main()
