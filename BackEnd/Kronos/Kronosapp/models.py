from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser


class Modules(models.Model):
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
    postalCode = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    streetNumber = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255)

class Schools(models.Model):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=10)
    logo = models.ImageField(upload_to='logos/')
    email = models.EmailField(max_length=255, unique=True)
    contactInfoId = models.OneToOneField('ContactInformation', on_delete=models.SET_NULL)

class AvailabilityStates(models.Model):
    name = models.CharField(max_length=255)
    isEnabled = models.BooleanField()

class DocumentTypes(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class Nationalities(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class Roles(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class CustomUser(AbstractUser):
    firstName = models.CharField(max_length=255,blank=True, null=True)
    lastName = models.CharField(max_length=255,blank=True, null=True)
    gender = models.CharField(max_length=255, choices=[('Male', 'Male'), ('Female', 'Female')],blank=True, null=True)
    email = models.CharField(max_length=255,blank=True, null=False, unique=True)
    document = models.CharField(max_length=255,blank=True, null=True)
    hoursToWork = models.IntegerField(blank=True, null=True)
    documentTypeId = models.ForeignKey('DocumentTypes', on_delete=models.SET_NULL,blank=True, null=True)
    nationalityId = models.ForeignKey('Nationalities', on_delete=models.SET_NULL,blank=True, null=True)
    contactInfoId = models.OneToOneField('ContactInformation', on_delete=models.SET_NULL,blank=True, null=True)
    roleId = models.ForeignKey('Roles', on_delete=models.SET_NULL,blank=True, null=True)
    email_verified = models.BooleanField(default=False,blank=True, null=True)
    verification_token = models.UUIDField(default=uuid.uuid4,blank=True, null=True)

class TeacherAvailability(models.Model):
    moduleId = models.ForeignKey('Modules', on_delete=models.CASCADE)
    teacherId = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    loadDate = models.DateTimeField()
    availabilityStateId = models.ForeignKey('AvailabilityStates', on_delete=models.CASCADE)

class Years(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    number = models.CharField(max_length=255)

class Courses(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    yearId = models.ForeignKey('Years', on_delete=models.CASCADE)

class Subjects(models.Model):
    name = models.CharField(max_length=255)
    studyPlan = models.TextField()
    description = models.CharField(max_length=255)
    weeklyHours = models.IntegerField()
    color = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=255)
    yearId = models.ForeignKey('Years', on_delete=models.CASCADE)
    courseId = models.ForeignKey('Courses', on_delete=models.SET_NULL)

class TeacherSubjectSchool(models.Model):
    schoolId = models.ForeignKey('Schools', on_delete=models.CASCADE)
    subjectId = models.ForeignKey('Subjects', on_delete=models.CASCADE)
    teacherId = models.ForeignKey('CustomUser', on_delete=models.CASCADE)

class Actions(models.Model):
    name = models.CharField(max_length=255)
    isEnabled = models.BooleanField()

class Schedules(models.Model):
    date = models.DateTimeField()
    actionId = models.ForeignKey('Actions', on_delete=models.SET_NULL)
    moduleId = models.ForeignKey('Modules', on_delete=models.CASCADE)
    tssId = models.ForeignKey('TeacherSubjectSchool', on_delete=models.CASCADE)

class EventTypes(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class Events(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    school = models.ForeignKey(Schools, on_delete=models.CASCADE)
    eventType = models.ForeignKey(EventTypes, on_delete=models.SET_NULL)
    affiliated_teachers = models.ManyToManyField(CustomUser)