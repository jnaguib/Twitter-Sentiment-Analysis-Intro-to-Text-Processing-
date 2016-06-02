from jnaguib_prep import *
import ast
import re
import codecs


# open the preparedData file and get from it the positive words, negatives, and the emos
f = open("docs/preparedData")

positives = ast.literal_eval(f.readline())
negatives = ast.literal_eval(f.readline())
positiveEmo = ast.literal_eval(f.readline())
negativeEmo = ast.literal_eval(f.readline())
neutralEmo = ast.literal_eval(f.readline())

f.close()

# create a new dictionary that will conatiain all the words 
dwords = {}

# the starting position which will be the value of the word in dwords
# relative position of a word in the features file
m = 1   # position                                                   

tweets = []

# value changes the bool value to 1 or 0
def value (x):
    if x == True:
        return 1
    else: return 0

# inNeg check if s in negatives dictionary
def inNeg (s):
    if (s in negatives):
        return -1
    else: return 0

# inPos check if s in the positives dictionary
def inPos(s):
    if (s in positives):
        return 1
    else: return 0

# checkRepetition takes a string and checks if there are more than two consecutive characters repeated
# if there is , check if the word is positive or negative
def checkRepetition (s):
    rep = False
    repPos = False
    repNeg = False

    # removing the repeated characters from the beginning or the end of the word
    last1 = re.sub (r"(.)\1\1+$", r"\1", s)
    last2 = re.sub (r"(.)\1\1+$", r"\1\1", s)
    start1 = re.sub (r"^(.)\1\1+", r"\1", s)
    start2 = re.sub (r"^(.)\1\1+", r"\1\1", s)

    # if there was characters removed from the word then it contained repeated words
    if last1 != s or last2 != s or start1 != s or start2 != s:
       
        rep = True

        # emphasized is if one of the words is in the negatives dictionary
        emphasized = inNeg(last1) + inNeg(last2) + inNeg(start1) + inNeg(start2)

        # emphasized1 is if one of the words is in the positives dictionary
        emphasized1 = inPos(last1) + inPos(last2) + inPos(start1) + inPos(start2)

        # if emphasized was less than 0 then it is negative repeated word
        if emphasized < 0:
            repNeg = True

        # if emphasized1 was more than zero then it is positive repeated word
        if emphasized1 > 0:
            repPos = True

    return [value(rep), value(repPos), value(repNeg)]


# hashtag takes a tag and checks if it is in positives or negatives
def hashtag (tag):
    pos = False
    neg = False

    if (tag.isupper()):
        a = [tag.lower()]
    else:
        # split the words by the uppercased letters
        a = re.findall('[A-Z][a-z]*', tag)
                                          
    # for each word in a check if it is positive or negative                      
    for i in range (0, len(a)):
        a[i] = a[i].lower()
        if (positives.get(a[i],0) != 0):
            pos = True
        elif (negatives.get(a[i],0) != 0):
            neg = True

    return (a, [value(pos), value(neg)])


# wordProcess takes the list of the tweet and a b to check if the words need to be added
# to the dictionary
def wordProcess(tweet, b):
    global m, tweets, dwords
    upper = False
    positive = False
    negative = False

    hashTag = False
    hashType = [0,0]

    user = False
    repetitions = []
    
    # for each word in the tweet list
    for i in range (0, len(tweet)):
        if ("@" in tweet[i]):
            user = True
        # check if it is all caps
        if (tweet[i].isupper()):
            upper = True
            w = tweet[i].lower()
                       
            # if it is , is the word in the positives
            if (w in positives):
                positive = True
            # if it is in the negatives
            elif w in negatives:
                negative = True


        # if there is a hash in the word, call hashtag to check if it is positive or negative
        if ("#" in tweet[i]):
            hashTag = True
            tweet[i] = tweet[i].replace("#","")
            (a, hashType) = hashtag (tweet[i])
            tweet[i] = ""
            tweet = tweet + a

        # apply preprocessing2 and replace it in the list
        tweet[i] = preProcessing2(tweet[i])
        
         # check if the word contains any repetitions
        repetitions += [checkRepetition(tweet[i])]

        # check b if it is 1 then add the word in the dictionary 
        if b == 1:
            if (dwords.get(tweet[i], -1) == -1):
                # add the word in the dictionary with its position m starting with zero (the global m)
                dwords[tweet[i]] = m
                # increment m
                m = m + 1

    # add the list of tweet to the list of tweets
    tweets = tweets + [tweet]

    case = [value(upper), value(positive), value(negative)]
    hashT = [value(hashTag)] + hashType

    repetitions = filter (lambda x: x[0] == 1, repetitions)
    rept = [0,0,0]
    for i in repetitions:
        rept[0] = 1
        if i[1] == 1:
            rept[1] = 1
        if i[2] == 1:
            rept[2] = 1

    # return the new tweet after preprocessing, a list for the case, list for hashTags, and list for the repetitions
    return (tweet, case, hashT, rept, value(user))


# smileys take a tweet and check if there is an emo in it 
# if there is check if it is positive, negative
def smileys (tweet):
    smile = False
    positive= False
    negative = False
    neutral = False

    # for all the emos in the positive list check if they are in the tweet
    # if yes, then there is a smiley and it is positive
    for x in positiveEmo:
        if x in tweet:
            smile = True
            positive = True
            break

    # do the same for the negativeEmo
    for x in negativeEmo:
        if x in tweet:
            smile= True
            negative = True
            break

    # the same for the neutralEmo
    for x in neutralEmo:
        if x in tweet:
            smile = True
            break

    return (value(smile), value(positive), value(negative))

