from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, matthews_corrcoef, precision_score, roc_auc_score
import pickle
import sys
sys.path.insert(1, '../')
from error_measurement import matthews_correlation, sensitivity, specificity, auc, f1_score


def cross_val(x_train, y_train, x_test, y_test, folds=10):
    skf = StratifiedKFold(n_splits=folds)

    model = RandomForestClassifier(n_estimators=100, bootstrap=False, random_state=47, verbose=1)
    accuracy = []
    mcc = []
    precision = []
    roc_auc = []
    Sensitivity = []
    Specificity = []
    score = []
    auc_score = []
    f1 = []
    for train_index, test_index in skf.split(x_train, y_train):
        X_train, X_test = x_train[train_index], x_train[test_index]
        Y_train, Y_test = y_train[train_index], y_train[test_index]

        model.fit(X_train, Y_train)
        y_predict = model.predict(X_test)
        # print(y_predict)
        score.append(model.score(X_test, Y_test))

        accuracy.append(accuracy_score(Y_test, y_predict))
        mcc.append(matthews_corrcoef(Y_test, y_predict))
        precision.append(precision_score(Y_test, y_predict))
        roc_auc.append(roc_auc_score(Y_test, y_predict))
        auc_score.append(auc(Y_test, y_predict))
        f1.append(f1_score(Y_test, y_predict))
        Sensitivity.append(sensitivity(Y_test, y_predict))
        Specificity.append(specificity(Y_test, y_predict))

    res = 'Mice SPD3\n'
    res += "{} folds\n".format(folds)
    res += "******************** Cross Validation Score ********************\n"
    res += "Accuracy: {}\n".format(np.mean(accuracy))
    res += "MCC: {}\n".format(np.mean(mcc))
    res += "Precision: {}\n".format(np.mean(precision))
    res += "Roc AUC score: {}\n".format(np.mean(roc_auc))
    res += "AUC score: {}\n".format(np.mean(auc_score))
    res += "F1 score: {}\n".format(np.mean(f1))
    res += "Sensitivity: {}\n".format(np.mean(Sensitivity))
    res += "Specifity: {}\n".format(np.mean(Specificity))

    y_test_predict = model.predict(x_test)
    res += "\n******************** Independent Test Score ********************\n"
    res += "Accuracy: {}\n".format(accuracy_score(y_test, y_test_predict))
    res += "MCC: {}\n".format(matthews_corrcoef(y_test, y_test_predict))
    res += "Precision: {}\n".format(precision_score(y_test, y_test_predict))
    res += "Roc AUC score: {}\n".format(roc_auc_score(y_test, y_test_predict))
    res += "AUC score: {}\n".format(auc(y_test, y_test_predict))
    res += "F1 score: {}\n".format(f1_score(y_test, y_test_predict))
    res += "Sensitivity: {}\n".format(sensitivity(y_test, y_test_predict))
    res += "Specifity: {}\n\n\n".format(specificity(y_test, y_test_predict))
    res += '\n\n\n\n'
    print(res)

    with open('random_forest.txt', 'a') as fp:
        fp.write(res)


if __name__ == '__main__':
    npzfile = np.load('./data/knn_features_mice.npz', allow_pickle=True)
    X_p = npzfile['arr_0']
    Y_p = npzfile['arr_1']
    X_n = npzfile['arr_2']
    Y_n = npzfile['arr_3']

    x_train_p, x_test_p, y_train_p, y_test_p = train_test_split(X_p, Y_p, test_size=0.1, shuffle=True, random_state=47)
    x_train_n, x_test_n, y_train_n, y_test_n = train_test_split(X_n, Y_n, test_size=0.1, shuffle=True, random_state=47)

    print(x_train_p.shape)
    print(x_train_n.shape)
    print(x_test_p.shape)
    print(x_test_n.shape)

    x_train = np.concatenate((x_train_p, x_train_n)).astype(np.float)
    x_test = np.concatenate((x_test_p, x_test_n)).astype(np.float)
    y_train = np.concatenate((y_train_p, y_train_n)).astype(np.float)
    y_test = np.concatenate((y_test_p, y_test_n)).astype(np.float)

    x_train = x_train.reshape(len(x_train), 456)
    x_test = x_test.reshape(len(x_test), 456)

    print(x_train.shape, y_train.shape)
    print(x_test.shape, y_test.shape)
    # svm(x_train, y_train, x_test, y_test)

    pssm_train = x_train[:, :400]
    spd3_train = x_train[:, 400:]

    pssm_test = x_test[:, :400]
    spd3_test = x_test[:, 400:]

    cross_val(spd3_train, y_train, spd3_test, y_test, folds=10)

