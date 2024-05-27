from django.contrib import admin
from join.models import Board
from join.models import Task

class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at')
    filter_horizontal = ('users',)  # Stellt sicher, dass Benutzer als Auswahlfelder erscheinen

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'priority', 'created_at', 'board')
    filter_horizontal = ('users',)  # Stellt sicher, dass Benutzer als Auswahlfelder erscheinen


admin.site.register(Board, BoardAdmin)
admin.site.register(Task, TaskAdmin)

