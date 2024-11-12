from django.contrib import admin
from .models import Post, Reaction, Report, Block

# 어드민에 등록
admin.site.register(Post)
admin.site.register(Reaction)
admin.site.register(Report)
admin.site.register(Block)