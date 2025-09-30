# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Name:         apps.py
# Purpose:      Declares the application configuration for the Invoice app.
#
# Author:       AnikRoy
# GitHub:       https://github.com/aroyslipk
#
# Created:      2025-06-20
# Copyright:    (c) AnikRoy 2025
# Licence:      Proprietary
# -----------------------------------------------------------------------------


from django.apps import AppConfig

class InvoiceConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Invoice'