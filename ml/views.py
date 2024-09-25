from ml.models import MashinData
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split

# Create your views here.

def f1(arg):
    return int(arg.replace(' км.', '').replace(',', ''))

def f2(arg):
    return float(arg.replace(' л', '').replace(',', ''))

# queryset = MashinData.objects.all()
# data = list(queryset.values('Uildverlegch', 'Mark', 'Motor_bagtaamj', 'Xrop', 'Uildverlesen_on', 'Hudulguur', 'Hutlugch', 'Yavsan_km', 'Une'))
# dataset = pd.DataFrame(data)
# dataset['Motor_bagtaamj'] = dataset['Motor_bagtaamj'].apply(f2)
# dataset['Yavsan_km'] = dataset['Yavsan_km'].apply(f1)
# dataset['Une'] = dataset['Une'].astype('Int64')
# dataset['Uildverlesen_on'] = dataset['Uildverlesen_on'].astype('Int64')
# dataset = dataset.dropna()

# X = dataset.drop('Une', axis=1)
# y = dataset['Une']
# numerical_features = ['Motor_bagtaamj', 'Uildverlesen_on', 'Yavsan_km']
# categorical_features = ['Uildverlegch', 'Mark', 'Xrop', 'Hudulguur', 'Hutlugch']
# preprocessor = ColumnTransformer(
#     transformers=[
#             ('num', StandardScaler(), numerical_features),
#             ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
#         ]
#     )
# pipeline = Pipeline(
#     steps=[
#         ('preprocessor', preprocessor),
#         ('model', RandomForestRegressor()) 
#     ])
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# pipeline.fit(X_train, y_train)

# def prediction(**args):
#     new_car_data = pd.DataFrame({
#                     'Uildverlegch': [args['Uildverlegch']],
#                     'Mark': [args['Mark']],
#                     'Motor_bagtaamj': [args['Motor_bagtaamj']],  
#                     'Xrop': [args['Xrop']],
#                     'Uildverlesen_on': [args['Uildverlesen_on']], 
#                     'Hudulguur': [args['Hudulguur']],
#                     'Hutlugch': [args['Hutlugch']],
#                     'Yavsan_km': [args['Yavsan_km']]  
#                 })
#     predicted_price = pipeline.predict(new_car_data)[0]
#     return int(predicted_price)

class CarPricePredictor:
    def __init__(self):
        self.pipeline = self.build_pipeline()

    def load_and_prepare_data(self):
        queryset = MashinData.objects.all()
        data = list(queryset.values('Uildverlegch', 'Mark', 'Motor_bagtaamj', 'Xrop', 'Uildverlesen_on', 'Hudulguur', 'Hutlugch', 'Yavsan_km', 'Une'))
        df = pd.DataFrame(data)
        df['Motor_bagtaamj'] = pd.to_numeric(df['Motor_bagtaamj'].str.replace(' л', '').str.replace(',', ''), errors='coerce')
        df['Yavsan_km'] = pd.to_numeric(df['Yavsan_km'].str.replace(' км.', '').str.replace(',', ''), errors='coerce')
        df['Une'] = pd.to_numeric(df['Une'], errors='coerce')
        df['Uildverlesen_on'] = pd.to_numeric(df['Uildverlesen_on'], errors='coerce')
        df = df.dropna()
        df = df[df['Une'] < 1e6]  
        return df

    def build_pipeline(self):
        df = self.load_and_prepare_data()
        X = df.drop('Une', axis=1)
        y = df['Une']
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), ['Motor_bagtaamj', 'Uildverlesen_on', 'Yavsan_km']),
                ('cat', OneHotEncoder(handle_unknown='ignore'), ['Uildverlegch', 'Mark', 'Xrop', 'Hudulguur', 'Hutlugch'])
            ]
        )

        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('model', RandomForestRegressor())
        ])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        pipeline.fit(X_train, y_train)

        return pipeline

    def predict(self, car_features):
        return self.pipeline.predict(car_features)[0]
    
car_price_predictor = CarPricePredictor()