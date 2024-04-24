from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser


class Modules(models.Model):
    moduleId = models.IntegerField(primary_key=True)
    moduleNumber = models.IntegerField()
    dayId = models.CharField(max_length=10, choices=[
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ])
    endTime = models.TimeField()
    startTime = models.TimeField()
    schoolId = models.ForeignKey('Schools', on_delete=models.CASCADE)

class ContactInformation(models.Model):
    contactInfoId = models.IntegerField(primary_key=True)
    phoneNumber = models.CharField(max_length=255)
    postalCode = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    streetNumber = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

class Schools(models.Model):
    schoolId = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=10)
    logo = models.ImageField(upload_to='logos/')
    email = models.EmailField(max_length=255)
    contactInfoId = models.OneToOneField('ContactInformation', on_delete=models.CASCADE)

class AvailabilityStates(models.Model):
    availabilityStateId = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    isEnabled = models.BooleanField()

class DocumentTypes(models.Model):
    documentTypeId = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class Nationalities(models.Model):
    nationalityId = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class Roles(models.Model):
    roleId = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class customuser(AbstractUser):
    firstName = models.CharField(max_length=255,blank=True, null=True)
    lastName = models.CharField(max_length=255,blank=True, null=True)
    gender = models.CharField(max_length=255, choices=[('Male', 'Male'), ('Female', 'Female')],blank=True, null=True)
    email = models.CharField(max_length=255,blank=True, null=True)
    document = models.CharField(max_length=255,blank=True, null=True)
    hoursToWork = models.IntegerField(blank=True, null=True)
    documentTypeId = models.ForeignKey('DocumentTypes', on_delete=models.CASCADE,blank=True, null=True)
    nationalityId = models.ForeignKey('Nationalities', on_delete=models.CASCADE,blank=True, null=True)
    contactInfoId = models.OneToOneField('ContactInformation', on_delete=models.CASCADE,blank=True, null=True)
    roleId = models.ForeignKey('Roles', on_delete=models.CASCADE,blank=True, null=True)
    email_verified = models.BooleanField(default=False,blank=True, null=True)
    verification_token = models.UUIDField(default=uuid.uuid4,blank=True, null=True)

class TeacherAvailability(models.Model):
    moduleId = models.ForeignKey('Modules', on_delete=models.CASCADE)
    teacherId = models.ForeignKey('customuser', on_delete=models.CASCADE)
    loadDate = models.DateTimeField()
    availabilityStateId = models.ForeignKey('AvailabilityStates', on_delete=models.CASCADE)

class Years(models.Model):
    yearId = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    number = models.CharField(max_length=255)

class Courses(models.Model):
    courseId = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    yearId = models.ForeignKey('Years', on_delete=models.CASCADE)

class Subjects(models.Model):
    subjectId = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    studyPlan = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    weeklyHours = models.IntegerField()
    color = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=255)
    yearId = models.ForeignKey('Years', on_delete=models.CASCADE)
    courseId = models.ForeignKey('Courses', on_delete=models.CASCADE)

class TeacherSubjectSchool(models.Model):
    schoolId = models.ForeignKey('Schools', on_delete=models.CASCADE)
    subjectId = models.ForeignKey('Subjects', on_delete=models.CASCADE)
    teacherId = models.ForeignKey('customuser', on_delete=models.CASCADE)

class Actions(models.Model):
    actionId = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    isEnabled = models.BooleanField()

class Schedules(models.Model):
    scheduleId = models.IntegerField(primary_key=True)
    date = models.DateTimeField()
    actionId = models.ForeignKey('Actions', on_delete=models.CASCADE)
    moduleId = models.ForeignKey('Modules', on_delete=models.CASCADE)
    tssId = models.ForeignKey('TeacherSubjectSchool', on_delete=models.CASCADE)

class EventTypes(models.Model):
    eventTypeId = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class Events(models.Model):
    eventId = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    schoolId = models.ForeignKey('Schools', on_delete=models.CASCADE)
    eventTypeId = models.ForeignKey('EventTypes', on_delete=models.CASCADE)

class TeacherEvent(models.Model):
    teacherId = models.ForeignKey('customuser', on_delete=models.CASCADE)
    eventId = models.ForeignKey('Events', on_delete=models.CASCADE)
    class Meta:
        unique_together = ('teacherId', 'eventId')