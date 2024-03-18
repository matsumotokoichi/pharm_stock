from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, View, ListView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import CustomUserCreationForm, UserLoginForm, UserChangeForm, ChangePasswordForm 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.views.generic import UpdateView
from django.contrib import messages
from .models import User
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from datetime import datetime

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'
    
    
    def get_template_names(self):
        code = self.request.user.institution_code.code
        if code.startswith('P'):
            template_name = 'home_test.html'
        else :
            template_name = 'home_test2.html'
            
        return [template_name]
    


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:signup_success')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['username'].label = 'ユーザー名'
        form.fields['institution_name'].label = '所属機関名'
        form.fields['email'].label = 'メールアドレス'
        form.fields['institution_code'].label = '病院や薬局か選択してください'
        return form
    
    def form_valid(self, form):
        user = form.save()
        self.object = user
        
        return super().form_valid(form)
    
    
class SignUpSuccessView(TemplateView):
    template_name = 'accounts/signup_success.html'
    
    
class TopView(TemplateView):
    template_name = 'top.html'
    
    
def logout_view(request):
    logout(request)
    return redirect('top')

#ユーザー情報ページ
class UserProfileView(TemplateView):
    template_name = 'accounts/user_profile.html'
    

class UserChangeView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'accounts/user_change.html'
    form_class = UserChangeForm
    success_url = reverse_lazy('accounts:user_profile')

    def get_object(self, queryset=None):
        obj = get_object_or_404(User, pk=self.kwargs['pk'])
        if obj.pk != self.request.user.pk:
            raise PermissionDenied
        return obj

    def form_valid(self, form):
        user_data = form.save(commit=False)
        # stock_data.institution_code_fk = self.request.user.institution_code #type:ignore エラー問題無
        user_data.user = self.request.user
        form.instance.create_at = datetime.now()
        form.instance.update_at = datetime.now()
        user_data.save()
        return super().form_valid(form)        



class UserChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    """パスワード変更ビュー"""
    success_url = reverse_lazy('accounts:user_change_password_done')
    template_name = 'accounts/user_change_password.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        context["form_name"] = "password_change"
        return context
    
class UserPasswordChangeDoneView(LoginRequiredMixin,PasswordChangeDoneView):
    """パスワード変更完了"""
    template_name = 'accounts/user_change_password_done.html'
