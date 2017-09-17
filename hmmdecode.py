import math
import sys
import string
import codecs
import ast

devFile=codecs.open(sys.argv[1],"r","utf-8")

#read transition and emission probabilities from modelFile. 
#trDict stores transition probabilities, emDict stores emission probabilities (logarithmic values)
modelFile = open("hmmmodel.txt", "r")
lines = modelFile.read()
lines=lines.split("\n")
trDict=ast.literal_eval(lines[0])
emDict=ast.literal_eval(lines[1])

outputFile=open("hmmoutput.txt","w")

#read development set
devText=[]
for line in devFile:
    line=line.strip(" ")
    line=line.strip("\n")
    devText.append(line)
devFile.close()

#list that stores POS tagged development set
outputList = []

for line in devText:
  # Viterbi - List of dictionaries; list index = time stamp/observation in test sentence
  viterbi = [{}]
  test=line.split(" ")

  for i in range(0,len(test)):

     # find probability,backptr for emission 0 from state 'q0'
     if i==0:
        observation = test[0]
        for k, v in trDict.items():
            if observation in emDict and k in emDict[observation] and k in trDict['q0']:
                viterbi[0][k] = {"prob": trDict['q0'][k] + emDict[observation][k], "prev": 'q0'}
             # Smoothing unknown words in dev set
            elif observation not in emDict and k in trDict['q0']:
                viterbi[0][k] = {"prob": trDict['q0'][k], "prev": "q0"}

    # find probability, backptr for emissions 1 to n
     else:
        observation=test[i]
        viterbi.append({})
        for k,v in trDict.items():
            maxProbValueList=[]
            maxProbStateList=[]
            max_prob=0
            for prevSt, val in trDict.items():
                if observation in emDict and k in emDict[observation] and k in trDict[prevSt] and prevSt in viterbi[i-1]:
                    trProb=trDict[prevSt][k]
                    emProb=emDict[observation][k]
                    prob=viterbi[i-1][prevSt]['prob']+trProb+emProb
                    maxProbValueList.append(prob)
                    maxProbStateList.append(prevSt)
                #smoothing unknown emissions
                elif observation not in emDict and k in trDict[prevSt] and prevSt in viterbi[i-1]:
                    trProb = trDict[prevSt][k]
                    emProb = 0.2
                    prob = viterbi[i - 1][prevSt]['prob'] + trProb + emProb
                    maxProbValueList.append(prob)
                    maxProbStateList.append(prevSt)
                #smoothing unknown transitions between 2 unambiguous words
                elif observation in emDict and k in emDict[observation] and prevSt in viterbi[i-1] and k not in trDict[prevSt]:
                    trProb = math.log(0.7)-math.log(29)
                    emProb = emDict[observation][k]
                    prob = viterbi[i - 1][prevSt]['prob'] + trProb + emProb
                    maxProbValueList.append(prob)
                    maxProbStateList.append(prevSt)

            if len(maxProbValueList)!=0:
                max_prob=max(maxProbValueList)
                index=maxProbValueList.index(max_prob)
                bakPtr=maxProbStateList[index]
                viterbi[i][k]={'prob':max_prob, 'prev':bakPtr}
                
  #final_max_prob picks the state with maximum likelihood for emission 'n'
  final_max_prob = max(value['prob'] for value in viterbi[-1].values())
  
  #prev keeps track of the backpointer while decoding, path stores the sequence of states
  prev=""
  path=[]
  for k,v in viterbi[-1].items():
        if v['prob']==final_max_prob:
            path.append(k)
            prev=k
            break
  for p in range(len(viterbi)-2, -1, -1):
        path.insert(0,viterbi[p+1][prev]['prev'])
        prev=viterbi[p+1][prev]['prev']

  for j in range(0,len(path)):
        outputList.append(test[j]+"/"+path[j]+" ")
  outputList.append("\n")

for line in outputList:
    if line!="\n":
        outputFile.write(line)
    else:
        outputFile.write("\n")

modelFile.close()
outputFile.close()