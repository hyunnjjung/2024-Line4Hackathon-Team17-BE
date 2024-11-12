from django.contrib import admin
from .models import Category, PatingReport, PatingBlock, PatingParticipation, PatingPost

# 어드민에 등록
admin.site.register(PatingPost)
admin.site.register(PatingParticipation)
admin.site.register(PatingReport)
admin.site.register(PatingBlock)
admin.site.register(Category)