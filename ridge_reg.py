import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
def datacleaning(dt):

    dt = dt.iloc[:,2:]
    LabE = LabelEncoder()
    # label = LabE.fit_transform(dt.C_floor)
    # dt.C_floor = label
    label = LabE.fit_transform(dt.district)
    dt.district = label
    district_dummy = pd.get_dummies(dt['district'], drop_first=True, prefix='district')
    dt = pd.concat([district_dummy, dt], axis=1)
    # floor_dummy = pd.get_dummies(dt['C_floor'], drop_first=True, prefix='C_floor')
    # dt = pd.concat([floor_dummy, dt], axis=1)
    dt = dt.drop('district',axis = 1)
    dt = dt.drop('C_floor', axis=1)
    del dt['address']
    del dt['lat']
    del dt['lag']
    per_price = dt.pop('per_price')
    dt.insert(len(dt.columns[:]), 'per_price', per_price)
    del dt['houseid']
    print(dt.dtypes)
    print(dt.isnull().any(axis=0))
    print(dt.iloc[:,:9])
    # nan_rows = dt[dt.isnull().T.any().T]
    # dt = dt.drop(nan_rows)
    return dt

def dtsplit(dt):
    x, y = dt.iloc[:, 0:len(dt.columns[:])-1], dt.iloc[:, len(dt.columns[:])-1]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)
    return x_train, x_test, y_train, y_test

def ridge(a,name,x_train, x_test, y_train,y_test):

    ridge = linear_model.Ridge(alpha=a, fit_intercept=True) 
    ridge.fit(x_train, y_train)
    print(ridge.coef_)
    ridge_coef = pd.DataFrame(ridge.coef_)
    ridge_coef.to_excel(r'D:\case\new-case\ridgecoef'+name+'.xlsx')
    y_pred = ridge.predict(x_test)
    
    plt.figure()
    plt.plot(np.arange(100), y_test[:100], "go-", label="True value")
    plt.plot(np.arange(100), y_pred[:100], "ro-", label="Predict value")
    plt.title(f"Ridge regression")
    plt.legend(loc="best")
    plt.savefig(r'D:\case\new-case\ridge_predict'+name+'.jpg')
    plt.show()
    return y_pred

def ridge_alphafig(dt,name):
    x, y = dt.iloc[:, 0:len(dt.columns[:])-1], dt.iloc[:, len(dt.columns[:])-1]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)
    n_alphas = 200
    alphas = np.logspace(-3, 10, n_alphas)

    coefs = []
    for a in alphas:
        ridge = linear_model.Ridge(alpha=a, fit_intercept=True)  # 每个循环都要重新实例化一个estimator对象
        ridge.fit(x_train, y_train)
        coefs.append(ridge.coef_)

  
    ax = plt.gca()
    ax.plot(alphas, coefs)
    ax.set_xscale('log')
    ax.set_xlim(ax.get_xlim()[::-1])  
    plt.xlabel('alpha')
    plt.ylabel('weights')
    plt.title('Ridge coefficients as a function of the regularization')
    plt.axis('tight')
    plt.savefig(r'D:\case\new-case\ridge_lambda' + name + '.jpg')
    plt.show()

def ridgecv(dt):
    x, y = dt.iloc[:, 0:len(dt.columns[:])-1], dt.iloc[:, len(dt.columns[:])-1]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)
    n_alphas = 200
    alphalist = list(np.logspace(-3, 10, n_alphas))
    ridge = linear_model.RidgeCV(alphas=alphalist,fit_intercept=True)  
    ridge.fit(x_train, y_train)
    # print('Coefficient matrix:\n', ridge.coef_)
    # print('Linear regression model:\n', ridge)
    print('The best alpha value for cross validation',ridge.alpha_)
    a = ridge.alpha_
    return a

def mse(y_test,y_pred):
    mse = mean_squared_error(y_test, y_pred)
    print('MSE: ',mse)
    return mse

def interaction_research(dt):
    dt['area_distance'] = dt.AREA * dt.distance
    dt['area_subway'] = dt.AREA * dt.subway
    # dt['subway_school'] = dt.subway * dt.distance
    dt['floor_distance'] = dt.floor_num * dt.distance
    dt['floor_subway'] = dt.floor_num * dt.subway
    # dt['Cfloor2_school'] = dt.C_floor_2 * dt.school
    # dt['Cfloor2_subway'] = dt.C_floor_2 * dt.subway
    # dt['subway_school'] = dt.subway * dt.school
    # for i in range(1, 10):
    #     name1 = 'dis' + str(i) + '_school'
    #     name2 = 'dis' + str(i) + '_subway'
    #     disname = 'district_' + str(i)
    #     dt[name1] = dt[disname] * dt.school
    #     dt[name2] = dt[disname] * dt.subway
    per_price = dt.pop('per_price')
    dt.insert(len(dt.columns[:]), 'per_price', per_price)
    print(dt.dtypes)
    x_train1, x_test1, y_train1, y_test1 = dtsplit(dt)
    name2 = 'interaction'
    ridge_alphafig(dt,name2)
    alpha2 = ridgecv(dt)
    y_pred_inter = ridge(alpha2,name2,x_train1, x_test1, y_train1, y_test1)
    mse(y_test1, y_pred_inter)


def main(dat,x_train, x_test, y_train, y_test):
    name1 = 'none'
    ridge_alphafig(dat,name1)
    # ridgecv(dt)
    alpha1 = ridgecv(dat)
    y_pred2 = ridge(alpha1,name1,x_train, x_test, y_train, y_test)
    mse2 = mse(y_test, y_pred2)
    interaction_research(dat)
    return y_pred2,mse2


if __name__ == '__main__':
    dt = pd.read_excel(r"D:\case\new-case\enddata.xls")
    dat = datacleaning(dt)
    x_train, x_test, y_train, y_test = dtsplit(dat)
    y_pred2,mse2 = main(dat,x_train, x_test, y_train, y_test)
    print(y_pred2,mse2)


