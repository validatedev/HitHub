from include import *
from util import *

args = ArgParser()
modelPath = args.model
inputPath = args.input

scalerModelName = "classifiers_dump/robustscaler.sav"
svmModelName = "classifiers_dump/svm_clf.sav"
nbModelName = "classifiers_dump/nb_clf.sav"
knnModelName = "classifiers_dump/knn_clf.sav"

annModelName = "saved_model/ann_clf"

# Load essential classes and trained classifiers from model

with open(modelPath + scalerModelName, 'rb') as modelFile:
    robust_scaler_fitted = pickle.load(modelFile)

with open(modelPath + svmModelName, 'rb') as modelFile:
    best_svm_clf = pickle.load(modelFile)

with open(modelPath + nbModelName, 'rb') as modelFile:
    best_nb_clf = pickle.load(modelFile)

with open(modelPath + knnModelName, 'rb') as modelFile:
    best_knn_clf = pickle.load(modelFile)

best_ann_clf = tf.keras.models.load_model(modelPath + annModelName)

df = getTracksFeatures(inputPath)
df = df.drop(columns=['track_href', 'analysis_url', 'uri', 'id', 'type'])

# Scale
df[df.columns] = robust_scaler_fitted.transform(df[df.columns])

# column check
columns_list = ['danceability', 'energy', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness',
                'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']
df = df[columns_list]

df = df.drop(columns=['tempo', 'mode'])

# SVM Prediction
y_pred_svm = best_svm_clf.predict(df)
print("SVM Prediction")
print(y_pred_svm)

# Naive Bayes Prediction
y_pred_nb = best_nb_clf.predict(df)
print("Naive Bayes Prediction")
print(y_pred_nb)

# KNN Prediction
y_pred_knn = best_knn_clf.predict(df)
print("K-Nearest Neighbor Prediction")
print(y_pred_knn)

# ANN Prediction
y_pred_ann = best_ann_clf.predict(df)
y_pred_ann = y_pred_ann.reshape(y_pred_ann.shape[0], ).round().astype(int)
print("Neural Network Prediction")
print(y_pred_ann)
