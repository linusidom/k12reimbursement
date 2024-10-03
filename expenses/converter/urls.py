from django.urls import path, re_path
from converter import views

app_name = 'firstapp'

urlpatterns = [
    
    path('reimburse', views.ReimburseView.as_view(), name='reimburse'),
    path('mileage', views.MileageView.as_view(), name='mileage'),
    path('reimburse_create', views.reimburse_create, name='reimburse_create'),
    path('mileage_create', views.mileage_create, name='mileage_create'),

    path('reimburse_error', views.ReimburseErrorView.as_view(), name='reimburse_error'),
    path('mileage_error', views.MileageErrorView.as_view(), name='mileage_error'),

    path('reimburse_delete/<int:pk>', views.ReimburseDeleteView.as_view(), name='reimburse_delete'),
    path('mileage_delete/<int:pk>', views.MileageDeleteView.as_view(), name='mileage_delete'),
]