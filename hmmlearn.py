import math
import sys
import string
import codecs
import ast

#import training dataset using codecs to preserve unicode encoding
#trainFile=codecs.open('train_tagged.txt','r','utf-8')

modelFile = open('hmmmodel.txt', 'w')
trainFile=codecs.open(sys.argv[1],"r")
trainText=[]
for line in trainFile:
    w=line.split(" ")
    trainText.append(w)
trainFile.close()

#dict that stores trasition count for all tags including a start state tag 'q0'. Key = tag, Value = <k,v>; k = tag to which a transition is made; v = number of times the transition occurs
trDict={} 
#dict that stores emission counts. Key = emission, Value = <k,v>; k = tag against which emission occurs, v = number of times the emission occurs as the tag 'k'
emDict={}	 
#dict that stores the total number of emissions for each tag
wordTagCount={}
trDict['q0']={}

for line in trainText:
    linelen = len(line)
    for w in line[0:]:
		#estimate transition, emission probabilities for state 'q0'
        if (line.index(w) == 0):
            tag=w[-2:]
            if tag not in trDict['q0']:
                trDict['q0'][tag]=1
            else:
                trDict['q0'][tag] += 1
            text=w[0:-3]
            if text not in emDict:
                emDict[text] = {}
                emVal = emDict[text]
                if tag not in emVal:
                    emVal[tag] = 1
                else:
                    emVal[tag] += 1
            if tag not in wordTagCount:
                wordTagCount[tag]=1
            else:
                wordTagCount[tag]+=1

		#estimate transition, emission probabilities for emission (n-1) to emission n
        elif (line.index(w)== linelen-2):
            tag = w[-2:]

            text=w[0:-3]
            if tag not in trDict:
                trDict[tag] = {}
            dict1 = trDict[tag]
            tagNext = line[-1][-3:-1]
            if tagNext not in dict1:
                dict1[tagNext] = 1
            else:
                dict1[tagNext] += 1
            if text not in emDict:
                emDict[text] = {}
            emVal = emDict[text]
            if tag not in emVal:
                emVal[tag] = 1
            else:
                emVal[tag] += 1
            if tag not in wordTagCount:
                wordTagCount[tag]=1
            else:
                wordTagCount[tag]+=1

		#estimate transition, emission probabilities for emission 'n'
        elif (line.index(w)==linelen-1):
            tag=w[-3:-1]

            text=w[0:-4]
            if text not in emDict:
                emDict[text] = {}
            emVal = emDict[text]
            if tag not in emVal:
                emVal[tag] = 1
            else:
                emVal[tag] += 1
            if tag not in wordTagCount:
                wordTagCount[tag]=1
            else:
                wordTagCount[tag]+=1
        #estimate transition, emission probabilities for other emissions
        else:
            tag=w[-2:]

            text=w[0:-3]
            pos=line.index(w)
            if tag not in trDict:
                trDict[tag] = {}
            dict1 = trDict[tag]
            tagNext = line[-1][-3:-1]
            tagNext=line[pos+1][-2:]
            if tagNext not in dict1:
                dict1[tagNext] = 1
            else:
                dict1[tagNext] += 1
            if text not in emDict:
                emDict[text] = {}
            emVal = emDict[text]
            if tag not in emVal:
                emVal[tag] = 1
            else:
                emVal[tag] += 1
            if tag not in wordTagCount:
                wordTagCount[tag]=1
            else:
                wordTagCount[tag]+=1


#find log probabilities
for k,v in trDict.items():
 	#tagsum stores total number of transitions that a tag makes to other tags 
    tagsum=sum(trDict[k].values())
    prob=math.log(tagsum)
    for h,j in trDict[k].items():

        trprob=math.log(j)
        trDict[k][h]=trprob-prob

for k,v in emDict.items():
    for h,j in emDict[k].items():
        wordsum=wordTagCount[h]
        prob=math.log(wordsum)
        emprob=math.log(j)
        emDict[k][h]=emprob-prob

#write transition and emission probabilities to model file (logarithmic values)
modelFile.write(str(trDict))
modelFile.write("\n")
modelFile.write(str(emDict))
modelFile.close()


