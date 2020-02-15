# Warnings
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
# %matplotlib inline
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
import spacy

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, fbeta_score
from sklearn.preprocessing import LabelEncoder

from keras.models import Model
from keras.layers import LSTM, Activation, Dense, Dropout, Input, Embedding
from keras.optimizers import RMSprop
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping
nlp = spacy.load("en")

def read_data(file):
    return pd.read_csv(file=file,sep=';', encoding='latin-1', names=['label', 'text','Unnamed','Unnamed','Unnamed'])
# READ IN DATA
msg= pd.read_csv("SmsCollection.csv",sep=';', encoding='latin-1', names=['label', 'text','Unnamed','Unnamed','Unnamed'])

def manipulate_data_format(data):
    data = msg.drop(columns=['Unnamed','Unnamed.1','Unnamed.2'], axis=1)
    data = msg.drop(index=0,axis=0)
    data = msg.reset_index(drop=True)
    return data

# MANIPULATE DATAFORMAT
msg =  msg.drop(columns=['Unnamed','Unnamed.1','Unnamed.2'], axis=1)
msg = msg.drop(index=0,axis=0)
msg  = msg.reset_index(drop=True)


def investigate_data(data, flag):
    if "general" == flag:
        data.info()
        data.groupby('label').describe()
    elif "specific" == flag:
        temp = data.groupby("text")["label"].agg([len, np.max]).sort_values(by="len", ascending=False).head()
        display(temp)
    elif "frequency" == flag:
        data["label"].value_counts().plot(kind='pie', explode=[0, 0.1], figsize=(6,6), autopct='%1.2f%%')
        plt.ylabel("Spam vs Ham")
        plt.legend(["Spam", "Ham"])
        plt.show()
    else:
        data['length'] = data['text'].astype("str").apply(len)
        data['length'].describe()
        data.hist(column='length', by='label', bins=50, figsize=(11, 5))
    return data
# INVESTIGATE DATA AND SENTENCES
# msg.info()
# msg.groupby('label').describe() # GENERAL DESCRIPTION
# top_msg = msg.groupby("text")["label"].agg([len, np.max]).sort_values(by="len", ascending=False).head(5)
# display(top_msg) # SPECIFIC DESCRIPTION

#  VISUALIZE FREQUNCY OF LABLES
# msg["label"].value_counts().plot(kind='pie', explode=[0, 0.1], figsize=(6,6), autopct='%1.2f%%')
# plt.ylabel("Spam vs Ham")
# plt.legend(["Spam", "Ham"])
# plt.show()

# RESEARCHING FEATURES TO TRAIN ON
msg["length"] = msg["text"].astype("str").apply(len)
# msg["length"].describe()

# msg.hist(column='length', by='label', bins=50, figsize=(11, 5))

# PROCESS TEXT AND VECTORISE MESSAGES
sms = msg['text'].copy()
def process_messages(text, stemming=False):
    text = text.translate(str.maketrans('', '', string.punctuation))
    if stemming:
        stemmer = SnowballStemmer('english')
        text = [ stemmer.stem(word) for word in text.split() if word.lower() not in stopwords.words("english")]
        return " ".join(text)
    text = [ word for word in text.split() if word.lower not in stopwords.words('english')]
    return " ".join(text)
sms = sms.astype("str").apply(process_messages)
vector = TfidfVectorizer(encoding="latin-1",strip_accents="unicode", stop_words="english")
features  = vector.fit_transform(sms)
# print(features.shape)
def create_features(data):
    temp = data.astype("str").apply(process_messages)
    vector = TfidfVectorizer(encoding="latin-1",strip_accents="unicode", stop_words="english")
    return vector.fit_transform(temp)

def encode_labels(label):
    return 1 if label == "spam" else 0

msg['label']= msg["label"].apply(encode_labels)

# CLASSIFY AND PREDICT
def set_up_classification(data):
    pass
X_train, X_test, Y_train, Y_test= train_test_split(features, msg['label'],stratify=msg['label'], test_size=0.2)
svc = SVC(kernel='sigmoid', gamma=1.0)
gauss_naive_bayes  = MultinomialNB(alpha=0.2)
clfs = {'SVC':svc, 'NB':gauss_naive_bayes}
def train_clfs(clf, xtrain, ytrain):
    clf.fit(xtrain, ytrain)

def predict_clfs(clf, y):
    return(clf.predict(y))

def get_scores(clf, xtrain, ytrain, xtest, ytest,flag=False):
    pred_scores =[]

    for k, v in clf.items():
        train_clfs(v, xtrain, ytrain)
        pred = predict_clfs(v, xtest)
        if flag:
            pred_scores.append((k, [accuracy_score(ytest, pred),fbeta_score(ytest,pred, beta=1.5, labels=np.unique(pred))])) # Favour Recall
        pred_scores.append((k, [accuracy_score(ytest, pred),fbeta_score(ytest,pred, beta=0.5,labels=np.unique(pred))])) # Favour Precision
    return pred_scores


