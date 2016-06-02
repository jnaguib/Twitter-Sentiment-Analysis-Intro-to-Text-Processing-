import imp
from jnaguib_featExtract import test
from jnaguib_prep import prepare_svm
import ast

foo = imp.load_source('svmutil', 'libsvm/python/svmutil.py')


#### TESTING FILES ############
#testF = "docs/taskA/dev/test/twitter-dev-gold-A.tsv"
#testF = "docs/taskA/twitter-test-gold-A.tsv"
#testF = "docs/taskA/train/twitter-train-cleansed-A.txt"
testF = raw_input ("Please Enter the full path to the test file: ")
####################################

# create the trainsvm file from train to
# be in the svm format
prepare_svm(1)

### TRAINING ######
y, x = foo.svm_read_problem('./trainsvm.txt')
prob = foo.svm_problem(y,x)

param = foo.svm_parameter()
param.kernel_type = foo.LINEAR

m = foo.svm_train(prob, param)
#############################

# opens the dictionary file
f = open("docs/dictionary.txt")
line = f.readline()
f.close()

# get the dwords dictionary, dictionary with all the words with their values being their
# position in the features list
dwords = ast.literal_eval(line)

fdata = test(dwords, testF)

prepare_svm(0)

##### PREDICTING #################
y2, x2 = foo.svm_read_problem('./testsvm.txt')

pred, acc, val = foo.svm_predict([0]*len(x2), x2, m) 
##################################


# WRITING VALUES TO FILE #######################
fout = open("svmvalues.txt", "w")

for k in range(0, len(pred)):
	i = pred[k]
	if i == 1.0:
		t = 'positive'
	elif i == 2.0:
		t = 'negative'
	else:
		t = "neutral"

	fout.write(fdata[k])
	fout.write("\t" + t)
	fout.write("\n")

fout.close()
####################################################


