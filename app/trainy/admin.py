from django.contrib import admin
from .models import Student, TrainingTime, TrainingTopic, Training, TrainingReq
from django.utils.html import format_html


admin.site.register(Student)
admin.site.register(TrainingTime)
admin.site.register(TrainingTopic)


@admin.register(TrainingReq)
class TrainingReqAdmin(admin.ModelAdmin):
    list_display = ("student", "training", "created_at")
    readonly_fields = ("created_at", "student", "training", "training_times", "topics")
    filter_horizontal = ("training_times", "topics")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class TrainingReqInline(admin.TabularInline):
    model = TrainingReq
    readonly_fields = ("student", "training", "training_times", "topics", "created_at")

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "status")
    inlines = [TrainingReqInline]
    readonly_fields = ("participants", "final_time", "final_topic")
