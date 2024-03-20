from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Medicine, User
from datetime import datetime
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from .forms import UpdateStockForm, MedicineFilterForm
from django.contrib.auth.mixins import LoginRequiredMixin 

class AddStockView(LoginRequiredMixin, CreateView):
    fields = ('name', 'stock', 'category', 'memo')
    template_name = 'stock/add_stock.html'
    model = Medicine
    success_url = reverse_lazy('stock:list_stock')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['name'].label = '医薬品名(先発名で記載推奨)'
        form.fields['stock'].label = '在庫数'
        form.fields['category'].label = '医薬品分類名'
        form.fields['memo'].label = 'メモ'
        return form 

    def form_valid(self, form):
        stock_data = form.save(commit=False)
        stock_data.institution_code_fk = self.request.user.institution_code #type:ignore エラー問題無
        stock_data.user = self.request.user
        form.instance.create_at = datetime.now()
        form.instance.update_at = datetime.now()
        stock_data.save()
        return super().form_valid(form)        
    
class ListStockView(LoginRequiredMixin, ListView):
    template_name = 'home.html'
    model = Medicine
    form_class = MedicineFilterForm
    
    def get_template_names(self):
        code = self.request.user.institution_code.code #type:ignore

        if code == 'P':
            template_name = 'stock/p_list_stock.html'
        else :
            template_name = 'stock/c_list_stock.html'
                        
        return [template_name]

    def get_queryset(self):
        queryset = super().get_queryset()
        request_user = self.request.GET.get('institution_name')  
        self_code = self.request.user.institution_name #type:ignore
        
        #病院側→institution_codeを選択できる、薬局→自身のinstitution_codeに該当するlistしか表示しない
        if request_user:
            queryset = queryset.filter(user_id=request_user)
        elif not request_user:
            queryset = queryset.filter(user_id=self.request.user)
            
        #名前で絞り込み
        medicine_name = self.request.GET.get('medicine_name', None)
        if medicine_name:
            queryset = queryset.filter(name__icontains=medicine_name)
        
        #分類検索
        category_name = self.request.GET.get('category_name', None)
        if category_name == '1' :
            queryset = queryset.filter(category=category_name)
        if category_name == '2' :
            queryset = queryset.filter(category=category_name)
        if category_name == '3' :
            queryset = queryset.filter(category=category_name)
        if category_name == '4' :
            queryset = queryset.filter(category=category_name)
        if category_name == '5' :
            queryset = queryset.filter(category=category_name)

                        
        return queryset.order_by('category', 'name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = MedicineFilterForm(self.request.GET)
        context['medicine_name'] = self.request.GET.get('medicine_name', '')
        category_name = self.request.GET.get('category_name', 0)
        if category_name == '1':
            context['category_name'] = True
        elif category_name == '2':
            context['category_name'] = True        

        return context
    

class DetailStockview(LoginRequiredMixin, DetailView):
    model = Medicine
    template_name = 'stock/detail_stock.html'    
    
    def get_object(self, queryset=None):
        return Medicine.objects.get(pk=self.kwargs['pk'])


class UpdateStockView(LoginRequiredMixin, UpdateView):
    template_name = 'stock/update_stock.html'
    form_class = UpdateStockForm
    success_url = reverse_lazy('stock:list_stock')
    
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['medicine'] = Medicine.objects.get(pk=self.kwargs['pk'])
        return context
    
    def get_initial(self, **kwargs):
        initial = super(UpdateStockView, self).get_initial(**kwargs)
        medicine = Medicine.objects.get(pk=self.kwargs['pk'])
        initial['name'] = medicine.name
        initial['stock'] = medicine.stock
        initial['category'] = medicine.category
        initial['memo'] = medicine.memo
        return initial
    
    def form_valid(self, form):
        stock_data = form.save(commit=False)
        original_create_at = stock_data.create_at
        form.instance.create_at = original_create_at
        form.instance.update_at = datetime.now()       
        stock_data.save()
        return super().form_valid(form)     


    def get_object(self, queryset=None):
        obj = get_object_or_404(Medicine, pk=self.kwargs['pk'])
        if obj.user != self.request.user:
            raise PermissionDenied
        return obj
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['name'].label = '医薬品名'
        form.fields['stock'].label = '在庫数'
        form.fields['category'].label = '分類'
        form.fields['memo'].label = 'メモ'
        return form 
 


class DeleteStockView(LoginRequiredMixin, DeleteView):
    template_name = 'stock/delete_confirm_stock.html'
    model = Medicine
    success_url = reverse_lazy('stock:list_stock')