# sms = sms.astype("str").apply(process_messages)
# vector = TfidfVectorizer(encoding="latin-1",strip_accents="unicode", stop_words="english")
# features  = vector.fit_transform(sms)
# X_train, X_test, Y_train, Y_test= train_test_split(features, msg['label'],stratify=msg['label'], test_size=0.2)
# pred = get_scores(clfs, X_train, Y_train, X_test, Y_test)
# # print(pred)

# df1 = pd.DataFrame.from_dict(dict(pred), orient='index',columns=['Accuracy','F_beta'])
# sms_stem = sms.astype("str").apply(process_messages,args=(True,))
# vector = TfidfVectorizer(encoding="latin-1",strip_accents="unicode", stop_words="english")

# features_stem  = vector.fit_transform(sms_stem)
# X_train_, X_test_, Y_train_, Y_test_= train_test_split(features_stem, msg['label'],stratify=msg['label'], test_size=0.2)
# pred_stem = get_scores(clfs, X_train_, Y_train_, X_test_, Y_test_)
# df2 = pd.DataFrame.from_dict(dict(pred_stem), orient='index',columns=['Accuracy_stem','F_beta_stem'])

# len_features = msg['length'].as_matrix()
# new_len_features = np.hstack((features.todense(),len_features[:,None]))
# new_len_features_stem = np.hstack((features_stem.todense(),len_features[:,None]))

# X_train_len, X_test_len, Y_train_len, Y_test_len= train_test_split(new_len_features, msg['label'],stratify=msg['label'], test_size=0.2)
# pred_len = get_scores(clfs, X_train_len, Y_train_len, X_test_len, Y_test_len,flag=True)
# df3 = pd.DataFrame.from_dict(dict(pred_len), orient='index',columns=['Accuracy_len','F_beta_len'])

# X_train_len_stem, X_test_len_stem, Y_train_len_stem, Y_test_len_stem= train_test_split(new_len_features_stem, msg['label'],stratify=msg['label'], test_size=0.2)
# pred_len_stem = get_scores(clfs, X_train_len_stem, Y_train_len_stem, X_test_len_stem, Y_test_len_stem,flag=True)
# df4 = pd.DataFrame.from_dict(dict(pred_len_stem), orient='index',columns=['Accuracy_len_stem','F_beta_len_stem'])

# df = pd.concat([df1,df2,df3,df4],axis=1)
# df
# df.to_latex(index=False)

# APPLY LSTM ON DATA
# INITIALISE DATA
X = msg['text'].astype("str")
Y = msg['label']
le = LabelEncoder()
Y = le.fit_transform(Y)
Y = Y.reshape(-1, 1)
# print(Y.shape)
# SPLIT DATA
train_X, test_X, train_Y, test_Y = train_test_split(X, Y, test_size=0.15)
# print(train_Y.shape)
# PROCESS DATA PADDING IS TO ENSURE SEQUENCE HAVE SAME SHAPE
# MAX LEN IS ARBITRARY
max_words = 1000
max_len= 150
token = Tokenizer(num_words=max_words)
token.fit_on_texts(train_X.astype("str"))
seq = token.texts_to_sequences(train_X.astype("str"))
seq_matrix = sequence.pad_sequences(seq, maxlen=max_len)

# RNN

def RNN():

    inputs = Input(name='inputs', shape=[max_len])
    layer =Embedding(input_dim=max_words, output_dim=50, input_length=max_len)(inputs)
    layer = LSTM(units=64)(layer)
    layer = Dense(units=256, name='FC1')(layer)
    layer = Activation('relu')(layer)
    layer = Dropout(0.5)(layer)
    layer = Dense(units=1,name='out_layer')(layer)
    layer = Activation('sigmoid')(layer)
    model = Model(inputs=inputs, output=layer)
    return model

model = RNN()
model.summary()
model.compile(loss='binary_crossentropy',optimizer=RMSprop(),metrics=['accuracy'])
# print(seq_matrix.shape, train_Y.shape)
model.fit(seq_matrix, train_Y, batch_size=128, epochs=10,validation_split=0.2,callbacks=[EarlyStopping(monitor='val_loss',min_delta=0.0001)])

test_sequences = token.texts_to_sequences(test_X)
test_sequences_matrix = sequence.pad_sequences(test_sequences,maxlen=max_len)

accuracy = model.evaluate(test_sequences_matrix, test_Y)
print('Test set\n  Loss: {:0.3f}\n  Accuracy: {:0.3f}'.format(accuracy[0],accuracy[1]))