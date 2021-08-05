from django.contrib import admin
from .models import Dashboard, Sprint, Task, Comment


admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(Dashboard)
admin.site.register(Sprint)
