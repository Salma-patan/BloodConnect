from django.db import models
from django.contrib.auth.models import User

# REGISTRATION

class Registration(models.Model):

    ROLE_CHOICES = (
        ('Donor', 'Donor'),
        ('Patient', 'Patient'),
    )

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    )

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=15)

    country = models.CharField(max_length=100)

    state = models.CharField(max_length=100)

    district = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    city_town = models.CharField(max_length=100)

    pincode = models.CharField(max_length=10)

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    person = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    bloodgroup = models.CharField(max_length=10)

    dob = models.DateField()

    password = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    count = models.IntegerField(default=0)

    last_donation = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name

# LOGIN
class login(models.Model):

    email = models.EmailField(max_length=200)

    password = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

# CONTACT
class Contact(models.Model):

    first_name = models.CharField(max_length=250)

    last_name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    Message = models.TextField(max_length=2000)

    def __str__(self):
        return self.first_name

# DONOR PROFILE
class Donor(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    first_name = models.CharField(max_length=250)

    last_name = models.CharField(max_length=250)

    email = models.EmailField(max_length=250)

    phone = models.CharField(max_length=250)

    country = models.CharField(max_length=250)

    state = models.CharField(max_length=250)

    district = models.CharField(max_length=100)

    city_town = models.CharField(max_length=250)

    pincode = models.CharField(max_length=250)

    bloodgroup = models.CharField(max_length=250)

    person = models.CharField(max_length=100)

    dob = models.DateField()

    def __str__(self):
        return self.user.first_name

# DONATE BLOOD
class donateblood(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    bloodgroup = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    date = models.DateField()
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    city_town = models.CharField(max_length=100)
    units = models.IntegerField()

    status = models.CharField(
        max_length=20,
        default="Pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name

# PATIENT REQUEST
from django.db import models
from .models import Registration

class patientrequest(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    )

    patient_name = models.CharField(max_length=100)

    donor = models.ForeignKey(
        Registration,
        on_delete=models.CASCADE,
        limit_choices_to={'person': 'Donor'}
    )
    donor_email=models.EmailField(max_length=30)
    bloodgroup = models.CharField(max_length=10)
    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.donor:
            return f"{self.patient_name} -> {self.donor.first_name}"
        return f"{self.patient_name} -> Unknown Donor"

    class Meta:
        ordering = ['-date']
# BLOOD CAMP
class Camp(models.Model):

    camp_name = models.CharField(max_length=200)

    location = models.CharField(max_length=200)

    date = models.DateField()

    time = models.TimeField(default='10:00:00')

    contact = models.CharField(max_length=15)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.camp_name

# DONOR REGISTRATION
class donorreg(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    bloodgroup = models.CharField(max_length=10)

    last_donation = models.DateField(
        null=True,
        blank=True
    )

    count = models.IntegerField(default=0)

    def __str__(self):
        return self.first_name

# NOTIFICATIONS
from django.db import models
from .models import Registration


class Notification(models.Model):

    NOTIFICATION_CHOICES = (
        ('Request', 'Request'),
        ('Donation', 'Donation'),
        ('Reward', 'Reward'),
        ('Camp', 'Camp'),
        ('Profile', 'Profile'),
    )

    donor = models.ForeignKey(
        Registration,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    notification_type = models.CharField(
        max_length=50,
        choices=NOTIFICATION_CHOICES
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.donor.first_name} - {self.notification_type}"
# CAMP REGISTRATION
class CampRegistration(models.Model):

    donor = models.ForeignKey(
        Registration,
        on_delete=models.CASCADE,
        limit_choices_to={'person': 'Donor'}
    )

    camp_name = models.CharField(max_length=100)

    location = models.CharField(max_length=200)

    date = models.DateField()

    time = models.TimeField(default='10:00:00')

    phone = models.CharField(max_length=15)

    bloodgroup = models.CharField(max_length=10)

    status = models.CharField(
        max_length=20,
        default='Registered'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor.first_name} - {self.camp_name}"
    
#blood request
from django.db import models
from django.contrib.auth.models import User


class BloodRequest(models.Model):

    patient_name = models.CharField(max_length=100)

    donor_name = models.CharField(max_length=100)

    donor_email = models.EmailField()

    blood_group = models.CharField(max_length=10)

    message = models.TextField()

    status = models.CharField(
        max_length=20,
        default='Pending'
    )

    date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.patient_name
    
class Patient(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    first_name = models.CharField(max_length=250)

    last_name = models.CharField(max_length=250)

    email = models.EmailField(max_length=250)

    phone = models.CharField(max_length=250)

    country = models.CharField(max_length=250)

    state = models.CharField(max_length=250)

    district = models.CharField(max_length=100)

    city_town = models.CharField(max_length=250)

    pincode = models.CharField(max_length=250)

    bloodgroup = models.CharField(max_length=250)

    dob = models.DateField()

    disease = models.CharField(
        max_length=250,
        blank=True,
        null=True
    )

    hospital = models.CharField(
        max_length=250,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.first_name    


#blood banks
class BloodBank(models.Model):

    BLOOD_CHOICES = (

        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),

    )

    bank_name = models.CharField(max_length=200)

    location = models.CharField(max_length=200)

    contact = models.CharField(max_length=15)

    bloodgroup = models.CharField(
        max_length=5,
        choices=BLOOD_CHOICES
    )

    units_available = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.bank_name
    
class PatientNotification(models.Model):

    patient = models.ForeignKey(
        Registration,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    notification_type = models.CharField(max_length=50)

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


#admin notification
from django.contrib.auth.models import User
from django.db import models

class AdminNotification(models.Model):
    NOTIF_TYPES = (
        ('donor', 'Donor Request'),
        ('camp', 'Camp Update'),
        ('system', 'System'),
    )

    title = models.CharField(max_length=255)
    message = models.TextField()
    notif_type = models.CharField(max_length=20, choices=NOTIF_TYPES, default='system')

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

  

    def __str__(self):
        return self.title