#!/usr/bin/env python
import os
import sys
from django.core.management.commands.runserver import Command as Runserver

if __name__ == '__main__':
    Runserver.default_addr = '0.0.0.0'  # 修改默认地址
    Runserver.default_port = '80'  # 修改默认端口
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videoproject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
