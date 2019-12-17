import random
import string
import sys
import re
import math
import operator
import numpy as np

def frmt(myfloat):
  return "{:.6f}".format(myfloat)

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
  min_val=9999999
  min_v1=-1
  min_v2=-1
  min_key='XXX'
  for k in set(h1.keys()).union(h2.keys()):
    v1=0
    if (k in h1.keys()):
      v1=h1[k]
    v2=0
    if (k in h2.keys()):
      v2=h2[k]
    val=math.sqrt(v1*v2)/float(max(v1,v2))
    if (val<min_val):
      min_val=val
      min_v1=v1
      min_v2=v2
      min_key=k
    tot+=math.sqrt(v1*v2)
  # value in 0..1 range
  #print("WORST KEY:",min_key," val:"+str(min_val)+" v1:"+str(min_v1)+" v2:"+str(min_v2))
  return -1*np.log(tot)
  
  
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
    # favour shorter substrings
    strlen=min(random.randint(1,MAXLEN),random.randint(1,MAXLEN),random.randint(1,MAXLEN))
    return data[start:start+strlen]
    
def reject_rule(left,right,all_left):
  return (left==right 
           or
           ((left[0]!=right[0] or
             left[0] in ['.','|'])
            and 
           (left[-1]!=right[-1] or
            left[-1] in ['.','|'])) 
           or
           left in all_left)
	
def new_rule(solution):
    left=rule_sub_string(data1)
    right=rule_sub_string(data2)
    all_left=list()
    for subst in solution:
      all_left.append(subst[0])
    while reject_rule(left,right,all_left):
      left=rule_sub_string(data1)
      right=rule_sub_string(data2)
    return [left,right]
    
def alter_rule(solution,index):
    all_left=list()
    left,right=solution[index]
    
    rand = random.random()

    c1=random.randint(0,len(data1)-1)
    c2=random.randint(0,len(data2)-1)
    rand1=random.random()
    res=''
    newl=left
    newr=right
    if (rand<0.1 and
        len(left)>1 and
        len(right)>1):
      if (rand1<.8):
        randl=random.randrange(len(left))
        newl=left[:randl]+left[randl+1:]
      if(rand1>.2):
        randr=random.randrange(len(right))
        newr=right[:randr]+right[randr+1:]
      res = [newl,newr]
    elif (rand<0.15 and len(left)<MAXLEN and len(right)<MAXLEN):
      temp=left+data1[c1]
      if (rand1<.8 and temp in top_n_1):
        newl=temp
      temp=right+data2[c2]
      if (rand1>.2 and temp in top_n_2):
        newr=temp
      res = [newl,newr]
    elif (rand<0.2 and len(left)<MAXLEN and len(right)<MAXLEN):
      temp=data1[c1]+left
      if (rand1<.8 and temp in top_n_1):
        newl=temp
      temp=data2[c2]+right
      if (rand1>.2 and temp in top_n_2):
        newr=temp
      res = [newl,newr]
    if (res!='' and (res[0]!=left or res[1]!=right)):
      print("ALTER character new:", res, '  old:',left,right)
      return res
    
    for subst in solution:
      all_left.append(subst[0])
    # index rule is going to be altered
    all_left.remove(left)
    for i in range(0,len(top_n_1)):
      newl=random.choice(top_n_1)
      newr=random.choice(top_n_2)
      newl_ok=False
      newr_ok=False
      if (newl!=left and
          #((newl in left) or (left in newl)) and
          not reject_rule(newl,right,all_left)):
        newl_ok=True
      if (newr!=right and
            #((newr in right) or (right in newr)) and
            not reject_rule(left,newr,all_left)):
        if (newl_ok and newl!=newr):
          print("ALTER left/right new:", newl,newr, '  old:',left,right)
          return [newl,newr]
        else:
          print("ALTER right new:", left,newr, '  old:',left,right)
          return [left,newr]
      elif newl_ok:
        print("ALTER left new:", newl,right, '  old:',left,right)
        return [newl,right]
    print("ALTER FAIL")
    return new_rule(solution)

def generate_random_solution(length):
  solution=list()
  for i in range(length):
    solution.append(new_rule(solution))
  return solution

def evaluate(solution):
    newdata=data1
    for subst in solution:
      newdata=newdata.replace(subst[0],subst[1])
    #print "newdata: " +newdata[:1000] 
    newh=bigram_histogram(newdata)
    # minimize difference both from source and target histograms
    diff_h2=histo_difference(newh,h2) # target
    #diff_h1=histo_difference(newh,h1) # source
    #tot= (diff_h2+diff_h1/10.0)*(5+len(solution))
    tot=diff_h2*(10+len(solution))
    #print "DIFF:"+str(tot)+" trgt:"+frmt(diff_h2)+" orig:"+frmt(diff_h1)+" len:"+str(len(solution))
    print "DIFF:"+str(tot)+" trgt:"+frmt(diff_h2)+" len:"+str(len(solution))
    return tot

def mutate_solution(solution):
    rand=random.random()
    if (rand<0): #disabled
      index=int(rand*10000)%2
      i1=random.randint(0, len(solution) - 1)
      i2=random.randint(0, len(solution) - 1)
      print("SWAP",i1,i2, index)
      solution[i1][index]=solution[i2][index]
      
    elif (rand<.001):
      i1=random.randint(0, len(solution) - 1)
      i2=random.randint(0, len(solution) - 1)
      print("SHIFT",i1,i2)
      temp=solution[i1]
      solution[i1]=solution[i2]
      solution[i2]=temp
    elif (rand < .1 and len(solution)>1):
      index = random.randint(0, len(solution) - 1)
      print("DEL ", solution[index], index)
      del solution[index]
    elif (rand<.5):
      index = random.randint(0, len(solution) - 1)
      solution[index]=alter_rule(solution,index)
    else:
      index=-1
      if (len(solution)==MAXRULES):
        index = random.randint(0, len(solution) - 1)
        del solution[index]
      rule=new_rule(solution)
      print("RULE ",rule, index)
      solution.insert(0,rule)
    

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

print("top_n_1 ",top_n_1)
print("top_n_2 ",top_n_2)

best = generate_random_solution(MAXRULES/2)
#best = [['.gli.','.li.'],['ello.','el.']]
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
    if score <= best_score: 
        best = new_solution
        best_score = score
        print(i,' NEW Best score so far', best_score, 'Solution', best)
