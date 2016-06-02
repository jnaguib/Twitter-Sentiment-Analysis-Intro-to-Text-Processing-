import codecs
import re

# ways of cleanup for the document:
# --> deleting most of the punctuation and stop words from the document
#     since the upper and lower cased words are the same

f = codecs.open ("docs/stopWds.txt")

stopWds = []

line = f.readline()

while line:
   a = line.split("\n")[0]
   stopWds = stopWds + [a]
   line = f.readline()
f.close()

def preProcessing (tweet):
  
    
   wds = tweet.split()
   line = ""
   for k in wds:
      if k == "can't":
         k = "not"
      else:
         k = k.replace("n't", " not")
      if k in stopWds:
         continue
      else:
         line = line + k + " "
         
   return line

def preProcessing2 (s):
   s = s.lower()
   s = s.replace ("#", "")
   s = s.replace (".", "")
   s = s.replace ("(", "")
   s = s.replace (")", "")
   s = s.replace (";", "")
   s= s.replace (":", "")
   return s

def prepare():
   positives = {}
   negatives = {}

   f = open("docs/emoticons")
   positiveEmo = []
   negativeEmo = []
   neutralEmo = []
   line = f.readline()
   while line:
      emo = line.split()
      if ('positive' in emo[1]):
         positiveEmo += [emo[0]]
      elif('negative' in emo[1]):
         negativeEmo += [emo[0]]
      else:
         neutralEmo += [emo[0]]
      
      line = f.readline()

   f.close()
   f = open ("docs/unigrams-pmilexicon.txt")
   line = f.readline()
   while line :      
      words = line.split()
      value = round(float(words[1]))
      if value > 0:
         positives [words[0]] =  value

      elif value < 0:
         negatives[words[0]] = value
      line = f.readline()

   f.close()

   f = open ("docs/negative-words.txt")
   line = f.readline()
   while line:
      word = line.split("\n")[0]
      negatives[word] = -1.0
      line = f.readline()
   f.close()

   f = open ("docs/positive-words.txt")
   line = f.readline()
   while line:
      word = line.split("\n")[0]
      positives[word] = 1.0
      line = f.readline()
   f.close()
    
   f = open("docs/preparedData", "w")
   f.write(str(positives))
   f.write("\n")
   f.write(str(negatives))
   f.write("\n")
   f.write(str(positiveEmo))
   f.write("\n")
   f.write(str(negativeEmo))
   f.write("\n")
   f.write(str(neutralEmo))
   f.write("\n")
   f.close()

# to make the file in the svm format
# values of b : 0 test
#              1 train
def prepare_svm(b):
   if b == 1:
      f = open("train.txt")
      f2 = open("trainsvm.txt", 'w')
   else:
      f = open("test.txt")
      f2 = open("testsvm.txt", 'w')

   line = f.readline()
   while line:
      line = line.replace("{", "")
      line = line.replace("}","")
      line = line.replace(": ", ":")
      line = line.replace(",", '')
      line = line.replace("'", "")
      if b ==0:
         f2.write ('0' + " ")
      f2.write(line)
      line = f.readline()

   f2.close()
   f.close()

