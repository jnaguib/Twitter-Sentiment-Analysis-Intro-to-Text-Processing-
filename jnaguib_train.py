# SCRIPT FOR TRAINING AND PRODUCING THE FIRST FILES THAT ARE REQUIRED

from jnaguib_featExtract import train
from jnaguib_prep import prepare
import ast

def dictPrep (lst):
    count = 0
    probabilities = {}

    for j in lst:
        for k in j:
            count += 1
            if (probabilities.get(k, 0) == 0):
                probabilities[k] = 1
            probabilities[k] = probabilities[k] + 1
    return (count, probabilities) 


def probFile():
    # open train file, which contains the features of the training data
    ftrain = open ("train.txt")
    line = ftrain.readline()


     # create three list, positives, negatives, neutral for 
    # the positive rows, negative rows, and neutral
    positives = [] 
    negatives = []
    neutral = []


    # add all the lines to allFeat
    while line:
        x = ast.literal_eval(str(line[3:]))
        
        if line[0:2] == "+1":
            positives = positives + [x]

        elif line[0:2] == "+0":
            neutral = neutral + [x]

        elif line[0:2] == "+2":
            negatives = negatives + [x]
        else:
            print "ERROR"
            exit()

        line = ftrain.readline()
    ftrain.close()

    # the total number of tweets
    N_files = len(positives) + len(neutral) + len(negatives)
    
    # probPos is the probability of a positive tweet by number of positives / total number of tweets
    probPos =  (len(positives) * 1.0 / N_files)
    # probNeg is the same for the negatives
    probNeg =  (len(negatives) * 1.0 / N_files)
    # probN is the same for the neutral
    probN  =  (len(neutral) * 1.0 / N_files)
    
    # from the positives get the posProb1  
    cPos, posProb1 = dictPrep(positives)
    # same for negatives
    cNeg, negProb1 = dictPrep(negatives)
    # same for neutral
    cNeu, neuProb1 = dictPrep(neutral)

    f = open ("featuresProb.txt", "w")
    f.write(str(posProb1) + "\n")
    f.write(str(cPos) + "\n")
    f.write(str(probPos) + "\n")

    f.write(str(negProb1) + "\n")
    f.write(str(cNeg) + "\n")
    f.write(str(probNeg) + "\n")

    f.write(str(neuProb1) + "\n")
    f.write(str(cNeu) + "\n")
    f.write(str(probN) + "\n")

    f.close()
    


x = raw_input ("Enter the full path for the training file: \n")
prepare()
train({}, x)

probFile()
