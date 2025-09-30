# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------- 
# Name:         urls.py (App Level)
# Purpose:      URL routing for the Invoice application's web pages.
# Author:       AnikRoy
# GitHub:       https://github.com/aroyslipk
# Created:      2025-06-20
# Copyright:    (c) AnikRoy 2025
# Licence:      Proprietary
# -----------------------------------------------------------------------------

from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    get_user_work_summary,
    home_view,
    CustomLoginView,
    CustomLogoutView,
    work_entry_form_view,
    get_user_login_history,
    my_work_entries_view,
    dashboard_template_view,
    admin_panel_view,
    my_team_view,
    delete_user_view,
    manage_projects_view,
    set_price_view,
    delete_project_view,
    manage_prices_view,
    price_edit_view,
    delete_price_view,
    export_page_view,
    generate_invoice,
    reports_view,
    invoice_reports_view,
    create_slots_view,
    submit_work_view,
    save_all_prices_view,
    delete_work_entry_view,
    delete_invoice_view,
    load_categories_view,
    edit_user_role_view,
    bulk_download_invoices_view,
    bulk_delete_invoices_view,
    user_reports_view,
    get_user_report_view,
    export_user_report_view
)
from .bank_invoice import generate_bank_invoice

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),  # Use your custom logout
    path('submit-work/', submit_work_view, name='submit_work'),
    path('my-work/', my_work_entries_view, name='my_work_entries'),
    path('dashboard/', dashboard_template_view, name='dashboard'),
    path('admin-panel/', admin_panel_view, name='admin_panel'),
    path('my-team/', my_team_view, name='my_team'),
    path('delete-user/<uuid:user_id>/', delete_user_view, name='delete_user'),
    path('edit-user-role/<uuid:user_id>/', edit_user_role_view, name='edit_user_role'),
    path('manage/projects/', manage_projects_view, name='manage_projects'),
    path('set-price/<int:entry_id>/', set_price_view, name='set_price'),
    path('manage/projects/delete/<int:project_id>/', delete_project_view, name='delete_project'),
    path('manage/projects/delete-entry/<int:entry_id>/', delete_work_entry_view, name='delete_work_entry'),
    path('save-all-prices/<int:project_id>/', save_all_prices_view, name='save_all_prices'),
    path('manage/prices/<int:project_id>/', manage_prices_view, name='manage_prices'),
    path('manage/prices/<int:id>/edit/', price_edit_view, name='price_edit'),
    path('manage/prices/delete/<int:id>/', delete_price_view, name='delete_price'),
    path('get-login-history/<uuid:user_id>/', get_user_login_history, name='get_login_history'),
    path('export-page/', export_page_view, name='export_page'),
    path('invoice/generate/', generate_invoice, name='generate_invoice'),
    path('reports/', reports_view, name='reports'),
    path('invoice-reports/', invoice_reports_view, name='invoice_reports'),
    path('invoice/delete/<int:invoice_id>/', delete_invoice_view, name='delete_invoice'),
    path('create-slots/', create_slots_view, name='create_slots'),
    path('ajax/load-categories/', load_categories_view, name='ajax_load_categories'),
    path('invoice/generate-bank/', generate_bank_invoice, name='generate_bank_invoice'),
    path('api/user-work-summary/', get_user_work_summary, name='get_user_work_summary'),
    path('bulk-download-invoices/', bulk_download_invoices_view, name='bulk_download_invoices'),
    path('bulk-delete-invoices/', bulk_delete_invoices_view, name='bulk_delete_invoices'),
    path('user-reports/', user_reports_view, name='user_reports'),
    path('get-user-report/<uuid:user_id>/', get_user_report_view, name='get_user_report'),
    path('export-user-report/<uuid:user_id>/<str:format>/', export_user_report_view, name='export_user_report'),
]
