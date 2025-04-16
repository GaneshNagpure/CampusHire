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
    
class Job(models.Model):
    company = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    salary_package = models.DecimalField(max_digits=10, decimal_places=2)
    last_date_to_apply = models.DateField()
    eligibility = models.TextField()
    job_description = models.TextField() 
    company_website = models.URLField(max_length=200, blank=True, null=True)  # Optional field for company website
    job_location = models.CharField(max_length=100, blank=True, null=True)  # Optional field for job location
    

    def __str__(self):
        return f"{self.role} at {self.company}"
