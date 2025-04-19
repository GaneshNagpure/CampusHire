from django.db import models

# Create your models here.
class Tpo(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=100, unique=True)  # Unique employee ID
    email = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=100)
    password = models.CharField(max_length=255)  # It is recommended to hash passwords
    is_approved = models.BooleanField(default=False)  # Admin approval status
    
    def __str__(self):
        return self.full_name
    
from django.utils import timezone
from datetime import timedelta
class Job(models.Model):
    company = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    salary_package = models.DecimalField(max_digits=10, decimal_places=2)
    last_date_to_apply = models.DateField()
    eligibility = models.TextField()
    job_description = models.TextField() 
    company_website = models.URLField(max_length=200, blank=True, null=True)  # Optional field for company website
    job_location = models.CharField(max_length=100, blank=True, null=True)  # Optional field for job location
    tpo = models.ForeignKey(Tpo, on_delete=models.CASCADE, related_name='jobs',default=True)  # Link to TPO who created the job
    is_active = models.BooleanField(default=True )  # Flag to indicate if the job is active or
    # created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the job was created
    # updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the job was last updated

    created_at = models.DateTimeField(default=timezone.now)
    # created_at= models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.role} at {self.company}"

class Alumni(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    course = models.CharField(max_length=100)
    passing_year = models.IntegerField()
    current_company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    is_visible = models.BooleanField(default=True)  # TPO can toggle this
    profile_pic = models.ImageField(upload_to='alumni_profiles/', blank=True, null=True)
 
    def __str__(self):
        return self.name
