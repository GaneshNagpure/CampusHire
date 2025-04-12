from django.shortcuts import render, redirect
from django.contrib import messages
import re 
import hashlib
from django.contrib.auth import logout as auth_logout
from .models import *
from django.core.mail import EmailMessage  
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required  # For requiring login to ask a question





# Create your views here.
def home(request):
    return render(request, 'home.html')

def terms(request):
    return render(request, 'termsandconditions.html')


def register(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_repeat = request.POST.get('password_repeat')

        # Check if fields are empty
        if not name or not email or not password or not password_repeat:
            messages.error(request, "All fields are required.")
            return render(request, 'register.html')

        # Validate password match
        if password != password_repeat:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        # Validate strong password
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return render(request, 'register.html')

        if not re.search(r'[A-Z]', password):
            messages.error(request, "Password must contain at least one uppercase letter.")
            return render(request, 'register.html')

        if not re.search(r'[a-z]', password):
            messages.error(request, "Password must contain at least one lowercase letter.")
            return render(request, 'register.html')

        if not re.search(r'\d', password):
            messages.error(request, "Password must contain at least one digit.")
            return render(request, 'register.html')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            messages.error(request, "Password must contain at least one special character.")
            return render(request, 'register.html')

        # Check if the email already exists in the database
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'register.html')

        # Create new user (assuming password is stored securely using hashing)
        #hash the password beore saving
        user = User(name=name, email=email, password=password)
        #user.set_password(password)  # Hash the password before saving
        user.save()
        
        storage = messages.get_messages(request)
        list(storage)

        messages.success(request, 'Your account has been created successfully.')
        return redirect('login')  # Redirect to login page after successful registration
    

    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if user exists
        try:
            user = User.objects.get(email=email)
            
            # Check if the entered password matches the stored password (in plain text)
            if user.password == password:
                # Manually create a session for the user
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                #messages.success(request, f"Welcome back, {user.name}!")
                return redirect('dashboard')  # Redirect to the dashboard page
            else:
                messages.error(request, "Invalid password. Please try again.")
        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")
        
        return render(request, 'login.html')

    return render(request, 'login.html')

# def dashboard(request):
#     if 'user_id' not in request.session:
#         return redirect('login')
    
#     user_id = request.session['user_id']
#     user = User.objects.get(id=user_id)
#     profile = user.profile  # Assuming you have a related name for the profile in User model
#     print(profile)
#     print(user)


#     skillscertifications = ProfileSkillsCertifications.objects.get(profile=profile)
#     print(skillscertifications)

#     messages.success(request, f"Welcome back, {user.name}!")
    
#     return render(request, 'dashboard.html', {'user': user,'skillscertifications': skillscertifications})   
#

from .models import User, Profile, Education, Experience, ProfileSkillsCertifications


def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)

    # ✅ Ensure profile exists
    profile, created = Profile.objects.get_or_create(user=user)
    print("Profile Image URL:", profile.profile_pic.url if profile.profile_pic else "No Image Found")


    # ✅ Ensure ProfileSkillsCertifications exists
    skillscertifications, created = ProfileSkillsCertifications.objects.get_or_create(profile=profile)
    certifications = skillscertifications.certifications.all()


    messages.success(request, f"Welcome back, {user.name}!")

    return render(request, 'dashboard.html', {
        'user': user,
        'profile': profile,
        'skillscertifications': skillscertifications,
        'certifications': certifications,
       })


def logout(request):
    if 'user_id' in request.session:
        # Clear session data
        request.session.flush()
        messages.success(request, "You have been logged out successfully.")
    else:
        messages.info(request, "You were not logged in.")
    return redirect('dashboard')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        sender = request.POST.get('email')

        # Save the enquiry in the database
        enquiry = Enquiry.objects.create(name=name, email=sender, subject=subject, message=message)

        # Full message for the admin
        full_message = f"""
        You have received a new message from {name} ({sender}) via the CampusHire placement portal:

        Subject: {subject}

        Message:
        {message}

        This enquiry was submitted on {enquiry.created_at}.
        """

        # Email to the website admin
        email = EmailMessage(
            subject=f"New Contact Message from {name}",
            body=full_message,
            from_email='your-email@gmail.com',  # Replace with your email
            to=['ganeshnagpure5402@gmail.com'],  # Admin's email address
        )

        # Confirmation email to the user
        confirmation_email = EmailMessage(
            subject="Thank You for Contacting Us - Zeal College Placement Portal",
            body=f"""
            Hi {name},

            Thank you for reaching out! We’ve received your message with the subject '{subject}'. Our placement team will get back to you soon.

            Best regards,
            Zeal College Placement Department
            """,
            from_email='your-email@gmail.com',  # Replace with your email
            to=[sender],
        )

        try:
            email.send()  # Send email to admin
            confirmation_email.send()  # Send confirmation email to user
            return HttpResponse("Your enquiry has been received. We will get back to you soon!")
        except Exception as e:
            print("Email send failed:", str(e))
            return HttpResponse(f"Failed to send email: {e}")

    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def privacy(request):
    return render(request, 'privacy.html')



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import FAQ, User  # Ensure you import your custom User model

