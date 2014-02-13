import sys
import os
import string
from os.path import abspath
from time import sleep

# This script removes all punctuation from a given file
def nopunct(filepath):
   
   # Read file into string
   print "Now depuncting file " + str(filepath)
   fileObj = open(filepath, "r+")
   text = fileObj.read()
            
   # Replace punctuation
   for char in "-\n":
      text = string.replace(text, char, " ")
   
   for char in ".,!?'\"":
      text = string.replace(text, char, "")
   
   # Close file
   fileObj.close()
   
   # Save file
   os.system("rm " + filepath + "-nopunct")    # Hacking
   sleep(0.3)
   os.system("touch " + filepath + "-nopunct") # Hacking
   sleep(0.3)
   fileObj2 = open(filepath + "-nopunct", "w")
   fileObj2.write(text)
   fileObj2.close()
   
# Do something
nopunct(abspath(sys.argv[1]))
