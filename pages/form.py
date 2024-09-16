from django import forms
import mysql.connector as mysql
import numpy as np
import pandas as pd


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

class Checkly(forms.Form):
    choose_uildverlegch = []
    for manufacturer in np.unique(dataset['Uildverlegch']):
        choose_uildverlegch.append((manufacturer,manufacturer))

    choose_xrop = []
    for xrop in np.unique(dataset['Xrop']):
        choose_xrop.append((xrop,xrop))
    
    choose_torol = []
    for torol in np.unique(dataset['Torol']):
        choose_torol.append((torol,torol))

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
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select manufacturer-mark', 'aria-label': 'Машины марк', 'disabled':'disabled'}),
        required=True,
    )
    Motor_bagtaamj = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control avaliable-all', 'placeholder': 'Моторын багтаамж', 'disabled':'disabled'}),
        required=True,
    )
    Xrop = forms.ChoiceField(
        choices=choose_xrop, 
        widget=forms.Select(attrs={'class': 'form-select avaliable-all', 'aria-label': 'Машины хроп', 'disabled':'disabled'}),
        required=True,
    )
    Torol = forms.ChoiceField(
        choices=choose_torol, 
        widget=forms.Select(attrs={'class': 'form-select avaliable-all', 'aria-label': 'Машины төрөл', 'disabled':'disabled'}),
        required=True,
    )
    Uildverlesen_on = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control avaliable-all', 'placeholder': 'Үйлдвэрлэсэн он', 'disabled':'disabled'}),
        required=True,
    )
    Hudulguur = forms.ChoiceField(
        choices=choose_hudulguur, 
        widget=forms.Select(attrs={'class': 'form-select avaliable-all', 'aria-label': 'Хөдөлгүүрийн төрөл', 'disabled':'disabled'}),
        required=True,
    )
    Hutlugch = forms.ChoiceField(
        choices=choose_hutlugch, 
        widget=forms.Select(attrs={'class': 'form-select avaliable-all', 'aria-label': 'Машины хөтлөгч', 'disabled':'disabled'}),
        required=True,
    )
    Yavsan_km = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control avaliable-all', 'placeholder': 'Машины нийт явсан километр', 'disabled':'disabled'}),
        required=True,
    )