from django.contrib import admin

from .models import Exercise, ExerciseType, Set, Workout, WorkoutEvent


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    search_fields = ("user__email", "slug")
    date_hierarchy = "date_started"
    list_display = ("slug", "user", "status", "date_started", "date_ended", "is_active")


@admin.register(ExerciseType)
class ExerciseTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name", "is_active")


class SetInline(admin.StackedInline):
    model = Set


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    search_fields = ("type__name", "slug", "workout__slug")
    date_hierarchy = "date_started"
    list_display = (
        "get_type",
        "slug",
        "workout",
        "date_started",
        "date_ended",
        "is_active",
    )
    inlines = [SetInline]

    @staticmethod
    def get_type(obj):
        if not hasattr(obj, "exercise_type"):
            return "N/A"

        return obj.exercise_type.name

    get_type.short_description = "Type"


@admin.register(WorkoutEvent)
class WorkoutEventAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
