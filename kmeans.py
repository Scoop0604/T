import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import math

def datacleaning():
    dt = pd.read_excel(r"D:\case\new-case\firstdata.xls")
    get_index = dt[(dt['hall'] == '室') | (dt['per_price'] <= 0) | (dt['AREA'] >= 300)|(dt['subway'] == 'no_subway')].index.values
    dt = dt.drop(get_index)
    print(dt['district'])
    dt = dt.astype({'roomnum':'float','hall':'int','AREA':'float','floor_num':'float','subway':'float'})
    LabE = LabelEncoder()
    label = LabE.fit_transform(dt.C_floor)
    dt.C_floor = label
    dt['per_price'] = np.log(dt['per_price'])
    del dt['school']
    print(dt.isnull().any(axis=0))
    # nan_rows = dt[dt.isnull().T.any().T]
    # dt = dt.drop(nan_rows)
    # dt.to_excel(r"D:\case\new-case\enddata.xls")

    return dt

def kmean(input_data):
    distortions = []
    ks = range(1,15)
    for k in ks:
        estimator = KMeans(n_clusters=k)
        estimator.fit(input_data)
        label_pred = estimator.labels_
        distortions.append(estimator.inertia_)
    
    plt.plot(ks, distortions, 'bo-', mfc='r')
    plt.xlabel('number of clusters')
    plt.ylabel('within groups sum of squares')
    plt.title('choose best clusters')
    plt.savefig(r'D:\case\new-case\cluster.jpg')
    plt.show()
    #two-dimensional diagram 
    # x0 = input_data[label_pred == 0]
    # x1 = input_data[label_pred == 1]
    # x2 = input_data[label_pred == 2]
    # plt.figure(1)
    # plt.subplot(1, 2, 1)
    # plt.scatter(x0.iloc[:, 3], x0.iloc[:, 7], c = "red", marker='o', label='label0')
    # plt.scatter(x1.iloc[:, 3], x1.iloc[:, 7], c = "green", marker='*', label='label1')
    # plt.scatter(x2.iloc[:, 3], x2.iloc[:, 7], c = "blue", marker='+', label='label2')
    # plt.subplot(1, 2, 2)
    # plt.scatter(x0.iloc[:, 2], x0.iloc[:, 7], c = "red", marker='o', label='label0')
    # plt.scatter(x1.iloc[:, 2], x1.iloc[:, 7], c = "green", marker='*', label='label1')
    # plt.scatter(x2.iloc[:, 2], x2.iloc[:, 7], c = "blue", marker='+', label='label2')
    # plt.xlabel('petal length')
    # plt.ylabel('petal width')
    # plt.legend(loc=2)
    # plt.show()

def analysis_cluster(input_data):
    estimator = KMeans(n_clusters=5)
    estimator.fit(input_data)
    quantity = pd.Series(estimator.labels_).value_counts()
    print(quantity)
    res0Series = pd.Series(estimator.labels_)
    dt['lab'] = res0Series.values
    group_by_name_year = dt.groupby(['lab','district'])
    result1 = group_by_name_year.size()
    result1.to_excel(r'D:\case\new-case\result1.xls')
    print(group_by_name_year.size())
    group_by_name = dt.groupby('lab')
    result2 = group_by_name[['AREA','per_price','floor_num','subway','roomnum','hall','distance']].mean()
    result2.to_excel(r'D:\case\new-case\result2.xls')
    print(group_by_name[['AREA','per_price','floor_num','subway','roomnum','hall','distance']].mean())



if __name__ == '__main__':
    dt = datacleaning()
    kmean(dt[['AREA','per_price','floor_num','subway','roomnum','hall','distance']])
    analysis_cluster(dt[['AREA','per_price','floor_num','subway','roomnum','hall','distance']])