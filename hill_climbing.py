import random
import string
import sys
import re
import math
import operator

def frmt(myfloat):
  return "{:.5f}".format(myfloat)

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
  return res
  
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
  
# Bhattacharyya
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
    tot+=math.sqrt(v1*v2)
  # value in 0..1 range
  return 1.0-tot
  
  
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
	
def rule_sub_string(data):
    start=random.randint(0,len(data)-MAXLEN)
    return data[start:start+random.randint(1,MAXLEN)]
	
def new_rule(solution):
    left=rule_sub_string(data1)
    right=rule_sub_string(data2)
    all_left=list()
    for subst in solution:
      all_left.append(subst[0])
    while (left==right 
           or
           ((left[0]!=right[0] or
             left[0] in ['.','|'])
            and 
           (left[-1]!=right[-1] or
            left[-1] in ['.','|'])) 
           or
           left in all_left):
      left=rule_sub_string(data1)
      right=rule_sub_string(data2)
    return [left,right]

def generate_random_solution(length):
  solution=list()
  for i in range(length):
    solution.append(new_rule(solution))
  return solution

def evaluate(solution):
    newdata=data1
    for subst in solution:
      newdata=data1.replace(subst[0],subst[1])
    newh=bigram_histogram(newdata)
    return histo_difference(newh,h2)

def mutate_solution(solution):
    rand=random.random()
    if (rand<0): #disabled
      index=int(rand*10000)%2
      i1=random.randint(0, len(solution) - 1)
      i2=random.randint(0, len(solution) - 1)
      print("SWAP",i1,i2, index)
      solution[i1][index]=solution[i2][index]
    elif (rand<.05):
      i1=random.randint(0, len(solution) - 1)
      i2=random.randint(0, len(solution) - 1)
      print("SHIFT",i1,i2)
      temp=solution[i1]
      solution[i1]=solution[i2]
      solution[i2]=temp
    #elif (rand < .3 and len(solution)>2):
    #  index = random.randint(0, len(solution) - 1)
    #  print("DEL ", solution[index], index)
    #  del solution[index]
    else:
      if (len(solution)==MAXRULES):
        index = random.randint(0, len(solution) - 1)
        del solution[index]
      rule=new_rule(solution)
      print("RULE ",rule, index)
      solution.append(rule)
    

data1=read_file(sys.argv[1])
data2=read_file(sys.argv[2])

print data1[:1000]
h1= bigram_histogram(data1)
print
print data2[:1000]
h2= bigram_histogram(data2)
print 'BHATT DIFF:' + frmt(histo_difference(h1,h2))

MAXLEN=5
MAXRULES=10

top_n_1=top_n_sequences(data1,1000,MAXLEN)
if ('.' in top_n_1):
  top_n_1.remove('.')
if ('|' in top_n_1):
  top_n_1.remove('|')
top_n_2=top_n_sequences(data2,1000,MAXLEN)

best = generate_random_solution(MAXRULES)
best_score = evaluate(best)
i=0
print(i,' NEW Best score so far', best_score, 'Solution', best)

while True:
    print(i,' Best score so far', best_score, 'Solution', best)
    i=i+1

    if best_score == 0:
        break

    new_solution = list(best)
    mutate_solution(new_solution)

    score = evaluate(new_solution)
    if evaluate(new_solution) < best_score: 
        best = new_solution
        best_score = score
        print(i,' NEW Best score so far', best_score, 'Solution', best)
