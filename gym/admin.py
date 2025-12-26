from django.contrib import admin
from .models import UserProfile, Client, Subscription, Visit, WriteOff, Reminder

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone', 'created_at']
    list_filter = ['role']
    search_fields = ['user__username']

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'phone', 'email', 'created_by', 'created_at']
    search_fields = ['first_name', 'last_name', 'phone']
    list_filter = ['created_at']

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['client', 'subscription_type', 'visits_left', 'start_date', 'end_date', 'status']
    list_filter = ['status', 'subscription_type', 'end_date']
    search_fields = ['client__first_name', 'client__last_name']

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ['client', 'check_in', 'check_out', 'created_by']
    list_filter = ['check_in', 'created_by']
    search_fields = ['client__first_name', 'client__last_name']

@admin.register(WriteOff)
class WriteOffAdmin(admin.ModelAdmin):
    list_display = ['subscription', 'writeoff_type', 'amount', 'created_by', 'created_at']
    list_filter = ['writeoff_type', 'created_at']

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ['subscription', 'reminder_type', 'sent_at', 'status']
    list_filter = ['reminder_type', 'status']