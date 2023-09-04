from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.apps import apps

for model in apps.get_app_config('app').get_models():
    admin.site.register(model)
