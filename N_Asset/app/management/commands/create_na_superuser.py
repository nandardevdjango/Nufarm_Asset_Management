import re
import getpass
from django.db import transaction
from django.core.management.base import BaseCommand
from NA_Models.models import NAPrivilege, NASysPrivilege


class Command(BaseCommand):

    def handle(self, *args, **options):
        email = input('Email: ')
        email_exists = NAPrivilege.objects.filter(email=email).exists()
        patterns_email = r'[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}'
        while email_exists:
            print('\t User with this Email has exists')
            email = input('Email: ')

        while not re.match(patterns_email, email):
            print('\t Please enter correct email address')
            email = input('Email: ')

        username = input('Username: ')
        username_exists = NAPrivilege.objects.filter(username=username).exists()
        while username_exists:
            print('\t User with this Username has exists')
            username = input('Username: ')

        password = getpass.getpass(prompt='Password: ')
        confirm_password = getpass.getpass(prompt='Confirm Password: ')
        while password != confirm_password:
            print('Password didn\'t match')
            password = getpass.getpass(prompt='Password: ')
            confirm_password = getpass.getpass(prompt='Confirm Password: ')

        with transaction.atomic():
            user = NAPrivilege()
            user.email = email
            user.username = username
            user.set_password(password)
            user.role = NAPrivilege.SUPER_USER
            user.divisi = NAPrivilege.IT
            user.is_superuser = True
            user.is_staff = True
            user.save()
            NASysPrivilege.set_permission(user)
        return 'NA Super User Created Successfully'
