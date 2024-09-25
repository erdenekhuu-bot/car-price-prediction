from django import forms
import mysql.connector as mysql
from ml.models import MashinData
import numpy as np
import pandas as pd


queryset = MashinData.objects.all()
data = list(queryset.values('Uildverlegch', 'Mark', 'Motor_bagtaamj', 'Xrop', 'Uildverlesen_on', 'Hudulguur', 'Hutlugch', 'Yavsan_km', 'Une'))
dataset = pd.DataFrame(data)

class Checkly(forms.Form):
    choose_uildverlegch = []
    for manufacturer in np.unique(dataset['Uildverlegch']):
        choose_uildverlegch.append((manufacturer,manufacturer))

    choose_mark=[]
    for mark in np.unique(dataset['Mark']):
        choose_mark.append((mark,mark))
    choose_xrop = []
    for xrop in np.unique(dataset['Xrop']):
        choose_xrop.append((xrop,xrop))

    choose_hudulguur = []
    for hudulguur in np.unique(dataset['Hudulguur']):
        choose_hudulguur.append((hudulguur, hudulguur))
    
    choose_hutlugch=[]
    for hutlugch in np.unique(dataset['Hutlugch']):
        choose_hutlugch.append((hutlugch, hutlugch))
    
    Uildverlegch = forms.ChoiceField(
        choices=choose_uildverlegch,
        widget=forms.Select(attrs={'class': 'form-select manufacturer', 'aria-label': 'Машин үйлдвэрлэгч'}),
        required=True,
    )
    Mark = forms.ChoiceField(
        choices=choose_mark,
        widget=forms.Select(attrs={'class': 'form-select manufacturer-mark', 'aria-label': 'Машины марк'}),
        required=True,
    )
    Motor_bagtaamj = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control avaliable-all', 'placeholder': 'Моторын багтаамж'}),
        required=True,
    )
    Xrop = forms.ChoiceField(
        choices=choose_xrop, 
        widget=forms.Select(attrs={'class': 'form-select', 'aria-label': 'Машины хроп'}),
        required=True,
    )
    Uildverlesen_on = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Үйлдвэрлэсэн он'}),
        required=True,
    )
    Hudulguur = forms.ChoiceField(
        choices=choose_hudulguur, 
        widget=forms.Select(attrs={'class': 'form-select', 'aria-label': 'Хөдөлгүүрийн төрөл'}),
        required=True,
    )
    Hutlugch = forms.ChoiceField(
        choices=choose_hutlugch, 
        widget=forms.Select(attrs={'class': 'form-select', 'aria-label': 'Машины хөтлөгч'}),
        required=True,
    )
    Yavsan_km = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Машины нийт явсан километр'}),
        required=True,
    )
    # Yavsan_km = forms.IntegerField(
    #     widget=forms.NumberInput(attrs={'class': 'form-control avaliable-all', 'placeholder': 'Машины нийт явсан километр', 'disabled':'disabled'}),
    #     required=True,
    # )