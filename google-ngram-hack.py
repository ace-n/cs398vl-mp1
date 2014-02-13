# A super-duper-hacky Google NGram scraper
import re
import urllib2
from decimal import Decimal

calls_to_google = 0

def get_frequency_from_google(word):

   # Monitor progress/usage
   calls_to_google += 1

   # Step 1: Construct query URL
   url = ("https://books.google.com/ngrams/graph" +
         "?content=" + str(word) +
         "&year_start=1999" +
         "&year_end=2000" +
         "&corpus=15" +
         "&smoothing=1" +
         "&share=" +
         "&direct_url=t1%3B%2C" + str(word) + "%3B%2Cc0")

   # Step 2: Execute query
   raw_html = urllib2.urlopen(url).read()
   
   # Step 3: Get line 347 (where the data is located)
   line347 = raw_html.split("\n")[346] # 346 0-based = 347 1-based
      
   # Step 4: Get first number in line 347
   freq = re.search("(\d|\.)+", line347).group(0)
   
   # Return word weight based on frequency (a number between 0 and 1 inclusive; weight("a") ~ 1)
   return max(Decimal(freq) * 10, 1)
