from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.datasets import load_boston
import matplotlib.pyplot as plt
import random
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error

def datacleaning(dt):
    dt = dt.iloc[:, 2:]
    LabE = LabelEncoder()
    # label = LabE.fit_transform(dt.C_floor)
    # dt.C_floor = label
    label = LabE.fit_transform(dt.district)
    dt.district = label
    district_dummy = pd.get_dummies(dt['district'], drop_first=True, prefix='district')
    dt = pd.concat([district_dummy, dt], axis=1)
    # floor_dummy = pd.get_dummies(dt['C_floor'], drop_first=True, prefix='C_floor')
    # dt = pd.concat([floor_dummy, dt], axis=1)
    dt = dt.drop('district', axis=1)
    dt = dt.drop('C_floor', axis=1)
    del dt['address']
    del dt['lat']
    del dt['lag']
    per_price = dt.pop('per_price')
    dt.insert(len(dt.columns[:]), 'per_price', per_price)
    del dt['houseid']
    print(dt.dtypes)
    print(dt.isnull().any(axis=0))
    print(dt.iloc[:, :9])
    # nan_rows = dt[dt.isnull().T.any().T]
    # dt = dt.drop(nan_rows)
    return dt

def dtsplit(dt):
    # 下The data set is divided into training set and test set
    x, y = dt.iloc[:, 0:len(dt.columns[:]) - 1], dt.iloc[:, len(dt.columns[:]) - 1]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)
    return x_train, x_test, y_train, y_test

def regtree(dt,x_train, x_test, y_train, y_test):
    feat_labels = dt.columns[0:len(dt.columns[:])-1]

    #Build regression tree model
    forest = DecisionTreeRegressor(criterion='mse', max_depth=5)
    forest.fit(x_train, y_train)

    
    score = forest.score(x_test, y_test)
    y_pred = forest.predict(x_test)

    
    mse = mean_squared_error(y_test, y_pred)
    print('MSE: ',mse)

  
    plt.figure()
    plt.plot(np.arange(100), y_test[:100], "go-", label="True value")
    plt.plot(np.arange(100), y_pred[:100], "ro-", label="Predict value")
    plt.title(f"RandomForest---score:{score}")
    plt.legend(loc="best")
    plt.savefig(r'D:\case\new-case\tree_predict.jpg')
    plt.show()

    # Assess the importance of variables
    importances = forest.feature_importances_
    # im = pd.DataFrame(importances)
    # im.to_excel(r'D:\case\new-case\tree_importance.xlsx')
    print("importance：", importances)
    x_columns = dt.columns[0:len(dt.columns[:])-1]
    print(x_columns)
    indices = np.argsort(importances)[::-1]
    print(indices)
    xlab = []


    for f in range(x_train.shape[1]):
        print("%2d) %-*s %f" % (f + 1, 30, feat_labels[indices[f]], importances[indices[f]]))
        xlab.append(feat_labels[indices[f]])

    # Screening of variables
    threshold = 0.1
    lab = list(feat_labels[importances > threshold])
    x_selected = x_train[lab]
   
    plt.figure(figsize=(10, 6))
    plt.title("importance", fontsize=18)
    plt.ylabel("import level", fontsize=15, rotation=90)
    plt.rcParams['font.sans-serif'] = ["SimHei"]
    plt.rcParams['axes.unicode_minus'] = False
    for i in range(x_columns.shape[0]):
        plt.bar(i, importances[indices[i]], color='orange', align='center')
        plt.xticks(np.arange(x_columns.shape[0]), xlab, rotation=90, fontsize=15)
    plt.savefig(r'D:\case\new-case\tree_importance.jpg')
    plt.show()
    return y_pred,mse
    # # roc
    # y_score = forest.fit(x_train, y_train).decision_function(x_test)
    # fpr, tpr, thersholds = roc_curve(y_test, y_score)
    #
    # roc_auc = auc(fpr, tpr)
    #
    # plt.plot(fpr, tpr, 'k--', label='ROC (area = {0:.2f})'.format(roc_auc), lw=2)
    # plt.show()

def main(dat,x_train, x_test, y_train, y_test):
    y_pred1,mse1 = regtree(dat,x_train, x_test, y_train, y_test)
    return y_pred1,mse1

if __name__ == '__main__':
    dt = pd.read_excel(r"D:\case\new-case\enddata.xls")
    dat = datacleaning(dt)
    x_train, x_test, y_train, y_test = dtsplit(dat)
    main(dat,x_train, x_test, y_train, y_test)