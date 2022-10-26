import numpy as np
import pandas as pd


train_features_path = "data/train_features.csv"
train_labels_path = "data/train_labels.csv"

train_features = pd.read_csv(train_features_path)

print(train_features.head())

# train_x = 