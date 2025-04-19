from django.contrib import admin
from django.utils.html import format_html

from .models import Tpo, Job
# Register your models here.

class TpoAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'employee_id', 'mobile_number', 'is_approved')

admin.site.register(Tpo, TpoAdmin)

class JobAdmin(admin.ModelAdmin):
    list_display = ('company', 'role', 'salary_package', 'last_date_to_apply', 'eligibility', 'job_description', 'company_website', 'job_location', 'tpo', 'is_active', 'created_at')
    
admin.site.register(Job, JobAdmin)

from django.contrib import admin
from .models import Alumni

@admin.register(Alumni)
class AlumniAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'course', 'passing_year', 'current_company', 'position', 'is_visible', 'profile_pic')
    search_fields = ('name', 'email', 'course', 'current_company')
   