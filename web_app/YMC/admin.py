from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Blog,Comment


admin.site_header="YMC Admin"
admin.site_title="YMC Admin Portal"
admin.index_title="Well come to YMC Admin Portal"
admin.site.register(Blog)
admin.site.register(Comment)
