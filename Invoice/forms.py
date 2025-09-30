# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Name:         urls.py (App Level)
# Purpose:      URL routing for the Invoice application's web pages.
#
# Author:       AnikRoy
# GitHub:       https://github.com/aroyslipk
#
# Created:      2025-06-20
# Copyright:    (c) AnikRoy 2025
# Licence:      Proprietary
# -----------------------------------------------------------------------------


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, WorkEntry, ClientProject, Category

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name', 'rate', 'currency']
       
class WorkEntryForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        label="Category",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = WorkEntry
        fields = ['project', 'folder_name', 'category', 'quantity', 'date']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-select'}),
            'folder_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter folder or file name'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        admin_manager = kwargs.pop('admin_manager', None)
        super().__init__(*args, **kwargs)
        
        if admin_manager:
            self.fields['project'].queryset = ClientProject.objects.filter(managed_by=admin_manager)
            self.fields['category'].queryset = Category.objects.filter(managed_by=admin_manager)
        else:
            self.fields['project'].queryset = ClientProject.objects.none()
            self.fields['category'].queryset = Category.objects.none()

class AdminUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'role')

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
        # Only show role field to super admins
        if not user or user.role != 'super_admin':
            del self.fields['role']

class ClientProjectForm(forms.ModelForm):
    class Meta:
        model = ClientProject
        fields = ['name', 'start_date', 'end_date', 'attachment']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
        }

class AdminSlotForm(forms.Form):

    slot_count = forms.IntegerField(
        min_value=1,
        label="",
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': '# of Slots'})
    )

class UserRoleUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['role']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'})
        }