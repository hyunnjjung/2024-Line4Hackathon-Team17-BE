from django.contrib import admin
from .models import User, Interest

# 어드민에 등록
admin.site.register(User)
admin.site.register(Interest)