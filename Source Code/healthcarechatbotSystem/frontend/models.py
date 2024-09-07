from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import time


# Create your models here.


class Doctor(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    licenseNo = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    phonenumber = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    specialization = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Patient(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    # created_at=models.DateTimeField(auto_now_add=True)
    gender = models.CharField(max_length=10)
    phonenumber = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Contact(models.Model):
    contactname = models.CharField(max_length=50)
    contactemail = models.EmailField(unique=True)
    contactphonenumber = models.CharField(max_length=15)
    message = models.TextField()

    def __str__(self):
        return self.name


class Appointment(models.Model):
    doctorname = models.CharField(max_length=50)
    doctoremail = models.EmailField(max_length=50)
    patientname = models.CharField(max_length=50)
    patientemail = models.EmailField(max_length=50)
    appointmentdate = models.DateField(max_length=10)
    followupdate = models.DateField(null=True, max_length=10)
    symptoms = models.CharField(max_length=100)
    status = models.BooleanField()
    prescription = models.CharField(max_length=200)
    appointment_time = models.TimeField(default=time(10, 0))

    def __str__(self):
        return f"{self.patientname} has appointment on  {self.appointmentdate} at {self.appointment_time} with {self.doctorname}"

