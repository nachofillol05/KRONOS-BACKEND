from django.db import models

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

class Users(models.Model):
    userId = models.IntegerField(primary_key=True)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    gender = models.CharField(max_length=255, choices=[('Male', 'Male'), ('Female', 'Female')])
    email = models.CharField(max_length=255)
    document = models.CharField(max_length=255)
    hoursToWork = models.IntegerField()
    documentTypeId = models.ForeignKey('DocumentTypes', on_delete=models.CASCADE)
    nationalityId = models.ForeignKey('Nationalities', on_delete=models.CASCADE)
    contactInfoId = models.OneToOneField('ContactInformation', on_delete=models.CASCADE)
    roleId = models.ForeignKey('Roles', on_delete=models.CASCADE)

class TeacherAvailability(models.Model):
    moduleId = models.ForeignKey('Modules', on_delete=models.CASCADE)
    teacherId = models.ForeignKey('Users', on_delete=models.CASCADE)
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
    teacherId = models.ForeignKey('Users', on_delete=models.CASCADE)

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
    teacherId = models.ForeignKey('Users', on_delete=models.CASCADE)
    eventId = models.ForeignKey('Events', on_delete=models.CASCADE)
    class Meta:
        unique_together = ('teacherId', 'eventId')