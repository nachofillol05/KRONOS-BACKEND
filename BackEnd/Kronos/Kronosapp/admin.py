from django.contrib import admin
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Modules)
admin.site.register(ContactInformation)
admin.site.register(Schools)
admin.site.register(AvailabilityStates)
admin.site.register(DocumentTypes)
admin.site.register(Nationalities)
admin.site.register(Roles)
admin.site.register(customuser)
admin.site.register(TeacherAvailability)
admin.site.register(Years)
admin.site.register(Courses)
admin.site.register(Subjects)
admin.site.register(TeacherSubjectSchool)
admin.site.register(Actions)
admin.site.register(Schedules)
admin.site.register(EventTypes)
admin.site.register(Events)
admin.site.register(TeacherEvent)