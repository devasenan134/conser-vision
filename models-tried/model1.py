import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report
import numpy as np
import cv2

(x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()

x_train.shape,x_test.shape


from sklearn.ensemble import RandomForestClassifier
model=RandomForestClassifier()

model.fit(x_train2,y_train)

y_pred = model.predict(x_test2)
y_pred

accuracy_score(y_pred,y_test)
print(classification_report(y_pred,y_test))

confusion_matrix(y_pred,y_test)