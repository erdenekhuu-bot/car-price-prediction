from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_protect
from pages.form import Checkly
from ml.models import MashinData
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier

# Create your views here.

def f1(arg):
    return int(arg.replace(' км.', '').replace(',', ''))

def f2(arg):
    return float(arg.replace(' л', '').replace(',', ''))

queryset = MashinData.objects.all()
data = list(queryset.values('Uildverlegch', 'Mark', 'Motor_bagtaamj', 'Xrop', 'Uildverlesen_on', 'Hudulguur', 'Hutlugch', 'Yavsan_km', 'Une'))
dataset = pd.DataFrame(data)

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
    ('model', RandomForestClassifier()) 
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
pipeline.fit(X_train, y_train)

def home(request):
     return render(request, 'home.html',{'active_page':'home'})

def about_us(request):
     return render(request, 'about_us.html',{'active_page':'about'})

def predict_second(request):
    form = Checkly()
    return render(request, 'car_input.html',{'form': form})

def login(request):
     return render(request,'register/login.html')

def signup(request):
     return render(request,'register/signup.html')

def policy(request):
    return render(request, 'policy.html')

@csrf_protect
def predict(request):
    if request.method == 'POST':
        try:
            form = Checkly(request.POST)
            if form.is_valid():
                new_car_data = pd.DataFrame({
                    'Uildverlegch': [form.cleaned_data['Uildverlegch']],
                    'Mark': [form.cleaned_data['Mark']],
                    'Motor_bagtaamj': [form.cleaned_data['Motor_bagtaamj']],  
                    'Xrop': [form.cleaned_data['Xrop']],
                    'Uildverlesen_on': [form.cleaned_data['Uildverlesen_on']], 
                    'Hudulguur': [form.cleaned_data['Hudulguur']],
                    'Hutlugch': [form.cleaned_data['Hutlugch']],
                    'Yavsan_km': [form.cleaned_data['Yavsan_km']]  
                })
                predicted_price = pipeline.predict(new_car_data)[0]
                return JsonResponse({'predicted_price': int(predicted_price)}, status=200)
            else:
                return JsonResponse({"error": "Invalid form data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

@require_GET
def searchMark(request):
    manufacturer = request.GET.get("manufacturer")
    try:
        marks_queryset = MashinData.objects.filter(Uildverlegch=manufacturer).values_list('Mark', flat=True).distinct()
        mark_choices = list(marks_queryset)
        return JsonResponse({'marks': mark_choices})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)