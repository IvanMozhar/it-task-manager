from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from task_manager.models import Worker, TaskType, Task, Position, Tag


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "position",
                    )
                },
            ),
        )
    )


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ("name", )


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ("name", )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ("name", )
