from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from django.db.models.signals import post_save

from django.dispatch import receiver

from rest_framework.authtoken.models import Token

# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STUDENT = "STUDENT", "Student"
        TEACHER = "TEACHER", "Teacher"
    
    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self,*args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)

class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role = User.Role.STUDENT)
    
class Student(User):
    base_role = User.Role.STUDENT
    student  = StudentManager()
    class Meta:
        proxy = True
    
    def welcome(self):
        return "Welcome Student"
    

class StudentProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'MALE'),
        ('F', 'FEMALE')
    )
    CLASS_CHOICES = (
        ('X', 'X'),
        ('IX', 'IX'),
        ('VIII', 'VIII'),
        ('VII', 'VII'),
        ('VI', 'VI'),
        ('V', 'V')
    )
    STATE_CHOICES = (
        ('ANDHRA PRADESH', 'ANDHRA PRADESH'),
        ('ANDAMAN & NICOBAR ISLAND', 'ANDAMAN & NICOBAR ISLAND'),
        ('ARUNACHAL PRADESH', 'ARUNACHAL PRADESH'),
        ('ASSAM', 'ASSAM'),
        ('BIHAR', 'BIHAR'),
        ('CHANDIGARH', 'CHANDIGARH'),
        ('CHATTISGARH', 'CHATTISGARH'),
        ('DADRA & NAGAR HAVELI & DAMAN & DIU',
         'DADRA & NAGAR HAVELI & DAMAN & DIU'),
        ('DELHI', 'DELHI'),
        ('GOA', 'GOA'),
        ('GUJARAT', 'GUJARAT'),
        ('HARYANA', 'HARYANA'),
        ('HIMACHAL PRADESH', 'HIMACHAL PRADESH'),
        ('JHARKHAND', 'JHARKHAND'),
        ('JAMMU & KASHMIR', 'JAMMU & KASHMIR'),
        ('KARNATAKA', 'KARNATAKA'),
        ('KERALA', 'KERALA'),
        ('LADAKH', 'LADAKH'),
        ('LAKSHADWEEP', 'LAKSHADWEEP'),
        ('MADHYA PRADESH', 'MADHYA PRADESH'),
        ('MAHARASHTRA', 'MAHARASHTRA'),
        ('MANIPUR', 'MANIPUR'),
        ('MEGHALAYA', 'MEGHALAYA'),
        ('MIZORAM', 'MIZORAM'),
        ('NAGALAND', 'NAGALAND'),
        ('ODISHA', 'ODISHA'),
        ('PUDUCHERRY', 'PUDUCHERRY'),
        ('PUNJAB', 'PUNJAB'),
        ('RAJASTHAN', 'RAJASTHAN'),
        ('SIKKIM', 'SIKKIM'),
        ('TAMIL NADU', 'TAMIL NADU'),
        ('TELANGANA', 'TELANGANA'),
        ('TRIPURA', 'TRIPURA'),
        ('UTTARAKHAND', 'UTTARAKHAND'),
        ('UTTAR PRADESH', 'UTTAR PRADESH'),
        ('WEST BENGAL', 'WEST BENGAL'),

    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to="files/avatar", null=True, blank=True)
    student_rkv_id = models.IntegerField(null=True, blank=True)
    fathers_name = models.CharField(max_length=100, null=True, blank=True)
    mothers_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    date_of_birth = models.DateField(max_length=8, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    blood_group = models.CharField(max_length=6, null=True, blank=True)
    class_name = models.CharField(
        max_length=5, choices=CLASS_CHOICES, null=True, blank=True)
    school_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    pincode = models.CharField(max_length=6, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=50, default='Muzaffarpur')
    state_and_ut = models.CharField(
        max_length=50, choices=STATE_CHOICES, default="BIHAR")

    country = models.CharField(max_length=50, default='India')

    def __str__(self):
        return f"{self.user} + {self.first_name}"
    

@receiver(post_save, sender =User)
@receiver(post_save, sender=Student)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    if created:
        Token.objects.create(user = instance)

@receiver(post_save, sender= Student)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.role == "STUDENT":
        StudentProfile.objects.create(user = instance)
