from jnaguib_featExtract import test
import ast
import math

testF = raw_input ("Please Enter the full path to the test file: ")
#testF = "docs/taskA/dev/test/twitter-dev-gold-A.tsv"
#testF = "docs/taskA/train/twitter-train-cleansed-A.txt"
#testF = "docs/taskA/twitter-test-gold-A.tsv"

# opens the dictionary file
f = open("docs/dictionary.txt")
line = f.readline()
f.close()

# get the dwords dictionary, dictionary with all the words with their values being their
# position in the features list
dwords = ast.literal_eval(line)


def getProb (feat, ones, count, maxV):
   
    prob = 0

    # get the number of features that are on in this tweet
    #x = feat.count('1')
    #y = feat.count('0')
    # add that to the total number of 1's for smoothing
    count = count + maxV
    #count = count + y

    for i in range(0, maxV+1): 
        if (feat.get(i, 0) == '1'):
            prob += math.log((ones.get(i,0) + 1.0) / count)
        else:
            prob += math.log(1.0 - (ones.get(i, 0) +1.0) / count)
       

    return prob

  
######### GETTING THE PROBABILITIES VALUES ##############         
f = open("featuresProb.txt")
posProb1 = ast.literal_eval(f.readline())
cPos = int(f.readline())
probPos = float(f.readline())

negProb1 = ast.literal_eval(f.readline())
cNeg = int(f.readline())
probNeg = float(f.readline())

neuProb1 = ast.literal_eval(f.readline())
cNeu = int(f.readline())
probN = float(f.readline())

f.close()
################################

######## TESTING ###################################3
# calling the test function on the file entered by the user
fdata = test(dwords, testF)

fout = open("testvalues.txt", "w")

ftest = open("test.txt")
line = ftest.readline()
i = 0

# get the biggest index in the class
a1 = max(k for k, v in posProb1.iteritems())
a2 = max(k for k, v in negProb1.iteritems())
a3 = max(k for k, v in neuProb1.iteritems())

while line:
    # get the features dictionary from the file
    feat = ast.literal_eval(line)
    
    # Getting the probability of each class
    pPos = getProb(feat, posProb1, cPos, a1) + math.log(probPos)
    pNeg = getProb(feat, negProb1, cNeg, a2) + math.log(probNeg)
    pN = getProb (feat, neuProb1, cNeu, a3) + math.log(probN)

    #Getting the max of the probabilities
    y = max(pPos, max(pNeg, pN))
   
  
    if (y == pPos):
        t = "positive"
    elif (y == pNeg):
        t = "negative"
    elif (y == pN):
        t = "neutral"
    
    # WRITING TO THE OUTPUT FILE
    fout.write(fdata[i])
    fout.write("\t" + t)
    fout.write("\n")

    i = i+1
    line = ftest.readline()

ftest.close()
fout.close()

#################################################333


