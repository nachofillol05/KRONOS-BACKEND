from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

class DocumentType(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.name


class Nationality(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.name


class ContactInformation(models.Model):
    postalCode = models.CharField(max_length=20)
    street = models.CharField(max_length=255)
    streetNumber = models.CharField(max_length=10)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.street} {self.streetNumber}, {self.city}, {self.province}"


class School(models.Model):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=10)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    contactInfo = models.OneToOneField(ContactInformation, null=True, blank=True, on_delete=models.SET_NULL)
    directives = models.ManyToManyField('CustomUser', related_name='directed_schools', blank=True)

    def __str__(self) -> str:
        return f"{self.pk} - {self.name} ({self.abbreviation})"


class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('male', 'Masculino'),
        ('female', 'Femenino')
    ]
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    document = models.CharField(max_length=255, blank=True, null=True)
    hoursToWork = models.IntegerField(blank=True, null=True)
    documentType = models.ForeignKey(DocumentType, on_delete=models.SET_NULL, blank=True, null=True)
    nationality = models.ForeignKey(Nationality, on_delete=models.SET_NULL, blank=True, null=True)
    contactInfo = models.OneToOneField(ContactInformation, on_delete=models.SET_NULL, blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4, blank=True, null=True, editable=False)
    dark_mode = models.BooleanField(default=False)
    color = models.SmallIntegerField(blank=True, null=True)

    def is_directive(self, school: School) -> bool:
        return self in school.directives.all()
    
    def is_teacher(self, school: School):
        return TeacherSubjectSchool.objects.filter(school=school, teacher=self).exists()
    
    def is_preceptor(self, school: School):
        return Year.objects.filter(school=school, preceptors=self).exists()
    
    def __str__(self) -> str:
        return f'{self.pk} {self.username}'


class Module(models.Model):
    moduleNumber = models.IntegerField()
    day = models.CharField(max_length=10, choices=[
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes')
    ])
    endTime = models.TimeField()
    startTime = models.TimeField()
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.school.name} - {self.pk}. N°{self.moduleNumber}"


class AvailabilityState(models.Model):
    name = models.CharField(max_length=255)
    isEnabled = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class TeacherAvailability(models.Model):
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    loadDate = models.DateTimeField(auto_now_add=True)
    availabilityState = models.ForeignKey(AvailabilityState, null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f"{self.teacher} - {self.module} - {self.availabilityState}"


class Year(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    number = models.CharField(max_length=10)
    preceptors = models.ManyToManyField(CustomUser, related_name="years", blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="years")

    def __str__(self) -> str:
        return f'{self.pk}. N°{self.number} - {self.name} - {self.school}'
    


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name} - {self.year}"
    

class Subject(models.Model):
    name = models.CharField(max_length=255)
    studyPlan = models.TextField()
    description = models.CharField(max_length=255, blank=True)
    weeklyHours = models.IntegerField()
    color = models.CharField(max_length=7, blank=True)  # Including # for hex color
    abbreviation = models.CharField(max_length=10, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return f"{self.name} - {self.course}"


class TeacherSubjectSchool(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.teacher} - {self.subject} - {self.school}"


class Action(models.Model):
    name = models.CharField(max_length=255)
    isEnabled = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class Schedules(models.Model):
    date = models.DateTimeField()
    action = models.ForeignKey(Action, null=True, on_delete=models.SET_NULL)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    tssId = models.ForeignKey(TeacherSubjectSchool, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.date} - {self.action} - {self.module}"


class EventType(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    roles = models.ManyToManyField(Role)
    eventType = models.ForeignKey(EventType, null=True, on_delete=models.SET_NULL)
    affiliated_teachers = models.ManyToManyField(CustomUser, blank=True)

    def _str_(self) -> str:
        return f"{self.name} - {self.school} - {self.eventType}" 




        
