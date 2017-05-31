import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, words: dict, hwords: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=None, verbose=False):
        self.words = words
        self.hwords = hwords
        self.sequences = words[this_word]
        self.X, self.lengths = hwords[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None

    def splitted_data(self, word_seq, length, indice):
        tab = np.array(word_seq)[indice]
        mytab = np.array([b for a in tab for b in a])
        ind = np.array(length)[indice]

        return mytab, ind.tolist()

    def max_log(self, model_list):
        if model_list:
            return sorted(model_list, key=lambda u : math.fabs(u[0]))[0][1]
        return self.base_model(self.min_n_components)


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Baysian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on BIC scores
        bestModel = []
        #test = []

        for i in range(self.min_n_components, self.max_n_components+1):
            model = self.base_model(i)
            try:
                logL = model.score(self.X, self.lengths)
                bic = -2 * logL + i * np.log(self.X.shape[0])
                bestModel.append((bic, model))
                #test.append((bic,i))
            except:
                pass

        return self.max_log(bestModel)


class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on DIC scores
        bestModel = []
        other_words = list(self.words.keys())
        other_words.remove(self.this_word)

        #test = []

        for i in range(self.min_n_components, self.max_n_components+1):
            model = self.base_model(i)
            logNL = []
            try:
                logL = model.score(self.X, self.lengths)
                for word in other_words:

                    o_model = self.base_model(i)
                    #o_model = SelectorConstant(self.words, self.hwords, word, i, self.min_n_components, self.max_n_components, self.random_state).select()

                    try:
                        logNL.append(o_model.score(*self.hwords[word]))
                    except:
                         pass
            except:
                pass
            if logNL:
                bestModel.append( (logL - 1/(len(logNL))*sum(logNL), model) )
                #test.append( (logL - 1/(len(logNL))*sum(logNL), i) )

        return self.max_log(bestModel)


class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        nb_samples = np.array(self.sequences).shape[0]

        if nb_samples < 2:
            return self.base_model(2)

        n_folds = 2 if nb_samples <= 2 else 3 if nb_samples < 50 else 10

        split_method = KFold(n_folds)

        bestModel = []
        logL_array = np.array([])
        #test = []

        for i in range(self.min_n_components, self.max_n_components+1):

            for cv_train_idx, cv_test_idx in split_method.split(self.sequences):

                X_train, lengths_train = self.splitted_data(self.sequences, self.lengths, cv_train_idx)
                X_test, lengths_test = self.splitted_data(self.sequences, self.lengths, cv_test_idx)

                try:
                    model = GaussianHMM(n_components=i, covariance_type="diag", n_iter=1000, random_state=self.random_state, verbose=False).fit(X_train, lengths_train)
                    logL_array = np.append(logL_array, model.score(X_test, lengths_test))
                except:
                    pass

            if logL_array.size:
                bestModel.append( (np.mean(logL_array), self.base_model(i)) )
                #test.append( (np.mean(logL_array), i) )

        #print()
        #print(sorted(test, key=lambda u : math.fabs(u[0])))
        return self.max_log(bestModel)