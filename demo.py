import mysql.connector as mysql
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay


def f1(arg):
    return int(arg.replace(' км.', '').replace(',', ''))

def f2(arg):
    return float(arg.replace(' л', '').replace(',', ''))

def sortingArray(list):
    return list


db=mysql.connect(host='localhost',username='root',password='',database='checkly')
object=db.cursor()
object.execute('SELECT `Uildverlegch`, `Mark`, `Motor_bagtaamj`, `Xrop`, `Torol`, `Uildverlesen_on`, `Hudulguur`, `Hutlugch`, `Yavsan_km`, `Une` FROM `mashin_data`')
fetch=object.fetchall()
object.close()
db.close()


data=[list(row) for row in fetch]
data=np.array(data)

columns = ['Uildverlegch', 'Mark', 'Motor_bagtaamj', 'Xrop', 'Torol', 'Uildverlesen_on', 'Hudulguur', 'Hutlugch', 'Yavsan_km', 'Une']
dataset = pd.DataFrame(data, columns=columns)

dataset['Motor_bagtaamj']=dataset['Motor_bagtaamj'].apply(f2)
dataset['Yavsan_km']=dataset['Yavsan_km'].apply(f1)

dataset.isnull().sum()
dataset = dataset.dropna()

X = dataset.drop('Une', axis=1)
y = dataset['Une'] 

numerical_features = ['Motor_bagtaamj', 'Uildverlesen_on', 'Yavsan_km']
categorical_features = ['Uildverlegch', 'Mark', 'Xrop', 'Torol', 'Hudulguur', 'Hutlugch']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(), categorical_features)
    ])


pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', RandomForestClassifier())
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipeline.fit(X_train, y_train)
new_car_data = pd.DataFrame({
    'Uildverlegch': ['BMW'],
    'Mark': ['X1'],
    'Motor_bagtaamj': [2.0],
    'Xrop': ['Автомат'],
    'Torol': ['Жийп'],
    'Uildverlesen_on': [2011],
    'Hudulguur': ['Бензин'],
    'Hutlugch': ['Хойноо RWD'],
    'Yavsan_km': [66000]
})

predicted_price = pipeline.predict(new_car_data)
print(predicted_price[0])