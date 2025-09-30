# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Name:         api_urls.py
# Purpose:      URL routing for the API endpoints of the Invoice application.
#
# Author:       AnikRoy
# GitHub:       https://github.com/aroyslipk
#
# Created:      2025-06-20
# Copyright:    (c) AnikRoy 2025
# Licence:      Proprietary
# -----------------------------------------------------------------------------


from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    RegisterView,
    ProfileView,
    WorkEntryListCreateView,
    DashboardView,
    PriceListCreateView,
    PriceDetailView,
    ClientProjectListCreateView,
    ExportWorkEntriesXLSXView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register_api'),
    path('profile/', ProfileView.as_view(), name='profile_api'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('work-entries/', WorkEntryListCreateView.as_view(), name='work_entry_api'),
    path('dashboard/', DashboardView.as_view(), name='dashboard_api'),
    path('prices/', PriceListCreateView.as_view(), name='price_list_create_api'),
    path('prices/<int:id>/', PriceDetailView.as_view(), name='price_detail_api'),
    path('projects/', ClientProjectListCreateView.as_view(), name='client_projects_api'),
    path('export/xlsx/', ExportWorkEntriesXLSXView.as_view(), name='export_xlsx_api'),
]