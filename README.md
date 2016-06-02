
You need to create a directory called docs in the same path
as the rest of the files.

First you need to train the system:
	Run the script: jnaguib_train.py
		- It will ask for the full path for the training set

	After Running the script you will find some files created in 
	the docs direcotry, and in the same directory of the file.
	It helps in running the system faster.

Testing with Naive Bayes:
	Run the script: jnaguib_nb.py
		- It will ask for the full path for the testing set
		- The Result of the prediction is in the file testvalues.txt
		with the name id of the file and the class predicted

Testing with SVM:
	Run the script: jnaguib_svm.py
		- It will ask for the full path for the testing set
		- The Result of the prediction is in a file called "svmvalues.txt"
		with the same format as the one from the Naive bayes
