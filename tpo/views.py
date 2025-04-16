from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .models import Tpo, Job
# Create your views here.
def tpo_dashboard(request):
    if "tpo_id" not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect("tpo_login")
    tpo = Tpo.objects.get(id=request.session["tpo_id"])

    return render(request, 'tpo_dashboard.html', { 'tpo': tpo })

def tpo_registration(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        employee_id = request.POST['employee_id']
        email = request.POST['email']
        mobile_number = request.POST['mobile']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Password matching check
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'registration.html', {
                'full_name': full_name,
                'employee_id': employee_id,
                'email': email,
                'mobile_number': mobile_number,
                
            })

        # Check if mobile number already exists
        if Tpo.objects.filter(employee_id=employee_id).exists():
            messages.error(request, "Employee id already registered.")
            return render(request, 'tpo_registration.html', {
                'full_name': full_name,
                'employee_id': employee_id,
                'email': email,
                'mobile_number': mobile_number,
                
            })

        # Hash password before storing
        hashed_password = make_password(password)

        # Create and save the vendor to the database
        tpo = Tpo(
            full_name=full_name,
            employee_id=employee_id,
            email=email,
            mobile_number=mobile_number,
        
            password=hashed_password
        )
        tpo.save()

        messages.success(request, "Registration successful! You can now log in.")
        return redirect('tpo_login')  # Redirect to login page after successful registration
    return render(request, 'tpo_registration.html')

def tpo_login(request):
    if request.method == "POST":
        employee_id = request.POST["employee_id"]
        password = request.POST["password"]

        try:
            tpo = Tpo.objects.get(employee_id=employee_id)

            if not tpo.is_approved:
                messages.error(request, "Your account is not approved by the admin.")
                return render(request, "tpo_login.html")
            
            if check_password(password, tpo.password):
                request.session["tpo_id"] = tpo.id
                print(tpo.id)
                request.session["tpo_name"] = tpo.full_name
                print(request.session["tpo_name"])
                messages.success(request, "Login successful.")
                return redirect("tpo_dashboard")  # Redirect vendors only

            else:
                messages.error(request, "Invalid password.")
                return render(request, "tpo_login.html")

        except Tpo.DoesNotExist:
            messages.error(request, "Tpo does not exist.")
            return render(request, "tpo_login.html")
    return render(request, 'tpo_login.html')

def tpo_logout(request):
    
    try:
        del request.session["tpo_id"]
        del request.session["tpo_name"]
        messages.success(request, "Logout successful.")
        return redirect('tpo_login')
    except KeyError:
        messages.error(request, "You are not logged in.")
        
        return redirect('tpo_login')

def tpo_update_profile(request):

    tpo = Tpo.objects.get(id=request.session.get('tpo_id'))  # assuming session holds vendor_id

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        employee_id = request.POST.get('employee_id')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        mobile = request.POST.get('mobile')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            tpo.full_name = full_name
            tpo.employee_id = employee_id
            tpo.email = email
            tpo.mobile_number = mobile
            tpo.password = password
            if password:
                tpo.password = make_password(password)
                tpo.save()
            messages.success(request, "Profile updated successfully.")
            request.session.update({"vendor_name": full_name})  # Update session name

    context = {
        'full_name': tpo.full_name,
        'employee_id': tpo.employee_id,
        'email': tpo.email,
        'mobile_number': tpo.mobile_number,
        
        
    }
    return render(request, 'tpo_account.html', context)


def add_job(request):
    if request.method == "POST":
        role = request.POST.get('role')
        company_name = request.POST.get('company_name')
        package = request.POST.get('salary')
        last_date = request.POST.get('last_date_to_apply')
        eligibility = request.POST.get('eligibility')
        job_description = request.POST.get('job_description')
        company_website = request.POST.get("company_website")
        job_location = request.POST.get("job_location")

        Job.objects.create(
            role=role,
            company=company_name,
            salary_package=package,
            last_date_to_apply=last_date,
            eligibility=eligibility,
            job_description=job_description,
            company_website=company_website,
            job_location=job_location
        )
        messages.success(request, "Job added successfully.")
        return redirect('add-job')  # or redirect to a success page

    return render(request, 'add_job.html')

def manage_job(request):

    tpo_id = request.session.get("tpo_id")

    if tpo_id is None:
        return redirect("tpo_login")  # Redirect if tpo is not logged in

    # Fetch food items belonging to the logged-in tpo
    Jobs = Job.objects.all()
    print("you are managing a job " ,Jobs)

    # for items in food_items :  # Debugging: Check if items exist in the terminal
    #     print(f'Name : {items}')
    return render(request, "manage_job.html", {"jobs": Jobs})

def update_job(request, id):
    Jobs = get_object_or_404(Job, id=id)
    print("you are updatating a job " ,id)
    
    if request.method == "POST":
        print("updatting a job")
        
        Jobs.company = request.POST["company_name"]
        Jobs.role = request.POST["role"]
        Jobs.salary_package = request.POST["salary_package"]
        Jobs.last_date_to_apply = request.POST["last_date_to_apply"]
        Jobs.eligibility = request.POST["eligibility"]
        Jobs.job_description = request.POST["job_description"]
        Jobs.company_website = request.POST["company_website"]
        Jobs.job_location = request.POST["job_location"]
        
        Jobs.save()
        messages.success(request, "Job updated successfully.")
        return redirect("manage-job")
    
    return render(request, "update_jobs.html", {"jobs": Jobs})
    
    

    


from django.shortcuts import get_object_or_404, redirect
def delete_job(request, job_id):
    
    # Jobs =  get_object_or_404(Job, id=Job_id)
    # print("you are deleting a job " ,Job_id)
    # Jobs.delete()
    messages.success(request, "Job deleted successfully.")
    return redirect("manage-job")
    