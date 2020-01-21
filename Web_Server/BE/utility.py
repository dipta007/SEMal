from feature_extract import get_bigrams
import pickle


def get_bigrams_utility(protein, pssm, spd3):
    seq = ""
    for p in protein:
        if p == 'K':
            seq += '1'
        else:
            seq += '2'

    [X, ind] = get_bigrams(protein, seq, '1', pssm, spd3)
    return [X, ind]


def predict_for_mice(x):
    model = pickle.load(open('../../data/rotation_forest_mice.pkl', 'rb'))
    y_test_predict = model.predict(x)
    return y_test_predict


def predict_for_human(x):
    model = pickle.load(open('../../data/rotation_forest_human.pkl', 'rb'))
    y_test_predict = model.predict(x)
    return y_test_predict


def get_result(pssm, spd3, species):
    protein = ""
    for val in spd3[1:]:
        if len(val.split()) >= 2:
            protein += val.split()[1]

    [X, ind] = get_bigrams_utility(protein, pssm, spd3)
    if species == 'human':
        Y = predict_for_human(X)
    else:
        Y = predict_for_mice(X)
    res = ''
    ind = 0
    for p in protein:
        if p == 'K':
            if Y[ind] == 1:
                res += '1'
            else:
                res += '0'
            ind += 1
        else:
            res += '2'
    return '{}\n{}'.format(protein, res)

