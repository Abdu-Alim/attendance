from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime, timedelta

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('employee', 'Сотрудник'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
    
    def is_admin(self):
        return self.role == 'admin'

class Client(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(blank=True, verbose_name="Email")
    notes = models.TextField(blank=True, verbose_name="Заметки")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='clients')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    
    def full_name(self):
        return f"{self.last_name} {self.first_name}"

class Subscription(models.Model):
    TYPE_CHOICES = [
        ('visits', 'По посещениям'),
        ('month', 'На месяц'),
        ('unlimited', 'Безлимит'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Активен'),
        ('paused', 'Приостановлен'),
        ('expired', 'Истек'),
        ('cancelled', 'Отменен'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='subscriptions', verbose_name="Клиент")
    subscription_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='visits', verbose_name="Тип абонемента")
    visits_total = models.IntegerField(default=10, verbose_name="Всего посещений")
    visits_left = models.IntegerField(default=10, verbose_name="Осталось посещений")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Стоимость")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Статус")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='subscriptions_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.client} - {self.get_subscription_type_display()} ({self.status})"
    
    def days_left(self):
        from datetime import date
        if self.end_date:
            delta = self.end_date - date.today()
            return delta.days
        return 0
    
    def is_expiring_soon(self):
        days = self.days_left()
        return 0 <= days <= 7

class Visit(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='visits', verbose_name="Клиент")
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True, related_name='visits', verbose_name="Абонемент")
    check_in = models.DateTimeField(verbose_name="Время входа", auto_now_add=True)
    check_out = models.DateTimeField(null=True, blank=True, verbose_name="Время выхода")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='visits_created')
    
    class Meta:
        ordering = ['-check_in']
    
    def __str__(self):
        return f"{self.client} - {self.check_in.strftime('%Y-%m-%d %H:%M')}"
    
    def duration(self):
        if self.check_out:
            delta = self.check_out - self.check_in
            hours = delta.seconds // 3600
            minutes = (delta.seconds % 3600) // 60
            return f"{hours}ч {minutes}м"
        return "В зале"

class WriteOff(models.Model):
    TYPE_CHOICES = [
        ('auto', 'Автоматическое списание'),
        ('manual', 'Ручное списание'),
        ('correction', 'Коррекция'),
        ('addition', 'Добавление'),
    ]
    
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='writeoffs', verbose_name="Абонемент")
    visit = models.ForeignKey(Visit, on_delete=models.SET_NULL, null=True, blank=True, related_name='writeoffs', verbose_name="Посещение")
    writeoff_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='auto', verbose_name="Тип списания")
    amount = models.IntegerField(default=1, verbose_name="Количество")
    notes = models.TextField(blank=True, verbose_name="Примечание")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subscription.client} - {self.amount} посещений ({self.get_writeoff_type_display()})"

class Reminder(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='reminders', verbose_name="Абонемент")
    reminder_type = models.CharField(max_length=20, choices=[
        ('7_days', 'За 7 дней'),
        ('3_days', 'За 3 дня'),
        ('1_day', 'За 1 день'),
        ('expired', 'Просрочен'),
        ('manual', 'Вручную'),
    ])
    sent_at = models.DateTimeField(auto_now_add=True)
    sent_to = models.EmailField(blank=True)
    status = models.CharField(max_length=20, default='sent')
    
    class Meta:
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"Напоминание для {self.subscription.client}"