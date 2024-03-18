from typing import Any
from django import forms
from .models import Room, Message
from accounts.models import InstitutionCode, User

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('name', 'user_id', 'user_code', 'recipient_code')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recipient_code'].queryset = InstitutionCode.objects.all()

class AddRoomForm(forms.ModelForm):

    class Meta:
        model = Room
        fields = ['name', 'user_code','recipient_code'] 
        
        error_messages = {
            "name": {"requied": "ルーム名が入力されていません",},
            "recipient_code": {"requied": "参加者を選択してください", }
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user_code"].disabled = True
        
        
    def clean(self):
        cleaned_data = super().clean()
        user_code = cleaned_data.get('user_code')
        recipient_code = cleaned_data.get('recipient_code')
        if Room.objects.filter(user_code=user_code, recipient_code=recipient_code).exists():
            raise forms.ValidationError('既に同じ参加者とのルームが作成されています')
        if Room.objects.filter(user_code=recipient_code, recipient_code=user_code).exists():
            raise forms.ValidationError('既に同じ参加者とのルームが作成されています')
        return cleaned_data   
    
class AddMessageForm(forms.ModelForm):
    
    message = forms.CharField(label='メッセージ', widget=forms.Textarea(attrs={'rows': 2, 'cols': 120}))
    
    class Meta:
        model = Message
        fields = ('message', )
        
class DeleteRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = []