import mysql.connector as mysql
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, r2_score

def f1(arg):
    return int(arg.replace(' км.', '').replace(',', ''))

def f2(arg):
    return float(arg.replace(' л', '').replace(',', ''))

db = mysql.connect(host='localhost', username='root', password='', database='checkly')
cursor = db.cursor()
cursor.execute('SELECT `Uildverlegch`, `Mark`, `Motor_bagtaamj`, `Xrop`, `Uildverlesen_on`, `Hudulguur`, `Hutlugch`, `Yavsan_km`, `Une` FROM `mashin_data`')
fetch = cursor.fetchall()
cursor.close()
db.close()
data = [list(row) for row in fetch]
data = np.array(data)

columns = ['Uildverlegch', 'Mark', 'Motor_bagtaamj', 'Xrop', 'Uildverlesen_on', 'Hudulguur', 'Hutlugch', 'Yavsan_km', 'Une']
dataset = pd.DataFrame(data, columns=columns)


dataset['Motor_bagtaamj'] = dataset['Motor_bagtaamj'].apply(f2)
dataset['Yavsan_km'] = dataset['Yavsan_km'].apply(f1)
dataset['Une'] = dataset['Une'].astype('Int64')
dataset['Uildverlesen_on'] = dataset['Uildverlesen_on'].astype('Int64')
dataset = dataset.dropna()

X = dataset.drop('Une', axis=1)
y = dataset['Une']
numerical_features = ['Motor_bagtaamj', 'Uildverlesen_on', 'Yavsan_km']
categorical_features = ['Uildverlegch', 'Mark', 'Xrop', 'Hudulguur', 'Hutlugch']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ]
)
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', RandomForestRegressor()) 
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

default_values = {
    'Uildverlegch': 'Mercedes-Benz',  
    'Mark': 'E-Class',            
    'Xrop': 'Автомат',       
    'Hudulguur': 'Бензин',   
    'Hutlugch': 'Бүх дугуй 4WD'  
}

new_car_data = pd.DataFrame({
    'Uildverlegch': [default_values['Uildverlegch']],
    'Mark': [default_values['Mark']],
    'Motor_bagtaamj': [3.5],  
    'Xrop': [default_values['Xrop']],
    'Uildverlesen_on': [2011], 
    'Hudulguur': [default_values['Hudulguur']],
    'Hutlugch': [default_values['Hutlugch']],
    'Yavsan_km': [10]  
})

predicted_price = pipeline.predict(new_car_data)[0]
print(int(predicted_price))