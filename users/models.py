
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name



class Enquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


from django.db import models
from .models import User  # Your custom User model

class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question
    
from django.db import models
from .models import User

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
#     name = models.CharField(max_length=100, blank=True, null=True)  # Store name separately
#     email = models.EmailField(blank=True, null=True)  # Store email separately
#     headline = models.CharField(max_length=255, blank=True, null=True)
#     contact = models.CharField(max_length=15, blank=True, null=True)
#     github = models.URLField(blank=True, null=True)
#     linkedin = models.URLField(blank=True, null=True)
#     profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
#     resume = models.FileField(upload_to='resumes/', blank=True, null=True)
#     street_address = models.CharField(max_length=255, blank=True)
#     city = models.CharField(max_length=100, blank=True)
#     state = models.CharField(max_length=100, blank=True)
#     zip_code = models.CharField(max_length=20, blank=True)
#     country = models.CharField(max_length=100, blank=True)
#     enrollment = models.CharField(max_length=100, blank=True)
#     dob = models.DateField(null=True, blank=True)

#     def save(self, *args, **kwargs):
#         """ Automatically sync name & email from User model. """
#         if self.user:
#             self.name = self.user.name
#             self.email = self.user.email
#         super().save(*args, **kwargs)
#     def __str__(self):
#         return self.name if self.name else "Profile without name"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)  # Store name separately
    email = models.EmailField(blank=True, null=True)  # Store email separately
    headline = models.CharField(max_length=255, blank=True, null=True)
    contact = models.CharField(max_length=15, blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    street_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    enrollment = models.CharField(max_length=100, blank=True)
    dob = models.DateField(null=True, blank=True)
    experience_type = models.CharField(
        max_length=50,
        choices=[('Fresher', 'Fresher'), ('Experienced', 'Experienced')],
        default='Fresher'
    )

    def save(self, *args, **kwargs):
        """ Automatically sync name & email from User model. """
        if self.user:
            self.name = self.user.name
            self.email = self.user.email
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name if self.name else "Profile without name"

    def profile_completion_percentage(self):
        base_fields = [
            self.name,
            self.email,
            self.headline,
            self.contact,
            self.github,
            self.linkedin,
            self.profile_pic,
            self.resume,
            self.street_address,
            self.city,
            self.state,
            self.zip_code,
            self.country,
            self.enrollment,
            self.dob,
        ]

        filled_base = sum(1 for field in base_fields if field not in [None, '', ' '])
        total_base = len(base_fields)

        # Related data
        has_education = self.education.exists()
        has_experience = self.experience.exists() if self.experience_type == 'Experienced' else True
        has_skills = self.skills_certifications.skills if hasattr(self, 'skills_certifications') else []
        has_certifications = self.skills_certifications.certifications.exists() if hasattr(self, 'skills_certifications') else False

        extra_filled = sum([
            1 if has_education else 0,
            1 if has_experience else 0,
            1 if has_skills else 0,
            1 if has_certifications else 0,
        ])

        total_fields = total_base + 4  # base + education + experience + skills + certifications
        total_filled = filled_base + extra_filled

        return (total_filled / total_fields) * 100 if total_fields > 0 else 0



class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='education')
    education_level = models.CharField(max_length=50)
    college = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)

class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experience')
    company = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    role_type = models.CharField(max_length=50, choices=[('Full-Time', 'Full-Time'), ('Internship', 'Internship')])
   

# class ProfileSkillsCertifications(models.Model):
#     profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='skills_certifications')
#     skills = models.JSONField(default=list)  # Stores skills as a list
#     certifications = models.JSONField(default=list)  # Stores certifications as a list

#     def __str__(self):
#         return f"{self.profile.name} - Skills & Certifications"


class ProfileSkillsCertifications(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='skills_certifications')
    skills = models.JSONField(default=list)  # Stores skills as a list
    #certifications = models.JSONField(default=list)  # Stores certifications as a list

    def __str__(self):
        return f"{self.profile.name} - Skills"

class Certification(models.Model):
    profile = models.ForeignKey(ProfileSkillsCertifications, on_delete=models.CASCADE, related_name='certifications')
    certification_name = models.CharField(max_length=255)
    file = models.FileField(upload_to='certifications/', blank=True, null=True)
    def __str__(self):
        return self.certification_name

# models.py
import random
from django.db import models
from django.utils import timezone
from datetime import timedelta

class PasswordResetOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)

from django.db import models
from django.conf import settings
from tpo.models import Job  # update this import as needed

APPLICATION_STATUS_CHOICES = [
    ('applied', 'Applied'),
    ('shortlisted', 'Shortlisted'),
    ('interviewing', 'Interviewing'),
    ('placed', 'Placed'),
    ('rejected', 'Rejected'),
]
class JobApplication(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)  # Correct field name might be 'student', not 'user'
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS_CHOICES, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('job', 'student')  # Prevent duplicate applications

    def __str__(self):
        return f"{self.student} applied to {self.job}"
