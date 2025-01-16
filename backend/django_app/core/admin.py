from django.contrib import admin
from .models import Equipment, ProcessStep, Analysis


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("name", "cost", "efficiency", "processing_capacity")
    search_fields = ("name", "description")


@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ("name", "process_type", "order", "equipment")
    list_filter = ("process_type",)
    search_fields = ("name", "equipment__name")


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ("process_type", "user", "created_at", "protein_yield", "npv")
    list_filter = ("process_type", "user")
    date_hierarchy = "created_at"
