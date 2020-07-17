from rotation_forest import RotationForestClassifier
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, matthews_corrcoef, precision_score, roc_auc_score
from error_measurement import matthews_correlation, sensitivity, specificity, auc, f1_score
import pickle


def svm(x_train, y_train, x_test, y_test):
    model = RotationForestClassifier(n_estimators=100, random_state=47, verbose=4)
    # model = SVC(C=1.0, kernel='poly', gamma=1.0, random_state=47, verbose=True)
    model.fit(x_train, y_train)

    with open('./data/svm-knn.pkl', 'wb') as f:
        pickle.dump(model, f)

    y_predict = model.predict(x_test)
    print("****************************************")
    print("Accuracy: ", accuracy_score(y_test, y_predict))
    print("MCC: ", matthews_corrcoef(y_test, y_predict))
    print("Precision: ", precision_score(y_test, y_predict))
    print("ROC auc score: ", roc_auc_score(y_test, y_predict))
    print("AUC def: ", auc(y_test, y_predict))
    print("F1 score: ", f1_score(y_test, y_predict))
    print("Sensitivity: ", sensitivity(y_test, y_predict))
    print("Specifity: ", specificity(y_test, y_predict))


def cross_val(x_train, y_train):
    skf = StratifiedKFold(n_splits=10)

    model = RotationForestClassifier(n_estimators=100, random_state=47, verbose=4, n_jobs=-2)
    accuracy = []
    mcc = []
    precision = []
    roc_auc = []
    Sensitivity = []
    Specificity = []
    score = []
    f1 = []
    for x in range(10):
        for train_index, test_index in skf.split(x_train, y_train):
            X_train, X_test = x_train[train_index], x_train[test_index]
            Y_train, Y_test = y_train[train_index], y_train[test_index]

            model.fit(X_train, Y_train)
            y_predict = model.predict(X_test)
            score.append(model.score(X_test, Y_test))

            accuracy.append(accuracy_score(Y_test, y_predict))
            mcc.append(matthews_corrcoef(Y_test, y_predict))
            precision.append(precision_score(Y_test, y_predict))
            f1.append(f1_score(Y_test, y_predict))
            roc_auc.append(roc_auc_score(Y_test, y_predict))
            Sensitivity.append(sensitivity(Y_test, y_predict))
            Specificity.append(specificity(Y_test, y_predict))

    with open('./data/rotation_forest_knn_human100.pkl', 'wb') as f:
        pickle.dump(model, f)

    print("****************************************")
    print("Accuracy: ", np.mean(accuracy))
    print("MCC: ", np.mean(mcc))
    print("Precision: ", np.mean(precision))
    print("Roc auc score: ", np.mean(roc_auc))
    print("F1 score: {}\n".format(np.mean(f1)))
    print("Sensitivity: ", np.mean(Sensitivity))
    print("Specifity: ", np.mean(Specificity))


def robust_cross_val(x_train, y_train, x_test, y_test, folds):
    skf = StratifiedKFold(n_splits=folds)

    model = RotationForestClassifier(n_estimators=100, random_state=47, verbose=4, n_jobs=-2)
    accuracy = []
    mcc = []
    precision = []
    roc_auc = []
    Sensitivity = []
    Specificity = []
    auc_score = []
    f1 = []
    score = []

    for x in range(1):
        for train_index, test_index in skf.split(x_train, y_train):
            X_train, X_test = x_train[train_index], x_train[test_index]
            Y_train, Y_test = y_train[train_index], y_train[test_index]

            model.fit(X_train, Y_train)
            y_predict = model.predict(X_test)
            score.append(model.score(X_test, Y_test))

            accuracy.append(accuracy_score(Y_test, y_predict))
            mcc.append(matthews_corrcoef(Y_test, y_predict))
            precision.append(precision_score(Y_test, y_predict))
            roc_auc.append(roc_auc_score(Y_test, y_predict))
            auc_score.append(auc(Y_test, y_predict))
            f1.append(f1_score(Y_test, y_predict))
            Sensitivity.append(sensitivity(Y_test, y_predict))
            Specificity.append(specificity(Y_test, y_predict))

    with open('./data/rotation_forest_knn_robust_human100.pkl', 'wb') as f:
        pickle.dump(model, f)

    res = "Human\n"
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

    with open('rof.txt', 'a') as f:
        f.write(res)


if __name__ == '__main__':
    npzfile = np.load('./data/knn_features_human100.npz', allow_pickle=True)
    X_p = npzfile['arr_0']
    Y_p = npzfile['arr_1']
    X_n = npzfile['arr_2']
    Y_n = npzfile['arr_3']

    print(X_p.shape, X_n.shape)

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

    pssm_train = x_train[:, :400]
    spd3_train = x_train[:, 400:]

    pssm_test = x_test[:, :400]
    spd3_test = x_test[:, 400:]

    robust_cross_val(x_train, y_train, x_test, y_test, 10)
