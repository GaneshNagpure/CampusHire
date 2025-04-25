from django.contrib import admin
from django.utils.html import format_html

from .models import Tpo, Job, Drive
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

class DriveAdmin(admin.ModelAdmin):
    list_display = ('job', 'tpo', 'drive_date', 'venue', 'created_at')
    list_filter = ('drive_date',)
    search_fields = ('job__role', 'tpo__full_name', 'venue') 

admin.site.register(Drive, DriveAdmin) 

from django.contrib import admin
from .models import HiringPartner

class HiringPartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'year', 'added_on', 'total_hired_students', 'logo')  # Display these fields in the admin list
    search_fields = ('name', 'website')  # Add search functionality by name and website
    list_filter = ('year',)  # Add filter by year
    ordering = ('-added_on',)  # Default ordering by added_on (descending)

    # Optionally, you can also make fields editable directly from the list view
    list_editable = ('year',)  # Make 'year' field editable directly in the list view

admin.site.register(HiringPartner, HiringPartnerAdmin)

