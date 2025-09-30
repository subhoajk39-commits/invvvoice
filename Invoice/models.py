# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Name:         models.py
# Purpose:      Defines the database models for the Invoice application.
#
# Author:       AnikRoy
# GitHub:       https://github.com/aroyslipk
#
# Created:      2025-06-20
# Copyright:    (c) AnikRoy 2025
# Licence:      Proprietary
# -----------------------------------------------------------------------------

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings


class User(AbstractUser):
    ROLE_CHOICES = (
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    created_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_users'
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def is_admin(self):
        return self.role == 'admin' or self.role == 'super_admin'

class ClientProject(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    attachment = models.FileField(upload_to='project_attachments/', null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='projects_created', on_delete=models.CASCADE)
    managed_by = models.ForeignKey(User, related_name='managed_projects', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'USD $'),
        ('EUR', 'EUR €'),
        ('GBP', 'GBP £'),
        ('AUD', 'AUD $')
    ]

    project = models.ForeignKey(
        'ClientProject', 
        on_delete=models.CASCADE, 
        related_name='categories'
    )
    
    name = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=10, decimal_places=2)

    currency = models.CharField(
        max_length=3, 
        choices=CURRENCY_CHOICES, 
        default='USD',
        help_text="Currency for the rate"
    )

    managed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('project', 'name')

    def __str__(self):
        return self.name

class WorkEntry(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    project = models.ForeignKey(
        'ClientProject', 
        on_delete=models.CASCADE, 
        related_name='work_entries'
    )
    folder_name = models.CharField(max_length=100)
    folder_name = models.CharField(max_length=100, verbose_name="Folder Name")
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(default=timezone.now)
    is_slot = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.folder_name}"
    
class UserLoginHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_history')
    login_datetime = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    device_type = models.CharField(max_length=50)
    browser = models.CharField(max_length=50)
    os = models.CharField(max_length=50)

    class Meta:
        ordering = ['-login_datetime']

    def __str__(self):
        return f"{self.user.username} - {self.login_datetime}"

class Invoice(models.Model):
    project = models.ForeignKey(ClientProject, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')

    project_name_snapshot = models.CharField(max_length=255, help_text="Project name at the time of invoice generation")
    
    invoice_file = models.FileField(upload_to='invoices/')
    generated_at = models.DateTimeField(auto_now_add=True)
    
    month = models.IntegerField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    invoice_file = models.FileField(upload_to='invoices/')
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice for {self.project_name_snapshot} ({self.generated_at.strftime('%b %Y')}) - Amount: ${self.total_amount}"