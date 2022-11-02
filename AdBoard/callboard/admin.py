from django.contrib import admin
from .models import Announcement, Category, Respond

admin.site.register(Announcement)
admin.site.register(Category)
admin.site.register(Respond)