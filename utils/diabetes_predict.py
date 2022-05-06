import pickle

from django_pandas.io import read_frame
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import missingno as msno
import seaborn as sns
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from sklearn.model_selection import learning_curve
from sklearn.metrics import confusion_matrix, accuracy_score

from xgboost import XGBClassifier
from sklearn.metrics import classification_report,accuracy_score,recall_score,roc_auc_score


def handle_data():
    file_path = r"/home/yuqiuwen/PythonProjects/diabetes.csv"
    df = pd.read_csv(file_path)
    cols = [col for col in df.columns if col not in ['Pregnancies', 'DiabetesPedigreeFunction', 'Age', 'Outcome']]
    df[cols] = df[cols].replace(0, np.nan)

    col_y = 'Outcome'
    col_x = df.columns.to_list()[:-1]

    df_na = df[cols].isna()
    df_mean = df.groupby(col_y)[cols].mean()
    for col in cols:
        na_series = df_na[col]
        names = list(df.loc[na_series, col_y])

        t = df_mean.loc[names, col]
        t.index = df.loc[na_series, col].index

        # 相同的index进行赋值
        df.loc[na_series, col] = t
    # 标准化
    # sc = StandardScaler()
    # sc_df = pd.DataFrame(sc.fit_transform(df.drop([col_y], axis=1)), columns=col_x)
    # x = sc_df
    # y = col_y

    x = df.drop('Outcome', axis=1)
    y = df[col_y]


    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=30/768, random_state=2022)
    xgb = XGBClassifier(gamma=0, use_label_encoder=False, learning_rate=0.1, max_depth=10, n_estimators=1000,
                        reg_lambda=6, reg_alpha=3, verbosity=0)
    xgb.fit(x_train, y_train)
    y_pred = xgb.predict(x_test)
    print(classification_report(y_test, y_pred))
    pickle.dump(xgb, open("pima.pickle.dat", "wb"))

handle_data()