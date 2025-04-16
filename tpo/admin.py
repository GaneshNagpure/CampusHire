from django.contrib import admin
from .models import Tpo, Job
# Register your models here.

class TpoAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'employee_id', 'mobile_number', 'is_approved')

admin.site.register(Tpo, TpoAdmin)

class JobAdmin(admin.ModelAdmin):
    list_display = ('company', 'role', 'salary_package', 'last_date_to_apply', 'eligibility', 'job_description', 'company_website', 'job_location')
    
admin.site.register(Job, JobAdmin)