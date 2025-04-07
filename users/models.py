
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

    def save(self, *args, **kwargs):
        """ Automatically sync name & email from User model. """
        if self.user:
            self.name = self.user.name
            self.email = self.user.email
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name if self.name else "Profile without name"


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