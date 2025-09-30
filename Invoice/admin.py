# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Name:         admin.py
# Purpose:      Django Admin configurations for the Invoice app.
#
# Author:       AnikRoy
# GitHub:       https://github.com/aroyslipk
#
# Created:      2025-06-20
# Copyright:    (c) AnikRoy 2025
# Licence:      Proprietary
# -----------------------------------------------------------------------------


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, WorkEntry, ClientProject, Category

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'created_by', 'is_staff')
    list_filter = ('role',)
    fieldsets = UserAdmin.fieldsets + (
        ('Role & Ownership', {'fields': ('role', 'created_by')}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)

    def save_model(self, request, obj, form, change):
        if not change and not request.user.is_superuser:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser and obj:
            return ('username', 'role', 'created_by', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        return ()

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return True 
        return obj.created_by == request.user

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)


@admin.register(ClientProject)
class ClientProjectAdmin(admin.ModelAdmin):
    """Admin configuration for the ClientProject model."""
    list_display = ('name', 'managed_by')
    list_filter = ('managed_by',)
    search_fields = ('name',)

    def save_model(self, request, obj, form, change):
        if not obj.managed_by_id:
            obj.managed_by = request.user
        if not getattr(obj, 'created_by_id', None):
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.role == 'super_admin':
            return qs
        return qs.filter(managed_by=request.user)

@admin.register(WorkEntry)
class WorkEntryAdmin(admin.ModelAdmin):
    """Admin configuration for the WorkEntry model."""
    list_display = ('user', 'project', 'get_folder_name', 'quantity', 'date')
    list_filter = ('date', 'project')
    search_fields = ('user__username', 'project__name', 'category')

    @admin.display(description="Folder Name")
    def get_folder_name(self, obj):
        return obj.category
    list_display = ('user', 'project', 'folder_name', 'get_category', 'quantity', 'date')
    list_filter = ('date', 'project')
    search_fields = ('user__username', 'project__name', 'folder_name', 'category__name')

    @admin.display(description="Rate Category")
    def get_category(self, obj):
        return obj.category.name if obj.category else "N/A"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.role == 'super_admin':
            return qs
        if request.user.role == 'admin':
            return qs.filter(project__managed_by=request.user)
        return qs.filter(user=request.user)
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'rate', 'managed_by')
    list_filter = ('managed_by',)
    search_fields = ('name',)