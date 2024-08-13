from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser
import uuid
from django.core.exceptions import ValidationError


def validate_numeric(value):
    if not value.isdigit():
        raise ValidationError(
            '%(value)s no es un número válido',
            params={'value': value},
        )
    

class CustomUserManager(BaseUserManager):
    def create_user(self, document, email, password=None, **extra_fields):
        if not document:
            raise ValueError('The Document field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(document=document, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, document, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(document, email, password, **extra_fields)


class DocumentType(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return f"{self.pk}, {self.name}"


class Nationality(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.name


class ContactInformation(models.Model):
    postalCode = models.CharField(max_length=20)
    street = models.CharField(max_length=255)
    streetNumber = models.CharField(max_length=10, validators=[validate_numeric])
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
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino')
    ]
    document = models.CharField(max_length=255, unique=True, blank=True, null=True, validators=[validate_numeric])
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    profile_picure = models.ImageField(upload_to='logos/', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    hoursToWork = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=25, blank=True, null=True, validators=[validate_numeric])
    documentType = models.ForeignKey(DocumentType, on_delete=models.SET_NULL, blank=True, null=True)
    nationality = models.ForeignKey(Nationality, on_delete=models.SET_NULL, blank=True, null=True)
    contactInfo = models.OneToOneField(ContactInformation, on_delete=models.SET_NULL, blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4, blank=True, null=True, editable=False)
    dark_mode = models.BooleanField(default=False)
    color = models.SmallIntegerField(blank=True, null=True)

    username = None
    USERNAME_FIELD = 'document'

    objects = CustomUserManager()

    def is_directive(self, school: School) -> bool:
        return self in school.directives.all()
    
    def is_teacher(self, school: School):
        return TeacherSubjectSchool.objects.filter(school=school, teacher=self).exists()
    
    def is_preceptor(self, school: School):
        return Year.objects.filter(school=school, preceptors=self).exists()
    
    def __str__(self) -> str:
        return f'{self.pk} {self.email}'


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
    number = models.CharField(max_length=1)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="years")
    preceptors = models.ManyToManyField(CustomUser)

    def __str__(self) -> str:
        return f'{self.pk}. N°{self.number} - {self.name} - {self.school}'    


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"({self.pk}) {self.name} - {self.year}"
    

class Subject(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    weeklyHours = models.IntegerField()
    color = models.CharField(max_length=7, blank=True)
    abbreviation = models.CharField(max_length=10, blank=True)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return f"{self.name} - {self.school}"


class CourseSubjects(models.Model):
    studyPlan = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class TeacherSubjectSchool(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    subject = models.ForeignKey(CourseSubjects, on_delete=models.SET_NULL, null=True, blank=True)
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

    def __str__(self) -> str:
        return f"{self.name} - {self.school} - {self.eventType}"
