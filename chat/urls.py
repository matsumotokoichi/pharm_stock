from django.urls import path
from chat import views

app_name = 'chat'

urlpatterns = [
    path('chat_room/', views.ListRoomView.as_view(), name="chat_room"),  
    path('add_chat_room/', views.AddRoomView.as_view(), name="add_chat_room"),
    path('chat_room/<int:id>', views.AddMessageView, name='add_message'),
    path('delete_chat_room/<int:pk>', views.DeleteRoomView.as_view(), name='delete_chat_room')
]