def faq_list(request):
    faqs = FAQ.objects.filter(is_approved=True).order_by('-submitted_at')
    return render(request, 'faq_list.html', {'faqs': faqs})

def ask_question(request):
    # Custom login check
    user_id = request.session.get('user_id')  # Check if user_id exists in session
    if not user_id:
        messages.error(request, "You need to log in to ask a question.")
        return redirect('login')  # Redirect to your custom login view

    if request.method == 'POST':
        question = request.POST.get('question')
        if not question:
            messages.error(request, "Question cannot be empty.")
            return redirect('ask_question')

        # Fetch the logged-in user using user_id from the session
        try:
            user = User.objects.get(id=user_id)
            FAQ.objects.create(question=question, submitted_by=user)
            messages.success(request, "Your question has been submitted for review.")
            return redirect('ask_question')
        except User.DoesNotExist:
            messages.error(request, "User not found. Please log in again.")
            return redirect('login')
        

    return render(request, 'ask_question.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Profile, Education, Experience, ProfileSkillsCertifications, Certification
from django.core.files.storage import FileSystemStorage
def profile(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        messages.error(request, "You need to log in to view your profile.")
        return redirect('login')

    try:
        user = User.objects.get(id=user_id)
        profile, created = Profile.objects.get_or_create(user=user)
        profile_data, created = ProfileSkillsCertifications.objects.get_or_create(profile=profile)

        if request.method == "POST":
            # Update profile details
            profile.headline = request.POST.get("headline")
            profile.contact = request.POST.get("contact")
            profile.github = request.POST.get("github")
            profile.linkedin = request.POST.get("linkedin")
            profile.profile_pic = request.FILES.get("profile_pic") or profile.profile_pic
            profile.resume = request.FILES.get("resume") or profile.resume
            profile.street_address = request.POST.get("street_address")
            profile.city = request.POST.get("city")
            profile.state = request.POST.get("state")
            profile.zip_code = request.POST.get("zip_code")
            profile.country = request.POST.get("country")
            profile.enrollment =request.POST.get("enrollment")
            profile.dob = request.POST.get("dob")
            profile.save()

            # Clear and save other profile details
            Education.objects.filter(profile=profile).delete()
            Experience.objects.filter(profile=profile).delete()

            for level, college, degree in zip(
                request.POST.getlist("education_level[]"),
                request.POST.getlist("college[]"),
                request.POST.getlist("degree[]")
            ):
                if college and degree:
                    Education.objects.create(profile=profile, education_level=level, college=college, degree=degree)

            for company, role, start_date, end_date, role_type in zip(
                request.POST.getlist("company[]"),
                request.POST.getlist("role[]"),
                request.POST.getlist("start_date[]"),
                request.POST.getlist("end_date[]"),
                request.POST.getlist("role_type[]")
            ):
                if company and role:
                    Experience.objects.create(
                        profile=profile,
                        company=company,
                        role=role,
                        start_date=start_date,
                        end_date=end_date if end_date else None,
                        role_type=role_type
                    )

            # ✅ Store skills & certifications as lists instead of separate models
            profile_data.skills = request.POST.getlist("skills[]")
            # profile_data.certifications = request.POST.getlist("certifications[]")
            # profile_data.save()
            # Get certification names and uploaded files
            certification_names = request.POST.getlist("certifications[]")
            certification_files = request.FILES.getlist("certification_files[]")

            certifications_combined = []

            # Combine name and file
            for certification_name, file in zip(certification_names, certification_files):
                Certification.objects.create(profile=profile_data, certification_name=certification_name, file=file)
            profile_data.save()


            messages.success(request, "Profile updated successfully!")
            return redirect("profile")  # ✅ Redirect after POST

        # ✅ Handle GET request (Render the profile page)
        return render(request, "profile.html", {"user": user, "profile": profile, "profile_data": profile_data})

    except User.DoesNotExist:
        messages.error(request, "User not found. Please log in again.")
        return redirect('login')

from django.shortcuts import render, get_object_or_404

def profile_view(request):
    user_id = request.session.get('user_id')

    if not user_id:
        messages.error(request, "You need to log in to view the profile.")
        return redirect('login')

    try:
        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
        profile_data = ProfileSkillsCertifications.objects.get(profile=profile)
        certifications = Certification.objects.filter(profile=profile_data)
        education = Education.objects.filter(profile=profile)
        experience = Experience.objects.filter(profile=profile)

        return render(request, "profile_view.html", {
            "user": user,
            "profile": profile,
            "profile_data": profile_data,
            "certifications": certifications,
            "education": education,
            "experience": experience,
        })

    except (User.DoesNotExist, Profile.DoesNotExist, ProfileSkillsCertifications.DoesNotExist):
        messages.error(request, "Profile data not found.")
        return redirect('profile')  # fallback to edit page
from django.http import FileResponse, Http404
from .models import Certification 

def download_certificate(request, cert_id):
    try:
        cert = Certification.objects.get(id=cert_id)
        return FileResponse(cert.file.open(), as_attachment=True, filename=cert.file.name)
    except Certification.DoesNotExist:
        raise Http404("Certificate not found")
    
# def edit_profile(request):
#     user_id = request.session.get('user_id')
    
#     if not user_id:
#         messages.error(request, "You need to log in to view your profile.")
#         return redirect('login')

#     try:
#         user = User.objects.get(id=user_id)
#         profile, created = Profile.objects.get_or_create(user=user)
#         profile_data, created = ProfileSkillsCertifications.objects.get_or_create(profile=profile)
#         certifications = profile_data.certifications.all()

#         if request.method == "POST":
#             # Update profile details
#             profile.headline = request.POST.get("headline")
#             profile.contact = request.POST.get("contact")
#             profile.github = request.POST.get("github")
#             profile.linkedin = request.POST.get("linkedin")
#             profile.profile_pic = request.FILES.get("profile_pic") or profile.profile_pic
#             profile.resume = request.FILES.get("resume") or profile.resume
#             profile.street_address = request.POST.get("street_address")
#             profile.city = request.POST.get("city")
#             profile.state = request.POST.get("state")
#             profile.zip_code = request.POST.get("zip_code")
#             profile.country = request.POST.get("country")
#             profile.enrollment =request.POST.get("enrollment")
#             profile.dob = request.POST.get("dob")
#             profile.save()

#             # Clear and save other profile details
#             Education.objects.filter(profile=profile).delete()
#             Experience.objects.filter(profile=profile).delete()

#             for level, college, degree in zip(
#                 request.POST.getlist("education_level[]"),
#                 request.POST.getlist("college[]"),
#                 request.POST.getlist("degree[]")
#             ):
#                 if college and degree:
#                     Education.objects.create(profile=profile, education_level=level, college=college, degree=degree)

#             for company, role, start_date, end_date, role_type in zip(
#                 request.POST.getlist("company[]"),
#                 request.POST.getlist("role[]"),
#                 request.POST.getlist("start_date[]"),
#                 request.POST.getlist("end_date[]"),
#                 request.POST.getlist("role_type[]")
#             ):
#                 if company and role:
#                     Experience.objects.create(
#                         profile=profile,
#                         company=company,
#                         role=role,
#                         start_date=start_date,
#                         end_date=end_date if end_date else None,
#                         role_type=role_type
#                     )

#             # ✅ Store skills & certifications as lists instead of separate models
#             profile_data.skills = request.POST.getlist("skills[]")
#             # profile_data.certifications = request.POST.getlist("certifications[]")
#             # profile_data.save()
#             # Get certification names and uploaded files
#             certification_names = request.POST.getlist("certifications[]")
#             certification_files = request.FILES.getlist("certification_files[]")

#             certifications_combined = []

#             # Combine name and file
#             for certification_name, file in zip(certification_names, certification_files):
#                 Certification.objects.create(profile=profile_data, certification_name=certification_name, file=file)
#             profile_data.save()



#             messages.success(request, "Profile updated successfully!")
#             return redirect("profile")  # ✅ Redirect after POST

#         # ✅ Handle GET request (Render the profile page)
#         return render(request, "edit_profile.html", {"user": user, "profile": profile, "profile_data": profile_data, "certifications": certifications})

#     except User.DoesNotExist:
#         messages.error(request, "User not found. Please log in again.")
#         return redirect('login')

from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def edit_profile(request):
#     user_id = request.session.get('user_id')
    
#     if not user_id:
#         messages.error(request, "You need to log in to view your profile.")
#         return redirect('login')

#     try:
#         user = User.objects.get(id=user_id)
#         profile, created = Profile.objects.get_or_create(user=user)
#         profile_data, created = ProfileSkillsCertifications.objects.get_or_create(profile=profile)

#         if request.method == "POST":
#             # Update profile fields
#             profile.headline = request.POST.get("headline")
#             profile.contact = request.POST.get("contact")
#             profile.github = request.POST.get("github")
#             profile.linkedin = request.POST.get("linkedin")
#             profile.profile_pic = request.FILES.get("profile_pic") or profile.profile_pic
#             profile.resume = request.FILES.get("resume") or profile.resume
#             profile.street_address = request.POST.get("street_address")
#             profile.city = request.POST.get("city")
#             profile.state = request.POST.get("state")
#             profile.zip_code = request.POST.get("zip_code")
#             profile.country = request.POST.get("country")
#             profile.enrollment = request.POST.get("enrollment")
#             profile.dob = request.POST.get("dob")
#             profile.save()

#             # Clear and re-create education entries
#             Education.objects.filter(profile=profile).delete()
#             for level, college, degree in zip(
#                 request.POST.getlist("education_level[]"),
#                 request.POST.getlist("college[]"),
#                 request.POST.getlist("degree[]")
#             ):
#                 if college and degree:
#                     Education.objects.create(profile=profile, education_level=level, college=college, degree=degree)

#             # Clear and re-create experience entries
#             Experience.objects.filter(profile=profile).delete()
#             for company, role, start_date, end_date, role_type in zip(
#                 request.POST.getlist("company[]"),
#                 request.POST.getlist("role[]"),
#                 request.POST.getlist("start_date[]"),
#                 request.POST.getlist("end_date[]"),
#                 request.POST.getlist("role_type[]")
#             ):
#                 if company and role:
#                     Experience.objects.create(
#                         profile=profile,
#                         company=company,
#                         role=role,
#                         start_date=start_date,
#                         end_date=end_date if end_date else None,
#                         role_type=role_type
#                     )

#             # Update skills
#             profile_data.skills = request.POST.getlist("skills[]")
#             profile_data.save()

#             # Delete selected certifications
#             certs_to_delete = request.POST.getlist("delete_cert_ids[]")
#             if certs_to_delete:
#                 Certification.objects.filter(id__in=certs_to_delete).delete()

#             # Add new certifications
#             cert_names = request.POST.getlist("certifications[]")
#             cert_files = request.FILES.getlist("certification_files[]")
#             for name, file in zip(cert_names, cert_files):
#                 if name or file:
#                     Certification.objects.create(profile=profile_data, certification_name=name, file=file)

#             messages.success(request, "Profile updated successfully!")
#             return redirect("profile")

#         # GET request: show existing data
#         certifications = profile_data.certifications.all()
#         education_list = Education.objects.filter(profile=profile)
#         experience_list = Experience.objects.filter(profile=profile)

#         return render(request, "edit_pro.html", {
#             "user": user,
#             "profile": profile,
#             "profile_data": profile_data,
#             "certifications": certifications,
#             "education_list": education_list,
#             "experience_list": experience_list
#         })

#     except User.DoesNotExist:
#         messages.error(request, "User not found. Please log in again.")
#         return redirect('login')


from django.views.decorators.csrf import csrf_protect
from django.db import transaction
from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User, Profile, ProfileSkillsCertifications, Education, Experience, Certification

@csrf_protect
def edit_profile(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        messages.error(request, "You need to log in to view your profile.")
        return redirect('login')

    try:
        user = User.objects.get(id=user_id)
        profile, created = Profile.objects.get_or_create(user=user)
        profile_data, created = ProfileSkillsCertifications.objects.get_or_create(profile=profile)

        if request.method == "POST":
            with transaction.atomic():
                # Update profile fields
                profile.headline = request.POST.get("headline")
                profile.contact = request.POST.get("contact")
                profile.github = request.POST.get("github")
                profile.linkedin = request.POST.get("linkedin")
                profile.profile_pic = request.FILES.get("profile_pic") or profile.profile_pic
                profile.resume = request.FILES.get("resume") or profile.resume
                profile.street_address = request.POST.get("street_address")
                profile.city = request.POST.get("city")
                profile.state = request.POST.get("state")
                profile.zip_code = request.POST.get("zip_code")
                profile.country = request.POST.get("country")
                profile.enrollment = request.POST.get("enrollment")

                try:
                    profile.dob = datetime.strptime(request.POST.get("dob"), "%Y-%m-%d").date()
                except (ValueError, TypeError):
                    profile.dob = None

                profile.save()

                # Delete selected education records
                edu_delete_ids = request.POST.getlist("delete_edu_ids[]")
                if edu_delete_ids:
                    Education.objects.filter(id__in=edu_delete_ids, profile=profile).delete()

                # Recreate or update education entries
                Education.objects.filter(profile=profile).exclude(id__in=edu_delete_ids).delete()
                for level, college, degree in zip(
                    request.POST.getlist("education_level[]"),
                    request.POST.getlist("college[]"),
                    request.POST.getlist("degree[]")
                ):
                    if college and degree:
                        Education.objects.create(profile=profile, education_level=level, college=college, degree=degree)

                # Delete selected experience records
                exp_delete_ids = request.POST.getlist("delete_exp_ids[]")
                if exp_delete_ids:
                    Experience.objects.filter(id__in=exp_delete_ids, profile=profile).delete()

                # Recreate or update experience entries
                Experience.objects.filter(profile=profile).exclude(id__in=exp_delete_ids).delete()
                for company, role, start_date, end_date, role_type in zip(
                    request.POST.getlist("company[]"),
                    request.POST.getlist("role[]"),
                    request.POST.getlist("start_date[]"),
                    request.POST.getlist("end_date[]"),
                    request.POST.getlist("role_type[]")
                ):
                    if company and role:
                        Experience.objects.create(
                            profile=profile,
                            company=company,
                            role=role,
                            start_date=start_date or None,
                            end_date=end_date or None,
                            role_type=role_type
                        )

                # Update skills
                profile_data.skills = request.POST.getlist("skills[]")
                profile_data.save()

                # Delete selected certifications
                certs_to_delete = request.POST.getlist("delete_cert_ids[]")
                if certs_to_delete:
                    Certification.objects.filter(id__in=certs_to_delete).delete()

                # Add new certifications
                cert_names = request.POST.getlist("certifications[]")
                cert_files = request.FILES.getlist("certification_files[]")
                for name, file in zip(cert_names, cert_files):
                    if name and file:
                        Certification.objects.create(profile=profile_data, certification_name=name, file=file)

            messages.success(request, "Profile updated successfully!")
            return redirect("profile")

        # GET request: show existing data
        certifications = profile_data.certifications.all()
        education_list = Education.objects.filter(profile=profile)
        experience_list = Experience.objects.filter(profile=profile)

        return render(request, "edit_pro.html", {
            "user": user,
            "profile": profile,
            "profile_data": profile_data,
            "certifications": certifications,
            "education_list": education_list,
            "experience_list": experience_list
        })

    except User.DoesNotExist:
        messages.error(request, "User not found. Please log in again.")
        return redirect('login')

from django.shortcuts import get_object_or_404

def delete_certification(request, cert_id):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Login required.")
        return redirect('login')

    certification = get_object_or_404(Certification, id=cert_id, profile__profile__user_id=user_id)
    certification.delete()
    messages.success(request, "Certification deleted.")
    return redirect('edit_profile')


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User  # Make sure to import your custom User model

def change_password(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please log in to change your password.")
        return redirect('login')

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        try:
            user = User.objects.get(id=request.session['user_id'])

            if user.password != current_password:
                messages.error(request, "Current password is incorrect.")
            elif new_password != confirm_password:
                messages.error(request, "New passwords do not match.")
            else:
                user.password = new_password  # You might want to hash this in real apps
                user.save()
                messages.success(request, "Password changed successfully!")
                return redirect('dashboard')

        except User.DoesNotExist:
            messages.error(request, "User not found. Please log in again.")
            return redirect('login')

    return render(request, 'change_password.html')
