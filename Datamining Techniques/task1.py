import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn import datasets
from sklearn import svm
from sklearn import tree
from sklearn import semi_supervised
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score

from collections import defaultdict

import seaborn as sns
sns.set()

import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

plt.rcParams['figure.figsize'] = [10, 7]
plt.rcParams['axes.grid'] = True

np.set_printoptions(threshold=np.inf)
plt.rcParams['legend.fontsize'] = 15
plt.rcParams['axes.labelpad'] = 10
label_size = 20
plt.rcParams['xtick.labelsize'] = label_size 
plt.rcParams['ytick.labelsize'] = label_size


def plot_pie(target):
    plt.rcParams['figure.figsize'] = [10, 10]
    #           OTHER    AI             CLS                         IS
    colors = ['#808080', '#92FFD8', '#9FABB9','#000000','#4044A7', '#01288F']

    target_dict = target.value_counts().to_dict()
    fig, ax = plt.subplots()
    print(target_dict)
    print(target_dict.values())
    slices, labels = ax.pie(target_dict.values(), colors=colors) # labels=target_dict.keys(),
    # plt.legend()
    center = slices[0].center
    r = slices[0].r
    circle = matplotlib.patches.Circle(center, r, fill=False, edgecolor="k", linewidth=2)
    # add the circle to the axes
    ax.add_patch(circle)
    plt.tight_layout()
    fig.savefig(THIS_FOLDER + '/figures/piechart_lecture.pdf', format='pdf')
    plt.show()


def plot_bar(target):
    plt.rcParams['figure.figsize'] = [10, 4]
    # target_dict = target.value_counts().to_dict()
    print(target)
    fig, ax = plt.subplots()

    ax = sns.distplot(target, bins=range(12))
    plt.xticks(np.arange(0.5, 11.5, 1), range(0,12))
    ax.set_ylabel("Percentage of\n students", fontsize=22)
    ax.set_xlabel("Numbers chosen by students", fontsize=22)
    plt.tight_layout()
    fig.savefig(THIS_FOLDER + '/figures/random_number.pdf', format='pdf')
    plt.show()

def CV(inputs, target):
    plt.rcParams['figure.figsize'] = [10, 4]
    # clf = svm.SVC(kernel='linear', C=1)
    # clf = tree.DecisionTreeClassifier()
    clf = semi_supervised.LabelPropagation(kernel='rbf')
    accs = []
    stds = []
    for k in range(2, 21):
        scores = cross_val_score(clf, inputs, target, cv=k, scoring='accuracy')
        accs.append(scores.mean())
        stds.append(scores.std() * 2)
        print(scores.mean())
    fig, ax = plt.subplots()
    plt.xticks(range(2, 21))
    plt.xlim(1.5,20.5)
    plt.ylim(0.25,0.68)

    ax.set_xlabel("Number of folds", fontsize=22)
    ax.set_ylabel("Score", fontsize=22)
    plt.tight_layout()
    ax = plt.errorbar(range(2,21), accs, stds, fmt='-o', capsize=5)
    fig.savefig(THIS_FOLDER + '/figures/CV_diff_k.pdf', format='pdf')
    plt.show()
    print(max(accs))


def main(num):
    odi_df = pd.read_csv("ODI-2019-csv.csv", sep=";")
    odi_df.columns = ["timestamp", "programme", "course_machine_learning", "course_information_retrieval", "course_statistics", "course_databases",
                      "gender", "chocolate_effect", "birthday", "count_neighbors",
                      "stand_up", "competition", "random_number", "bed_time", "good_day1", "good_day2", "stress_level"]
    # A
    if num == 0:
        target = odi_df.iloc[:,12]

        target = target[target.str.len() < 10]
        target = target.str.replace(r'(,)', '.')
        target = pd.to_numeric(target, errors='coerce').dropna()
        target = target.astype(np.float64)
        target = target[target<11]
        target = target[target == target // 1]
        target = target.astype(np.int32)

        plot_bar(target)


    # B
    elif num == 1:
        odi_df = odi_df.iloc[:,1:6]

        ''' inputs '''
        inputs = odi_df.drop("programme", axis=1)
        inputs = odi_df[inputs.columns[:]].apply(LabelEncoder().fit_transform)

        '''target'''
        target = odi_df.ix[:,0].str.lower()

        target = target.str.replace(r'(^.*artificial intelligence.*$)', 'ai')
        target = target.str.replace(r'(^.*master ai.*$)', 'ai')
        target = target.str.replace(r'(^.*uva ai.*$)', 'ai')

        target = target.str.replace(r'(^.*computer science.*$)', 'cs')

        target = target.str.replace(r'(^.*cls.*$)', 'cls')
        target = target.str.replace(r'(^.*computational science.*$)', 'cls')
        target = target.str.replace(r'(^.*compuational science.*$)', 'cls')

        target = target.str.replace(r'(^.*bioinformatics.*$)', 'bsb')
        target = target.str.replace(r'(^.*information.*$)', 'is')

        target = target.str.replace(r'(^.*tqm.*$)', 'other')
        target = target.str.replace(r'(^.*ba.*$)', 'other')
        target = target.str.replace(r'(^.*qrm.*$)', 'other')
        target = target.str.replace(r'(^.*x.*$)', 'other')
        target = target.str.replace(r'(^.*eor.*$)', 'other')
        target = target.str.replace(r'(^.*mba.*$)', 'other')
        target = target.str.replace(r'(^.*ms.*$)', 'other')
        target = target.str.replace(r'(^.*ds.*$)', 'other')
        target = target.str.replace(r'^.*.{4,}.*$', 'other')

        plot_pie(target)

        # CV(inputs, target)

        X_train, X_test, y_train, y_test = train_test_split(inputs, target, test_size=0.4, random_state=0)
        clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
        print(clf.score(X_test, y_test))


if __name__ == '__main__':
    main(1)