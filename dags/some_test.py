
import sys
sys.path.append('../')

import postgresdb.implementation.train as training

print(training.insert_sentiment("You guys suck"))
print(training.insert_sentiment("You guys rock"))