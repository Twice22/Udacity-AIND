import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Likelihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    #probabilities should be length 178 (num of words = test_set.num_items = len(get_all_sequences))
    #each probabilities[i] should be length 112 (num of words in training set = size of models)
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []

    # TODO implement the recognizer
    for i in range(test_set.num_items):
      prob = dict()
      for key, value in models.items():
        try:
          prob[key] = value.score(*test_set.get_item_Xlengths(i))
        except:
          prob[key] = float("-inf")
      probabilities.append(prob)
      guesses.append(max(prob, key=prob.get))

    return probabilities, guesses
