from django.contrib.auth.forms import UserCreationForm
from . import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django import forms
from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm

class CustomUserCreationForm(UserCreationForm):

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if models.User.objects.filter(email=email).exists():
            raise ValidationError(_("このメールアドレスは既に登録されています。"))
        return email
    
    def save(self, *args, **kwargs):
        obj = super(CustomUserCreationForm, self).save(commit=False)
        obj.update_at = datetime.now()
        obj.create_at = datetime.now()
        obj.save()
        return obj

    class Meta:
        model = models.User
        fields = ['username', 'email',  'institution_code', 'institution_name']
    
        
class UserLoginForm(AuthenticationForm):
    email = forms.EmailField(label='ログインID(メールアドレス)')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    
    
#ユーザー情報編集
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# class UserChangeForm(forms.ModelForm):
    
#     class Meta:
#         model = models.User
#         fields = [ 'email', 'institution_name']
        
#     def __init__(self, username=None, institution_code=None, email=None,
#                  institution_name=None, *args, **kwargs):
#         kwargs.setdefault('label_suffix', '')
#         self.request = kwargs.pop('request', None)
#         super().__init__(*args, **kwargs)
#         if self.request:
#             # ユーザーの更新前情報をフォームに挿入
#             self.fields['email'].initial = self.request.user.email
#             self.fields['institution_name'].initial = self.request.user.institution_name


#     def update(self, user):
#         user.email = self.cleaned_data['email']
#         user.institution_code = user.institution_code
#         user.update_at = datetime.now()
#         user.create_at = user.create_at 
#         # バリデーションを一時的に無効化して保存
#         user._disable_validation = True
#         try:
#             user.save()
#         finally:
#             del user._disable_validation
            
#     def clean(self):
#         if hasattr(self.instance, '_disable_validation'):
#             return
#         cleaned_data = super().clean()
#         email = cleaned_data.get('email')
#         if email and models.User.objects.filter(email=email).exclude(pk=self.request.user.pk).exists():
#             raise ValidationError({'email': _('This email address is already in use.')})
#         return cleaned_data



class UserChangeForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['username', 'email', 'institution_name']

    def clean_email(self):
        email = self.cleaned_data['email']
        if models.User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('このメールアドレスは既に使用されています')
        return email



from django.contrib.auth import authenticate, get_user_model
 
# User = get_user_model()
 
class ChangePasswordForm(forms.Form):
    
    class Meta:
        model = models.User
        
    """パスワード変更"""
    current_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
    )
    new_password = forms.CharField(
        required=True,
        min_length=8,
        widget=forms.PasswordInput(),
    )
    confirm_new_password = forms.CharField(
        required=True,
        min_length=8,
        widget=forms.PasswordInput(),
    )
    def __init__(self, user_id, *args, **kwargs):
        self.user_id = user_id
        super().__init__(*args, **kwargs)
 
    def clean_current_password(self):
        current_password = self.cleaned_data['current_password']
        user = models.User.objects.get(pk=self.user_id)
        if user.username and current_password:
            auth_result = authenticate(
                username = user.username,
                password=current_password,
            )
            if not auth_result:
                raise ValidationError('現在のパスワードが間違っています。')
        return current_password
 
    def clean_new_password(self):
        new_password = self.cleaned_data['new_password']
        return new_password
 
    def clean_confirm_new_password(self):
        confirm_new_password = self.cleaned_data['confirm_new_password']
        return confirm_new_password
 
    def clean(self):
        cleaned_data = super().clean()
        new_password = self.cleaned_data.get('new_password')
        confirm_new_password = self.cleaned_data.get('confirm_new_password')
        if new_password != confirm_new_password:
            self.add_error(
                field='confirm_new_password',
                error=ValidationError('パスワードが一致しません。'))
        return cleaned_data