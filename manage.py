#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Name:         manage.py
# Purpose:      Django's command-line utility for administrative tasks.
#
# Author:       AnikRoy
# GitHub:       https://github.com/aroyslipk
#
# Created:      2025-06-20
# Copyright:    (c) AnikRoy 2025
# Licence:      Proprietary
# -----------------------------------------------------------------------------

"""
Django's command-line utility for administrative tasks.
This script serves as the entry point for running management commands
such as 'runserver', 'migrate', 'makemigrations', 'shell', etc.
"""

import os
import sys

def main():
    """Runs administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Invoice_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()