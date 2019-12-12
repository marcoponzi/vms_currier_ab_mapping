import sys
import codecs
import time
import re
import random
import Levenshtein
from os.path import isfile, join
import operator, math

def frmt(myfloat):
  return "{:.2f}".format(myfloat)
  
  
def top_n_sequences(string, N, max_len):
  counts=dict()
  for ln in range(1,max_len+1):
    for i in range(0,len(string)-ln):
      cur=string[i:i+ln]
      if not(cur in counts.keys()):
        counts[cur]=1
      else:
        counts[cur]=counts[cur]+1
  srt=sorted(counts.items(), key=operator.itemgetter(1),reverse=True)
  res=list()
  for i in range(0,min(len(srt),N)):
     res.append(srt[i][0])
  return res
  

def bigram_histrogram(string):
  res=dict()
  
  # sum of histo must be 1
  unit=1.0/float(len(string)-1)
  for i in range(0,len(string)-1):
    cur=string[i:i+2]
    if not(cur in res.keys()):
      res[cur]=unit
    else:
      res[cur]=res[cur]+unit
  return  dict(sorted(res.items(), key=operator.itemgetter(1),reverse=True))
  

def histo_difference(h1,h2):
  tot=0
  print set(h1.keys()).union(h2.keys())
  for k in set(h1.keys()).union(h2.keys()):
    v1=0
    if (k in h1.keys()):
      v1=h1[k]
    v2=0
    if (k in h2.keys()):
      v2=h2[k]
    tot+=abs(v1-v2)
  # value in 0..1 range
  return (tot/2.0)
  
  
# reads whole file into a string
def read_file(fname):
	data=''
	with open(fname, 'r') as myfile:
	    data=' '+myfile.read()

	data=re.sub(r' *\n *', '|', data)
	data=re.sub(r'  *', '.', data)
	return data



data1=read_file(sys.argv[1])
data2=read_file(sys.argv[2])

print data1
h1= bigram_histrogram(data1)
print data2
h2= bigram_histrogram(data2)
print histo_difference(h1,h2)

print top_n_sequences(data1,500,3)
