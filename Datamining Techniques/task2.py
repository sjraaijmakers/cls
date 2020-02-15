import pandas as pd
import numpy as np
import re
import seaborn as sns
sns.set()

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# SKlearn Classifiers
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

# function from https://www.kaggle.com/sinakhorami/titanic-best-working-classifier/notebook
def get_title(name):
	title_search = re.search(" ([A-Za-z]+)\.", name)
	if title_search:
		return title_search.group(1)
	return ""

def age_map(age):
    if age <= 11:
        return 0
    elif age > 11 and age <= 18:
        return 1
    elif age > 18 and age <= 22:
        return 2
    elif age > 22 and age <= 27:
        return 3
    elif age > 27 and age <= 33:
        return 4
    elif age > 33 and age <= 40:
        return 5
    elif age > 40:
        return 6

def title_map(title):
    if title == "Mr":
        return 1
    elif title == "Miss" or title == "Mlle" or title == "Ms":
        return 2
    elif title == "Mrs" or title == "Mme":
        return 3
    elif title == "Master":
        return 4
    elif title in ["Lady", "Countess","Capt", "Col", "Don", "Dr", "Major", "Rev", "Sir", "Jonkheer", "Dona"]:
        return 5

def fare_map(fare):
    if fare <= 7.91:
        return 0
    elif fare > 7.91 and fare <= 14.454:
        return 1
    elif fare > 14.454 and fare <= 31:
        return 2
    elif fare > 31 and fare <= 99:
        return 3
    elif fare > 99 and fare <= 250:
        return 4
    elif fare > 250:
        return 5

def main():
    train = pd.read_csv("train.csv")
    test = pd.read_csv("test.csv")
    total = pd.concat([train, test], sort=False)

    # Add features
    total["Has_Cabin"] = total["Cabin"].apply(lambda x: False if type(x) is float else True)
    total["Is_Alone"] = (total["SibSp"] + total["Parch"]).apply(lambda x: True if x == 0 else False)

    # title
    total["Title"] = total["Name"].apply(get_title)
    total["Title"] = total["Title"].apply(title_map)

    # Age
    age_mean = total["Age"].mean()
    age_std = total["Age"].std()
    a_cpy = total["Age"].copy()
    np.random.seed(1)
    a_cpy[a_cpy.isnull()] = np.random.randint(age_mean - age_std, age_mean + age_std, size=total["Age"].isnull().sum())
    total["Age"] = a_cpy
    total["Age"] = total["Age"].astype(int)
    total["Age_Cat"] = total["Age"].apply(age_map)
    
    # Rest
    total["Embarked"] = total["Embarked"].fillna("S")

    total["Fare"] = total["Fare"].fillna(0)
    total["Fare"] = total["Fare"].apply(np.round)
    total["Fare"] = total["Fare"].astype(int)
    total["Fare"] = total["Fare"].apply(fare_map)

    total["Name_Len"] = total["Name"].apply(lambda x: len(x))
    total["Name_Len"] = (total["Name_Len"]/10).astype(np.int64)

    # drop (irrelevant) columns
    total = total.drop(["Cabin", "Ticket", "Age", "SibSp", "Parch", "Name"], axis=1)

    # Map strings to int values
    total["Sex"] = total["Sex"].replace({"male": 0, "female": 1})
    total["Embarked"] = total["Embarked"].replace({"S": 0, "C": 1, "Q": 2})
    total["Has_Cabin"] = total["Has_Cabin"].replace({False: 0, True: 1})
    total["Is_Alone"] = total["Is_Alone"].replace({False: 0, True: 1})
    
    train["Survived"] = train["Survived"].astype(int)

    # Divide "total" back to train and test set
    train = total[total["Survived"].notnull()]
    test = total[total["Survived"].isnull()]
    test = test.drop(["Survived"], axis=1)

    # 
    features = ["Pclass", "Sex", "Embarked", "Has_Cabin", "Is_Alone", "Age_Cat", "Title", "Name_Len", "Fare"]

    #
    X_train, X_test, y_train, y_test = train_test_split(train[features], train["Survived"], test_size=0.33, shuffle=False)

    # RFC
    estimators = np.arange(10, 200, 10)
    accs = []

    for e in estimators:
        rfc = RandomForestClassifier(n_estimators=e)
        rfc.fit(X_train, y_train)
        c_predict = rfc.predict(X_test)
        accuracy = accuracy_score(y_test, c_predict)
        accs.append(accuracy)

    ax = sns.lineplot(x=estimators, y=accs)
    ax.set(xlabel="# estimators", ylabel="Accuracy")
    ax.figure.savefig("lp.pdf")    

    # K nearest
    ks = np.arange(1, 9, 1)
    accs2 = []
    for k in ks:
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train, y_train)
        c_predict = knn.predict(X_test)
        accuracy = accuracy_score(y_test, c_predict)
        accs2.append(accuracy)

    ax2 = sns.lineplot(x=ks, y=accs2)
    ax2.set(xlabel="# neighbors", ylabel="Accuracy")
    ax2.figure.savefig("knn.pdf")   

    ax = sns.barplot(x=features, y=rfc.feature_importances_)
    ax.set(ylabel="importance")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, fontsize=7)
    ax.figure.savefig("feature_importance.pdf")

    winner = RandomForestClassifier(n_estimators=30)
    winner.fit(train[features], train["Survived"])
    p = winner.predict(test[features])
    test["Survived"] = winner.predict(test[features]).astype(int)

    # Create csv for kaggle
    test[["PassengerId", "Survived"]].to_csv("kaggle.csv", index=False)


if __name__ == "__main__":
    main()