# check if there is a not in the tweet and if the following word is positive or negative
def notExist (tweet):
    notFound = False
    positive = False
    negative = False
    for i in tweet:
        if notFound == True:
            if (positives.get (i,0) != 0):
                notExistence = True
                positive = True
            elif (negatives.get (i, 0) != 0):
                notExistence = True
                negative = True

            notFound = False
        elif i == "not":
            notFound = True

    return (value(notFound), value(positive), value(negative))

# check if the tweet has positives, negative word
def wordType (t):
    posW = False
    negW = False
    for i in t:
        if i in positives:
            posW = True
        elif i in negatives:
            negW = True

    return (value(posW), value(negW))

#########################  
####### MAIN CODE #######
#########################

def writeToFile(features, dwords, fout, b):
    global tweets    
    
    f = codecs.open (fout, "w")

    extra = len(features[0])
    size = extra + len(dwords) + 1

    if b == 1:
        x = 0
    else:
        x = 1

    for i in range(0, len(tweets)):
        a = {}
        # loop on words                                                       
        for word in tweets[i]:
            p = dwords.get(word, -1)
            if p == -1:
                continue
            pos = dwords[word] + extra
            a[pos + x] = '1'
        
       
        for j in range(b, len(features[i])):
            if features[i][j] == 0:
                continue
            
            a[j + x] = str(features[i][j])


        
       # a = " ".join(a)
        if (b == 1):
            f.write(str(features[i][0]) + " ")
        f.write(str(a))
        f.write("\n")

    f.close()

def train(d, Tfile):
    global dwords
    global tweets
    tweets = []
    dwords = d
    ftrain = codecs.open (Tfile, "r")
    #ftrain = codecs.open ("docs/taskA/train/train2", "r")
    # read the first line from the training data
    line = ftrain.readline()

    # a list of lists to save the features of each tweet in a list
    feature = []

    while line:
        # split the line with tabs
        words = line.split()

        # the tweet is in position 5 -> end
        tweet = " ".join(words[5:])

        # the class of the tweet is at position 4
        analysis = words[4]

        # preprocess the tweet and save the preprocessed tweet in lineP
        lineP = preProcessing (tweet)

        # split lineP (preprocessed Tweet) to get the words in the tweet
        T = lineP.split()

        # call smileys on the list of words of the preprocessed tweet
        # get if there is a smile, if it is positive, if it is negative. 1 0 0 means neutral 
        (smile, smileP, smileN) = smileys(T)

        # call wordProcess on the list of words of the preprocessed tweet
        # return the new tweet after preprocess 2, if there is upper cased word, list for hashtag, list for repetition
        # wordProcess takes 1 to add the words in the dictionary dwords
        (T2, case, hashT, rept, user) = wordProcess(T,1)

        # call notExist on the new tweet returned from wordprocess after the preprocessing2 
        # check if there is a not, if the word follow not is positive, or negative or neither of them which is 0 & 0
        (notExistence, notP, notN) = notExist(T2)

        # check if there are positive, negative word in the tweet after preprocessing2
        (positiveW, negativeW) = wordType(T2)

        # read the next line from the training data
        line = ftrain.readline()

        # the analysis is 1 -> positive
        #                 2 -> negative
        #                  0 -> neutral
        if (analysis == "positive"):
            analysis = "+1"
        elif (analysis == "negative"):
            analysis = "+2"
        else:
            analysis = "+0"

        # in the feature list of lists add the list of features collected from this tweet
        feature = feature + [[analysis,
                                positiveW, negativeW,
                                smile, smileP, smileN,
                                hashT[0], hashT[1], hashT[2],
                                notExistence, notP, notN,
                                rept[0], rept[1], rept[2],
                                case[0], case[1], case[2],
                                user]]

    # Loop ENDS 

    # call writeToFile with the feature list, the dwords: dictionary with all the words found, 
    # and the name of the file to write to
    writeToFile(feature, dwords, "train.txt", 1)    
    
    # write the dwords to the dictionary file
    fdict = codecs.open("docs/dictionary.txt","w")
    fdict.write(str(dwords))
    fdict.close()

    # return the list of features
    return feature

def test (d, name):
    global dwords
    global tweets
    features = []
    tweets = []
    dwords = d
    ftest = codecs.open(name, "r")
    line = ftest.readline()
    fdata = []
    
    while line:

        words = line.split()

        tweet = " ".join(words[5:])

        # fdata is the name id of the file
        fdata = fdata + ["\t".join(words[0:4])]
    
        lineP = preProcessing (tweet)

        T = lineP.split()

        (smile, smileP, smileN) = smileys(T)
        (T2, case, hashT, rept, user) = wordProcess(T,0)
        (notExistence, notP, notN) = notExist(T2)
        (positiveW, negativeW) = wordType(T2)
        
        line = ftest.readline()
        
        features = features + [[positiveW, negativeW,
                                smile, smileP, smileN,
                                hashT[0], hashT[1], hashT[2],
                                notExistence, notP, notN,
                                rept[0], rept[1], rept[2],
                                case[0], case[1], case[2], 
                                user]]
    
    writeToFile(features, dwords, "test.txt", 0)
    return fdata
