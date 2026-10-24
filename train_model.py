
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

file_path = "dataset/Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv"
data = pd.read_csv(file_path, low_memory=False)

data.columns = data.columns.str.strip()


import numpy as np

data = data.replace([np.inf, -np.inf], np.nan)#np.inf is positive infinity 

#it removes row containing missing values 
data = data.dropna()


X = data.drop(columns=["Label"])
y = data["Label"].map({"BENIGN": 0, "PortScan": 1})

# 5. Keep only the two classes we want
valid = y.notna()
X = X[valid]
y = y[valid].astype(int)

X = X.select_dtypes(include=["number"])


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)


model = RandomForestClassifier(
    n_estimators=100, random_state=42, n_jobs=-1
)
model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("Training records:", len(X_train))
print("Testing records:", len(X_test))
print("Accuracy:", round(accuracy_score(y_test, predictions) * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(
    y_test, predictions, target_names=["BENIGN", "PortScan"]
))

print("Confusion Matrix ")
print(confusion_matrix(y_test, predictions))

joblib.dump(model, "traffic_classifier.pkl")
