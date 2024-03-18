from django.forms import ModelForm
from .models import Medicine, CATEGORY
from accounts.models import User
from datetime import datetime
from django import forms
from accounts.models import InstitutionCode

class UpdateStockForm(ModelForm):

    class Meta:
        model = Medicine
        fields = ['name', 'stock','category', 'memo']    


class MedicineFilterForm(forms.Form):
    
    institution_name = forms.ModelChoiceField(queryset=User.objects.filter(institution_code=9), label='施設名')
