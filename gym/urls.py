from django.urls import path
from . import views

urlpatterns = [
    # Основные
    path('', views.dashboard, name='dashboard'),
    
    # Клиенты
    path('clients/', views.client_list, name='client_list'),
    path('clients/create/', views.client_create, name='client_create'),
    path('clients/<int:pk>/', views.client_detail, name='client_detail'),
    path('clients/<int:pk>/edit/', views.client_edit, name='client_edit'),
    path('clients/<int:pk>/delete/', views.client_delete, name='client_delete'),
    
    # Абонементы
    path('subscriptions/', views.subscription_list, name='subscription_list'),
    path('subscriptions/create/', views.subscription_create, name='subscription_create'),
    path('subscriptions/<int:pk>/', views.subscription_detail, name='subscription_detail'),
    
    # Посещения
    path('visits/create/', views.visit_create, name='visit_create'),
    path('visits/<int:pk>/checkout/', views.visit_checkout, name='visit_checkout'),
    
    # Сотрудники (только для админов)
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/create/', views.employee_create, name='employee_create'),
    
    # Экспорт
    path('export/excel/', views.export_excel, name='export_excel'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),
    
    # Статистика
    path('admin/stats/', views.admin_stats, name='admin_stats'),
]