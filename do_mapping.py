import sys
import codecs
import time
import re
from collections import Counter
from os.path import isfile, join
import operator, math

def frmt(myfloat):
  return "{:.7f}".format(myfloat)
  
  
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
  
def word_histogram(string):
  words=filter(None, re.split("[.|]+", string))
  res=dict()
  
  cnt=Counter(words)
  for w in cnt.keys():
    res[w]=float(cnt[w])/float(len(words))
  return res
  
  

def bigram_histogram(string):
  res=dict()
  
  # sum of histo must be 1
  unit=1.0/float(len(string)-1)
  for i in range(0,len(string)-1):
    cur=string[i:i+2]
    if not(cur in res.keys()):
      res[cur]=unit
    else:
      res[cur]=res[cur]+unit
  #return  dict(sorted(res.items(), key=operator.itemgetter(1),reverse=True))
  return res
  

def histo_difference(h1,h2):
  tot=0
  #print set(h1.keys()).union(h2.keys())
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
# | for newline
# . for space
def read_file(fname):
	data=''
	with open(fname, 'r') as myfile:
	    data=' '+myfile.read()

	data=re.sub(r'<[^>]*>', ' ', data)
	data=re.sub(r' *\n *', '|', data)
	data=re.sub(r'\|\|*', '|', data)
	data=re.sub(r'  *', '.', data)
	return data

# altering data1 to make it like data2
def loop_replace(data1,data2):
  # word_ can be changed to bigram_histogram
  h1=word_histogram(data1)
  h2=word_histogram(data2)
  orig_diff=histo_difference(h1,h2)
  top_n_1=top_n_sequences(data1,100,4)
  if ('.' in top_n_1):
    top_n_1.remove('.')
  if ('|' in top_n_1):
    top_n_1.remove('|')
  top_n_2=top_n_sequences(data2,100,4)
  
  for seq1 in top_n_1:
    for seq2 in top_n_2:
      if (seq1!=seq2):
        replaced=data1.replace(seq1,seq2)
        h1=word_histogram(replaced)
        #print data1
        #print replaced
        print seq1+' -> '+seq2+' '+frmt(histo_difference(h1,h2)-orig_diff)
      else:
        print 'EQ:'+seq1


data1=read_file(sys.argv[1])
data2=read_file(sys.argv[2])

print data1[:1000]
h1= word_histogram(data1)
print
print data2[:1000]
h2= word_histogram(data2)
print 'DIFF:' + frmt(histo_difference(h1,h2))

#print word_histogram(data1)
#print word_histogram(data2)

print top_n_sequences(data1,130,4)
print
print top_n_sequences(data2,130,4)
loop_replace(data1,data2)
