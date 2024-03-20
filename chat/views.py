from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Room, Message
from .forms import RoomForm, AddRoomForm, AddMessageForm, DeleteRoomForm
from django.urls import reverse_lazy
from accounts.models import InstitutionCode, User
from datetime import datetime
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin 

    
    
class AddRoomView(LoginRequiredMixin, CreateView):
    template_name = 'chat/add_chat_room.html'
    success_url = reverse_lazy('chat:chat_room')
    form_class = AddRoomForm

    def form_valid(self, form):
        room_data = form.save(commit=False)
        self_code = self.request.user.institution_name #type:ignore エラー問題無
        form.instance.user_code = self.request.user
        form.instance.user_id = self.request.user
        room_data.save()
        return super().form_valid(form)    

    def get_initial(self):
        initial = super().get_initial()
        initial['user_code'] = self.request.user
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['name'].label = 'ルーム名'
        form.fields['user_code'].label = '作成者'
        form.fields['recipient_code'].label = 'どの薬局・病院とチャットを始めますか'

        code = self.request.user.institution_code.code #type:ignore
        print(code)
        if code == 'P':
               form.fields['recipient_code'].queryset = User.objects.filter(institution_code__code='C') 
        else:
               form.fields['recipient_code'].queryset = User.objects.filter(institution_code__code='P') 
        
        return form 
    
    
    
class ListRoomView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'chat/list_chat_room.html'

    def get_queryset(self):
        filter_code = self.request.user
        print(filter_code)
        queryset = super().get_queryset()
        queryset = queryset.filter(user_code=filter_code) | queryset.filter(recipient_code=filter_code)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_code'] = self.request.user.institution_name #type:ignore
        return context
    

def AddMessageView(request, id):

    message_form = AddMessageForm(request.POST or None)
    room = get_object_or_404(Room, id=id)
    list_message = Message.objects.filter(room_id=id)
    show_delete_link = request.user == room.user_id
    
    if message_form.is_valid():
        message_form.instance.room = room
        message_form.instance.sender = request.user
        message_form.instance.create_at = datetime.now()
        message_form.save()
        return redirect('chat:add_message', id=id)
    return render(
        request, 'chat/add_chat_message.html', context={
            'message_form': message_form,
            'room': room,
            'list_message': list_message,
            'show_delete_link': show_delete_link
        }
    ) 
 

class DeleteRoomView(LoginRequiredMixin, DeleteView):
    template_name = 'chat/delete_confirm_chat_room.html'
    model = Room
    success_url = reverse_lazy('chat:chat_room')
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.user_id != self.request.user:
            raise Http404("ルームの削除はルーム作成者のみ可能です。")
        return obj