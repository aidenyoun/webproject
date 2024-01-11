from django import forms
from .models import Medicine

class MedicineForm(forms.ModelForm):
    morning_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time'}))
    morning_check = forms.BooleanField(required=False)
    lunch_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time'}))
    lunch_check = forms.BooleanField(required=False)
    dinner_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time'}))
    dinner_check = forms.BooleanField(required=False)

    class Meta:
        model = Medicine
        fields = [
            'name', 'form', 'start_date', 'end_date', 'morning_check', 'morning_time', 'lunch_check', 'lunch_time', 'dinner_check', 'dinner_time'
        ]
