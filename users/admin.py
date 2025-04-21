from django.contrib import admin
from .models import User, Enquiry, Profile, Education, Experience,ProfileSkillsCertifications

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'password','id')

class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'message', 'created_at')
    
admin.site.register(User, UserAdmin)
admin.site.register(Enquiry, EnquiryAdmin)

from django.contrib import admin
from .models import FAQ

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_approved', 'submitted_by', 'submitted_at')
    list_filter = ('is_approved', 'submitted_at')
    search_fields = ('question', 'answer')
    actions = ['approve_faqs']

    def approve_faqs(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected FAQs have been approved.")
    approve_faqs.short_description = "Approve selected FAQs"

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'headline', 'contact', 'github', 'linkedin','experience_type','city','enrollment','dob','email','id','profile_pic','resume')
    search_fields = ('user__username', 'headline', 'contact')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('profile', 'education_level', 'college', 'degree')
    search_fields = ('profile__user__username', 'college', 'degree')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('profile', 'company', 'role', 'start_date', 'end_date', 'role_type')
    search_fields = ('profile__user__username', 'company', 'role')

# @admin.register(Skill)
# class SkillAdmin(admin.ModelAdmin):
#     list_display = ('profile', 'skill_name')
#     search_fields = ('profile__user__username', 'skill_name')

# @admin.register(Certification)
# class CertificationAdmin(admin.ModelAdmin):
#     list_display = ('profile', 'certification_name')
#     search_fields = ('profile__user__username', 'certification_name')

# @admin.register(ProfileSkillsCertifications)
# class ProfileSkillsCertificationsAdmin(admin.ModelAdmin):
#     list_display = ( 'skill_name', 'certification_name')
#     search_fields = ('profile__user__username', 'skill_name', 'certification_name')

# from django.contrib import admin
# from .models import ProfileSkillsCertifications

# class ProfileSkillsCertificationsAdmin(admin.ModelAdmin):
#     list_display = ('profile', 'display_skills', 'display_certifications')  # ✅ Updated field names

#     def display_skills(self, obj):
#         return ", ".join(obj.skills) if obj.skills else "No skills"

#     def display_certifications(self, obj):
#         return ", ".join(obj.certifications) if obj.certifications else "No certifications"

#     display_skills.short_description = "Skills"
#     display_certifications.short_description = "Certifications"

# admin.site.register(ProfileSkillsCertifications, ProfileSkillsCertificationsAdmin)

from django.contrib import admin
from django.utils.html import format_html, format_html_join, mark_safe
from .models import ProfileSkillsCertifications, Certification

class ProfileSkillsCertificationsAdmin(admin.ModelAdmin):
    list_display = ('profile', 'display_skills', 'display_certifications')

    def display_skills(self, obj):
        return ", ".join(obj.skills) if obj.skills else "No skills"

    def display_certifications(self, obj):
        certifications = obj.certifications.all()
        if not certifications:
            return "No certifications"
        return format_html_join(
            mark_safe('<br>'),
            '<a href="{}" target="_blank">{}</a>',
            ((cert.file.url, cert.certification_name) for cert in certifications)
        )

    display_skills.short_description = "Skills"
    display_certifications.short_description = "Certifications"

admin.site.register(ProfileSkillsCertifications, ProfileSkillsCertificationsAdmin)

# from django.contrib import admin
# from .models import JobApplication

# @admin.register(JobApplication)
# class JobApplicationAdmin(admin.ModelAdmin):
#     list_display = ('student', 'job', 'applied_at')
#     list_filter = ('job', 'applied_at')
#     search_fields = ('student__name', 'job__role')
from django.contrib import admin
from .models import JobApplication

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'job', 'status', 'applied_at')  # Added 'status' to list_display
    list_filter = ('job', 'status', 'applied_at')  # Added 'status' to list_filter
    search_fields = ('student__name', 'job__role')

    # Enable editing the 'status' field directly in the list view
    list_editable = ('status',)