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

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, WorkEntry, ClientProject, Category

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password'] 

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role='user'
        )
        return user

class WorkEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkEntry
        fields = ['id', 'user', 'project', 'category', 'quantity', 'date']
        read_only_fields = ['user']

class WorkDashboardSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = WorkEntry
        fields = ['id', 'username', 'project_name', 'category', 'quantity', 'date']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'rate', 'managed_by']
        read_only_fields = ['managed_by']

class ClientProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProject
        fields = ['id', 'name', 'start_date', 'end_date', 'attachment', 'created_by', 'managed_by']
        read_only_fields = ['created_by', 'managed_by']