from django.contrib import admin

from .models import (
    Module,
    ContactInformation,
    School,
    AvailabilityState,
    DocumentType,
    CustomUser,
    TeacherAvailability,
    Year,
    Course,
    Subject,
    TeacherSubjectSchool,
    Action,
    Schedules,
    EventType,
    Event,
    Nationality,
    Role
)


# Register your models here.
admin.site.register(Module)
admin.site.register(ContactInformation)
admin.site.register(School)
admin.site.register(AvailabilityState)
admin.site.register(DocumentType)
admin.site.register(Nationality)
admin.site.register(CustomUser)
admin.site.register(TeacherAvailability)
admin.site.register(Year)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(TeacherSubjectSchool)
admin.site.register(Action)
admin.site.register(Schedules)
admin.site.register(EventType)
admin.site.register(Event)
admin.site.register(Role)
