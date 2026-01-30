from django.contrib import admin
from .models import Student, TrainingTime, TrainingTopic, Training, TrainingReq, TrainingPlace
from django.utils.html import format_html


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


class TrainingInline(admin.TabularInline):
    model = Training.participants.through
    can_delete = False
    verbose_name = "Тренировка"
    verbose_name_plural = "Тренировки"

    readonly_fields = ("training", "training_date", "training_final_topic")
    fields = ("training", "training_date", "training_final_topic")

    @admin.display(description="Дата")
    def training_date(self, obj):
        return obj.training.date
    
    @admin.display(description="Тема")
    def training_final_topic(self, obj):
        return obj.training.final_topic

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    inlines = [TrainingInline, TrainingReqInline]

@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "status")
    inlines = [TrainingReqInline]
    readonly_fields = ("participants", "final_time", "final_topic")
    list_filter = ["status", "date", "place","final_topic","participants"]

@admin.register(TrainingPlace)
class TrainingAdmin(admin.ModelAdmin):
    readonly_fields = ("open_in_maps",)

    def open_in_maps(self, obj):
        return format_html(
            '<a class="button" href="{}" target="_blank">Открыть на карте</a>',
            obj.yandex_maps_url()
        )

    open_in_maps.short_description = "Карта"