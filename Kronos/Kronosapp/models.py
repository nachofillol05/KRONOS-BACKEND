from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser


class DocumentType(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)


class Nationality(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)


class ContactInformation(models.Model):
    postalCode = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    streetNumber = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255)


class School(models.Model):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=10)
    logo = models.ImageField(upload_to='logos/', null=True)
    email = models.EmailField(max_length=255, unique=True)
    contactInfo = models.OneToOneField(ContactInformation, null=True, on_delete=models.SET_NULL)
    directives = models.ManyToManyField('CustomUser')

    def __str__(self) -> str:
        return f"{self.pk} - {self.name} ({self.abbreviation})"


class CustomUser(AbstractUser):
    GENDER_CHOICES = {
        'male': 'Masculino',
        'female': 'Femenino'
    }
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES,blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=False, unique=True)
    document = models.CharField(max_length=255, blank=True, null=True)
    hoursToWork = models.IntegerField(blank=True, null=True)
    documentType = models.ForeignKey(DocumentType, on_delete=models.SET_NULL,blank=True, null=True)
    nationality = models.ForeignKey(Nationality, on_delete=models.SET_NULL,blank=True, null=True)
    contactInfo = models.OneToOneField(ContactInformation, on_delete=models.SET_NULL,blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4,blank=True, null=True)
    dark_mode = models.BooleanField(default=False)
    color = models.SmallIntegerField(blank=True, null=True)

    def is_directive(self, school: School):
        return self in school.directives.all()
    
    def is_teacher(self, school: School):
        return TeacherSubjectSchool.objects.filter(school=school, teacher=self).exists()
    
    def is_preceptor(self, school: School):
        return Year.objects.filter(school=school, preceptors=self).exists()
    
    def __str__(self) -> str:
        return f'{self.pk} {self.username}'


class Module(models.Model):
    DAY_CHOICES = {
        'monday': 'Lunes',
        'tuesday': 'Martes',
        'wednesday': 'Miércoles',
        'thursday': 'Jueves',
        'friday': 'Viernes',
        'saturday': 'Sábado',
        'sunday': 'Domingo'
    }
    moduleNumber = models.IntegerField()
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    endTime = models.TimeField()
    startTime = models.TimeField()
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.school.name} - {self.pk}. N°{self.moduleNumber}"


class AvailabilityState(models.Model):
    name = models.CharField(max_length=255)
    isEnabled = models.BooleanField()


class TeacherAvailability(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    loadDate = models.DateTimeField()
    availabilityState = models.ForeignKey(AvailabilityState, null=True, on_delete=models.SET_NULL)


class Year(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    preceptors = models.ManyToManyField(CustomUser, related_name="years")
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="years")

    def __str__(self) -> str:
        return f'{self.pk}. N°{self.number} - {self.name} - {self.school}'


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name} - {self.year}"


class Subject(models.Model):
    name = models.CharField(max_length=255)
    studyPlan = models.TextField()
    description = models.CharField(max_length=255)
    weeklyHours = models.IntegerField()
    color = models.CharField(max_length=6)
    abbreviation = models.CharField(max_length=10)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.course}"


class TeacherSubjectSchool(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Action(models.Model):
    name = models.CharField(max_length=255)
    isEnabled = models.BooleanField()


class Schedules(models.Model):
    date = models.DateTimeField()
    action = models.ForeignKey(Action, null=True, on_delete=models.SET_NULL)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    tssId = models.ForeignKey(TeacherSubjectSchool, on_delete=models.CASCADE)


class EventType(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    eventType = models.ForeignKey(EventType, null=True, on_delete=models.SET_NULL)
    affiliated_teachers = models.ManyToManyField(CustomUser)
