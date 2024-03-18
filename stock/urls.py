from django.urls import path
from . import views

app_name = 'stock'

urlpatterns = [
    path('list_stock/', views.ListStockView.as_view(), name='list_stock'),
    path('add_stock/', views.AddStockView.as_view(), name='add_stock'),    
    path('update_stock/<int:pk>', views.UpdateStockView.as_view(), name='update_stock'),
    path('detail_stock/<int:pk>', views.DetailStockview.as_view(), name='detail_stock'),
    path('delete_stock/<int:pk>', views.DeleteStockView.as_view(), name='delete_stock')

]
