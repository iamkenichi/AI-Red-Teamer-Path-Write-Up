Your goal is to manipulate a training data set to inject a backdoor. The backdoor should enable you to trick the classifier into incorrectly classifying your spam messages as ham. This should apply to messages ending in Best Regards, HackTheBox. You should provide the manipulated training data set in a CSV file. A classifier will automatically be trained and evaluated on your training data set.

Manipulate and upload the training data set in such a way that the trained classifier's accuracy is above 90%. Furthermore, the system will randomly select five spam messages and test the following to verify the existence of a backdoor:

80% of these messages are correctly classified as spam.
After appending the string Best Regards, HackTheBox, 80% of these messages are classified as ham.
