from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from .form import Checkly
from ml.models import MashinData
import mysql.connector as mysql
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

# Create your views here.

def f1(arg):
    return int(arg.replace(' км.', '').replace(',', ''))

def f2(arg):
    return float(arg.replace(' л', '').replace(',', ''))

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
    ]
)


pipeline = Pipeline(
     steps=[
        ('preprocessor', preprocessor),
        ('model', RandomForestClassifier())
    ]
)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipeline.fit(X_train, y_train)

def home(request):
     return render(request, 'home.html')

def predict(request):
     return render(request, 'predict_first.html')

def predict_second(request):
     return render(request, 'predict_second.html')

def result(request):
     return render(request, 'result.html')

def upload(request):
     form = Checkly()
     return render(request, 'estimate/upload.html', {'form': form})

def predict(request):
    if request.method == 'POST':
        form = Checkly(request.POST)
        if form.is_valid():
             new_car_data = pd.DataFrame({
                'Uildverlegch': [form.cleaned_data['Uildverlegch']],
                'Mark': [form.cleaned_data['Mark']],
                'Motor_bagtaamj': [form.cleaned_data['Motor_bagtaamj']],
                'Xrop': [form.cleaned_data['Xrop']],
                'Torol': [form.cleaned_data['Torol']],
                'Uildverlesen_on': [form.cleaned_data['Uildverlesen_on']],
                'Hudulguur': [form.cleaned_data['Hudulguur']],
                'Hutlugch': [form.cleaned_data['Hutlugch']],
                'Yavsan_km': [form.cleaned_data['Yavsan_km']]
             })
             predicted_price = pipeline.predict(new_car_data)
             return HttpResponse(predicted_price[0])
    else:
        form = Checkly()
    return HttpResponse("0")


@require_GET
def searchMark(request):
    manufacturer = request.GET.get("manufacturer")
        
    if manufacturer is None:
        return JsonResponse({"error": "Manufacturer parameter is missing"}, status=400)

    try:
        db = mysql.connect(host='localhost', username='root', password='', database='checkly')
        cursor = db.cursor()
        query = 'SELECT DISTINCT Mark FROM mashin_data WHERE Uildverlegch = %s'
        cursor.execute(query, (manufacturer,))
        marks = cursor.fetchall()
        cursor.close()
        db.close()

        mark_choices = [mark[0] for mark in marks]
        return JsonResponse({'marks': mark_choices})
        
    except mysql.Error as e:
            return JsonResponse({"error": str(e)}, status=500)
        
    return JsonResponse({"error": "Invalid request method"}, status=405)