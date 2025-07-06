from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score
import pickle
from sklearn.metrics import accuracy_score


# preparing and splitting data 
df = pd.read_csv('data/clustered_data.csv')
features = ['danceability', 'energy', 'valence', 'acousticness', 'instrumentalness']
X = df[features]
y = df['cluster']
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, max_depth=10, min_samples_leaf=5, random_state=42)
model.fit(X_train, y_train)


y_pred = model.predict(X_test)

# overfitting check
train_pred = model.predict(X_train)
train_acc = accuracy_score(y_train, train_pred)
test_acc = accuracy_score(y_test, y_pred)

importances = model.feature_importances_
for name, importance in zip(features, importances):
    print(f"{name}: {importance:.3f}")

print(f"Train acc: {train_acc:.2f}")
print(f"Test acc: {test_acc:.2f}")

# cross-validation
scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
print(f"CV Accuracy: {scores.mean():.2f} (+/- {scores.std():.2f})")

print(classification_report(y_test, y_pred))

with open('models/random_forest.pkl', 'wb') as f:
    pickle.dump(model, f)

# Accuracy with cross-validation: 0.95

