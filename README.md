This is the project for Intro to Text Processing course. I build a Twitter Sentiment Analyzer which uses either Naive Bayes or SVM.
The program is trained on a training set of tweets and then it can predict if other tweets are positive/negative/neutral using either of two methods: Naive Bayes or SVM.
The whole process for the project is presented in the report file with the tests and the results.

Different Features implemented in the system:
	1-Type of word:
		-Tweet containing positive or negative words (using Building the
State-of-the-Art in Sentiment Analysis of Tweets data for positive and negative words)
	2-Emoticons:
		-I built a list of emoticons and made each of them either positive or negative
	3-Hashtags:
		-If there are any hashtags in the tweet.
		-Whether the hashtag is positive or negative.
	4-Existence of Not:
		-Existence of not changes the tweet from positivity to negativity and vice versa. (not before positive or negative words change their polarity)
	5-Elongated words:
		-If any elongated words exist (only implemented for the beginning and end of the word e.g. helloooo, greattt..etc)
	6-Uppercase words (e.g GREAT, BAD, AWESOME..etc)
	7-User:
		-If there are tags in the tweet ('@<user>')
	8-Bag of words:
		-Took all the words as a feature to help predict if the tweet is positive/negative/neutral

# To run the code:
You need to create a directory called docs in the same path
as the rest of the files.

## Training the system
	Run the script: jnaguib_train.py
		- It will ask for the full path for the training set

	After Running the script you will find some files created in
	the docs direcotry, and in the same directory of the file.
	It helps in running the system faster.

## Testing with Naive Bayes:
	Run the script: jnaguib_nb.py
		- It will ask for the full path for the testing set
		- The Result of the prediction is in the file testvalues.txt
		with the name id of the file and the class predicted

## Testing with SVM:
	Run the script: jnaguib_svm.py
		- It will ask for the full path for the testing set
		- The Result of the prediction is in a file called "svmvalues.txt"
		with the same format as the one from the Naive bayes
