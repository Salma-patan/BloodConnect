from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, date

from .models import (
    Registration,
    Contact,
    donateblood,
    patientrequest,
    PatientNotification,
    AdminNotification,
    Camp,
    Notification,
    CampRegistration
)


# =====================================
# HOME
# =====================================
def home(request):
    return render(request, 'home.html')


# =====================================
# LOGIN
# =====================================
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Registration

def user_login(request):

    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')
        person = request.POST.get('person')

        try:
            user = Registration.objects.get(
                email=email,
                person=person
            )

            if check_password(password, user.password):

                # Common session
                request.session['user_id'] = user.id
                request.session['person'] = user.person

                # Role-wise session
                if user.person == "Donor":
                    request.session['donor_id'] = user.id
                    return redirect('donorpage')

                elif user.person == "Patient":
                    request.session['patient_id'] = user.id
                    return redirect('patientpage')

                else:
                    messages.error(request, "Invalid Role")
                    return redirect('login_view')

            else:
                messages.error(request, "Invalid Password")
                return redirect('login_view')

        except Registration.DoesNotExist:
            messages.error(request, "Email not registered")
            return redirect('login_view')

    return render(request, 'user_login.html')
 
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from datetime import datetime, date
from .models import Registration

def register(request):

    if request.method == "POST":

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        pincode = request.POST.get('pincode')
        country = request.POST.get('country')
        state = request.POST.get('state')
        district = request.POST.get('district')
        city_town = request.POST.get('city_town')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        bloodgroup = request.POST.get('bloodgroup')
        person = request.POST.get('person')
        password = request.POST.get('password')

        # Donor age validation
        if person == "Donor":

            birth_date = datetime.strptime(
                dob,
                "%Y-%m-%d"
            ).date()

            today = date.today()

            age = today.year - birth_date.year - (
                (today.month, today.day) <
                (birth_date.month, birth_date.day)
            )

            if age < 18:
                messages.error(
                    request,
                    "Donors must be 18 years or older."
                )
                return redirect('register')

        # Check Registration table
        if Registration.objects.filter(email=email).exists():

            messages.error(
                request,
                "Email already registered."
            )

            return redirect('register')


        # Create Registration record
        Registration.objects.create(
            first_name=first_name,
            last_name=last_name,
            dob=dob,
            gender=gender,
            pincode=pincode,
            country=country,
            state=state,
            district=district,
            city_town=city_town,
            email=email,
            phone=phone,
            bloodgroup=bloodgroup,
            person=person,
            password=make_password(password),  # IMPORTANT
        )

        messages.success(
            request,
            "Registered Successfully"
        )

        return redirect('login_view')

    return render(
        request,
        'authentication/register.html'
    )

#donate blood
def donate_blood(request):
    return render(request, 'donateblood.html')

#request blood
def request_blood(request):
    return render(request,'request_blood.html')
# =====================================
# LOGOUT
# =====================================
def user_logout(request):

    request.session.flush()

    return redirect('login_view')


# =====================================
# CONTACT
# =====================================
def contact(request):

    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        Message = request.POST.get('Message')

        Contact.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            Message=Message
        )

        subject = f"New Contact Message from {first_name}"

        message_body = f"""
        Name: {first_name} {last_name}
        Email: {email}
        Message: {Message}
        """

        send_mail(
            subject,
            message_body,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        messages.success(request, "Message Sent Successfully")

        return redirect('contact')

    return render(request, 'contactus/contact.html')


# =====================================
# ABOUT
# =====================================
def about(request):
    return render(request, 'about/about.html')


# =====================================
# REQUEST BLOOD
# =====================================
def request_blood(request):
    return render(request, 'request_blood.html')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Registration, donateblood

def donate_form(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login_view')

    donor = get_object_or_404(
        Registration,
        id=user_id,
        person='Donor'
    )

    if request.method == "POST":

        donateblood.objects.create(
            first_name=donor.first_name,
            last_name=donor.last_name,
            email=donor.email,
            bloodgroup=donor.bloodgroup,
            phone=donor.phone,
            date=request.POST.get('date'),
            country=donor.country,
            state=donor.state,
            district=donor.district,
            city_town=donor.city_town,
            units=request.POST.get('units')
        )

        messages.success(
            request,
            "Blood donation submitted successfully!"
        )

        return redirect('donations')

    return render(request, 'donate_form.html', {
        'donor': donor
    })

# =====================================
# KNOW MORE
# =====================================
def uses(request):
    return render(request, 'know_more.html')


# =====================================
# DONOR DASHBOARD
# =====================================
def donorpage(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login_view')

    donor = get_object_or_404(
        Registration,
        id=user_id,
        person='Donor'
    )

    camps = Camp.objects.all()

    requests_count = patientrequest.objects.filter(
        donor=donor
    ).count()

    unread_notifications = Notification.objects.filter(
        donor=donor,
        is_read=False
    ).count()

    return render(request, 'donor_dashboard.html', {
        'donor': donor,
        'camps': camps,
        'requests_count': requests_count,
        'total_donations': donor.count,
        'last_donation': donor.last_donation,
        'unread_notifications': unread_notifications,
    })


# =====================================
# PATIENT DASHBOARD
# =====================================
def patientpage(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login_view')

    patient = get_object_or_404(
        Registration,
        id=user_id,
        person='Patient'
    )

    recent_requests = patientrequest.objects.filter(
        patient_name=patient.first_name
    ).order_by('-date')[:5]

    return render(request, 'patient_dashboard.html', {
        'patient': patient,
        'recent_requests': recent_requests
    })
#admin Dashboard
def adminpage(request):

    donor = Registration.objects.filter(person='Donor')
    patient = Registration.objects.filter(person='Patient')

    # TOTAL DONATION REQUESTS GIVEN BY DONORS
    blood_requests = donateblood.objects.all()

    # RECENT DONATIONS
    donations = donateblood.objects.all().order_by('-id')[:5]

    # CAMPS
    camps = Camp.objects.all().order_by('date', 'time')[:5]

    context = {

        'donor': donor,
        'patient': patient,
        'blood_requests': blood_requests,
        'donations': donations,
        'camps': camps,

    }

    return render(request,
                  'admin_dashboard.html',
                  context)

# =====================================
# DONATIONS PAGE
# =====================================
from django.shortcuts import render, redirect, get_object_or_404
from .models import Registration, donateblood

def donations(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login_view')

    donor = get_object_or_404(
        Registration,
        id=user_id,
        person='Donor'
    )

    donations = donateblood.objects.filter(
        email=donor.email
    ).order_by('-date')

    return render(request, 'mydonations.html', {
        'donor': donor,
        'donations': donations
    })

# =====================================
# DONOR PROFILE
# =====================================
def donor_profile(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login_view')

    donor = Registration.objects.get(id=user_id)

    return render(request, 'donor_profile.html', {
        'donor': donor
    })

#patient profile
def patient_profile(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login_view')

    patient = Registration.objects.get(id=user_id)

    return render(request, 'patient_profile.html', {
        'patient': patient
    })
# =====================================
# ADMIN REQUESTS
# =====================================
def admin_requests(request):

    data = donateblood.objects.all()

    return render(request, 'admin_requests.html', {
        'data': data
    })


# =====================================
# APPROVE DONATION
# =====================================
def approve_donation(request, id):

    donor = donateblood.objects.get(id=id)

    donor.status = "Approved"

    donor.save()

    return redirect('admin_requests')


# =====================================
# REJECT DONATION
# =====================================
def reject_donation(request, id):

    donor = donateblood.objects.get(id=id)

    donor.status = "Rejected"

    donor.save()

    return redirect('admin_requests')


# =====================================
# DONOR DETAILS
# =====================================
def donor_details(request):

    donor = Registration.objects.filter(person="Donor")

    return render(request, 'donor_details.html', {
        'donor': donor
    })


# =====================================
# PATIENT DETAILS
# =====================================
def patient_details(request):

    patient = Registration.objects.filter(person='Patient')

    return render(request, 'patient_details.html', {
        'patient': patient
    })


# =====================================
# APPOINTMENTS
# =====================================
def appointments(request):
    return render(request, 'appointment_approve.html')


# =====================================
# BLOOD AVAILABILITY
# =====================================
def availability(request):

    bloodgroup = request.GET.get('bloodgroup')
    district = request.GET.get('district')

    donors = donateblood.objects.filter(status='Approved')

    if bloodgroup:
        donors = donors.filter(bloodgroup__icontains=bloodgroup)

    if district:
        donors = donors.filter(district__icontains=district)

    return render(request, 'blood_availability.html', {
        'donors': donors
    })
#send_message
def send_message(request, id):

    donor = Registration.objects.get(id=id)

    return render(request,
                  'send_message.html',
                  {
                      'donor': donor
                  })


# =====================================
# PATIENT REQUEST
# =====================================
from django.shortcuts import render, redirect
from django.contrib import messages
def patient_request(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login_view')

    patient = Registration.objects.get(id=user_id)

    donors = Registration.objects.filter(person="Donor")

    total_requests = patientrequest.objects.filter(
        patient_name=patient.first_name
    ).count()

    if request.method == "POST":

        patient_name = patient.first_name

        donor_id = request.POST.get('donor_id')
        bloodgroup = request.POST.get('bloodgroup')
        message = request.POST.get('message')

        donor = Registration.objects.get(id=donor_id)
        patientrequest.objects.create(
            patient_name=patient.first_name,
            donor=donor,
            donor_email=donor.email,   # TEMP FIX
            bloodgroup=bloodgroup,
            message=message
)
        Notification.objects.create(
            donor=donor,
            message=f"New Blood Request From {patient_name}",
            notification_type="Request"
        )

        return redirect('patient_request')

    requests = patientrequest.objects.all().order_by('-date')

    return render(request, 'patient_requests.html', {
        'donors': donors,
        'requests': requests,
        'total_requests': total_requests
    })
from django.shortcuts import get_object_or_404, redirect
from .models import patientrequest, Notification

# ===============================
# APPROVE REQUEST
# ===============================
def approve_request(request, id):

    req = get_object_or_404(patientrequest, id=id)

    req.status = "Accepted"
    req.save()

    # send notification to donor
    Notification.objects.create(
        donor=req.donor,
        message=f"Your blood request for {req.bloodgroup} has been ACCEPTED.",
        notification_type="request"
    )

    return redirect('donor_requests')


# ===============================
# REJECT REQUEST
# ===============================
def reject_request(request, id):

    req = get_object_or_404(patientrequest, id=id)

    req.status = "Rejected"
    req.save()

    # send notification to donor
    Notification.objects.create(
        donor=req.donor,
        message=f"Your blood request for {req.bloodgroup} has been REJECTED.",
        notification_type="request"
    )

    return redirect('donor_requests')


# =====================================
# DONOR REQUESTS
# =====================================
def donor_requests(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login_view')

    donor = Registration.objects.get(id=user_id)

    requests = patientrequest.objects.filter(
        donor=donor
    ).order_by('-date')

    return render(request, 'donor_requests.html', {
        'requests': requests
    })


# =====================================
# LOGIN VIEW
# =====================================
def login_view(request):
    return render(request, 'authentication/login.html')


# =====================================
# ADMIN LOGIN
# =====================================
def admin_login(request):

    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')

        if email == 'admin@gmail.com' and password == 'admin@123':
            return redirect('adminpage')

        elif email == 'camps@gmail.com' and password == 'camps@123':
            return redirect('blood_camps')

        else:
            messages.error(request, 'Enter Correct Details')

    return render(request, 'authentication/admin_login.html')


# =====================================
# BLOOD CAMPS ADMIN
# =====================================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import date

from .models import Camp, CampRegistration


# =====================================
# CAMP ADMIN PAGE
# =====================================
def blood_camps(request):

    # ADD NEW CAMP
    if request.method == "POST":

        camp_name = request.POST.get('camp_name')
        location = request.POST.get('location')
        date_value = request.POST.get('date')
        time = request.POST.get('time')
        contact = request.POST.get('contact')

        Camp.objects.create(

            camp_name=camp_name,
            location=location,
            date=date_value,
            time=time,
            contact=contact

        )

        messages.success(request, "Camp Added Successfully")

        return redirect('blood_camps')

    # SHOW CAMPS
    camps = Camp.objects.all().order_by('date', 'time')

    # REGISTRATIONS
    registrations = CampRegistration.objects.all().order_by('-id')

    return render(request,
                  'blood_camps/upcoming_bloodcamps.html',
                  {

                      'camps': camps,
                      'registrations': registrations

                  })


# =====================================
# USER SIDE - FIND CAMPS
# =====================================
def camps(request):

    camps = Camp.objects.filter(
        date__gte=date.today()
    ).order_by('date', 'time')

    location = request.GET.get('location')
    date_filter = request.GET.get('date')

    if location:
        camps = camps.filter(location__icontains=location)

    if date_filter:
        camps = camps.filter(date=date_filter)

    return render(request,
                  'find_camps.html',
                  {

                      'camps': camps

                  })


# =====================================
# DELETE CAMP
# =====================================
def delete_camp(request, id):

    camp = get_object_or_404(Camp, id=id)

    camp.delete()

    messages.success(request,
                     "Camp Deleted Successfully")

    return redirect('blood_camps')


# =====================================
# EDIT CAMP
# =====================================
def edit_camp(request, id):

    camp = get_object_or_404(Camp, id=id)

    if request.method == "POST":

        camp.camp_name = request.POST.get('camp_name')
        camp.location = request.POST.get('location')
        camp.date = request.POST.get('date')
        camp.time = request.POST.get('time')
        camp.contact = request.POST.get('contact')

        camp.save()

        messages.success(request,
                         "Camp Updated Successfully")

        return redirect('blood_camps')

    return render(request,
                  'blood_camps/update_camp.html',
                  {

                      'camp': camp

                  })
# =====================================
# REWARDS
# =====================================
def rewards(request):
    return render(request, 'rewards.html')


# =====================================
# DONOR NOTIFICATIONS
# =====================================
def donor_notification(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login_view')

    donor = get_object_or_404(
        Registration,
        id=user_id,
        person='Donor'
    )

    notifications = Notification.objects.filter(
        donor=donor
    ).order_by('-created_at')

    unread_count = notifications.filter(
        is_read=False
    ).count()

    return render(request, 'donor_notifications.html', {

        'donor': donor,
        'notifications': notifications,
        'unread_count': unread_count

    })


# =====================================
# MARK AS READ
# =====================================
def mark_as_read(request, notification_id):

    notification = get_object_or_404(
        Notification,
        id=notification_id
    )

    notification.is_read = True

    notification.save()

    return redirect('donor_notification')


# =====================================
# MARK ALL AS READ
# =====================================
def mark_as_read(request, notification_id):

    donor_id = request.session.get('donor_id')

    if not donor_id:
        return redirect('login_view')

    try:
        donor = Registration.objects.get(id=donor_id, person='Donor')
    except Registration.DoesNotExist:
        request.session.flush()
        return redirect('login_view')

    notification = get_object_or_404(Notification, id=notification_id)

    # 🔥 SECURITY CHECK
    if notification.donor_id != donor.id:
        return redirect('donor_notification')

    notification.is_read = True
    notification.save()

    return redirect('donor_notification')


# =====================================
# DELETE NOTIFICATION
# =====================================
def delete_notification(request, notification_id):

    notification = get_object_or_404(
        Notification,
        id=notification_id
    )

    notification.delete()

    return redirect('donor_notification')


# =====================================
# REGISTER CAMP
# =====================================
def register_camp(request):

    donor = get_object_or_404(
        Registration,
        id=request.session.get('donor_id'),
        person='Donor'
    )

    if request.method == "POST":

        CampRegistration.objects.create(

            donor=donor,
            camp_name=request.POST.get('camp_name'),
            location=request.POST.get('location'),
            date=request.POST.get('date'),
            time=request.POST.get('time'),
            phone=request.POST.get('phone'),
            bloodgroup=request.POST.get('bloodgroup'),

        )

        Notification.objects.create(
            donor=donor,
            message="Camp Registered Successfully",
            notification_type="Camp"
        )

        messages.success(request, "Camp Registered Successfully")

        return redirect('donorpage')

    return render(request,
                  'donor_camps_register.html',
                  {'donor': donor})

#find_donors
def find_donors(request):
    bloodgroup = request.GET.get('bloodgroup')

    donors = donateblood.objects.filter(status="Approved")

    if bloodgroup:
        donors = donors.filter(bloodgroup=bloodgroup)

    return render(request, 'find_donors.html', {'donors': donors})


#blood banks
from .models import BloodBank
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404


# =====================================
# ADMIN BLOOD BANK PAGE
# =====================================
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import BloodBank


# =====================================
# ADMIN BLOOD BANK PAGE
# =====================================
def blood_banks(request):

    # ADD BLOOD BANK
    if request.method == "POST":

        bank_name = request.POST.get('bank_name')

        location = request.POST.get('location')

        contact = request.POST.get('contact')

        bloodgroup = request.POST.get('bloodgroup')

        units_available = request.POST.get('units_available')

        BloodBank.objects.create(

            bank_name=bank_name,
            location=location,
            contact=contact,
            bloodgroup=bloodgroup,
            units_available=units_available

        )

        messages.success(request,
                         "Blood Bank Added Successfully")

        return redirect('blood_banks')

    # FETCH ALL BLOOD BANKS
    banks = BloodBank.objects.all().order_by('-id')

    return render(request,
                  'blood_banks/blood_banks.html',
                  {

                      'banks': banks

                  })


# =====================================
# DELETE BLOOD BANK
# =====================================
def delete_blood_bank(request, id):

    bank = get_object_or_404(BloodBank,
                             id=id)

    bank.delete()

    messages.success(request,
                     "Blood Bank Deleted Successfully")

    return redirect('blood_banks')


# =====================================
# PATIENT BLOOD BANKS PAGE
# =====================================
def patient_blood_banks(request):

    banks = BloodBank.objects.all().order_by('-id')

    # SEARCH BY BLOOD GROUP
    bloodgroup = request.GET.get('bloodgroup')

    if bloodgroup:

        banks = banks.filter(
            bloodgroup=bloodgroup
        )

    return render(request,
                  'patient_blood_banks.html',
                  {

                      'banks': banks

                  })

#reports
from django.shortcuts import render
from .models import donateblood, patientrequest


def admin_reports(request):

    total_donors = donateblood.objects.count()

    total_patients = patientrequest.objects.count()

    approved = patientrequest.objects.filter(
        status='Approved'
    ).count()

    pending = patientrequest.objects.filter(
        status='Pending'
    ).count()

    rejected = patientrequest.objects.filter(
        status='Rejected'
    ).count()

    context = {

        'total_donors': total_donors,
        'total_patients': total_patients,
        'approved': approved,
        'pending': pending,
        'rejected': rejected,

    }

    return render(request,'reports.html',context
    )

#patient notification view
from .models import Notification, Registration

def patient_notifications(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login_view')

    patient = Registration.objects.get(id=user_id)
    notifications = PatientNotification.objects.filter(
        patient=patient
    ).order_by('-created_at')

    unread_count = notifications.filter(is_read=False).count()

    return render(request, 'patient_notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })

#mark as read for patient 
def mark_as_read_patient(request, id):

    notification = PatientNotification.objects.get(id=id)

    notification.is_read = True
    notification.save()

    return redirect('patient_notifications')

#delete notification
def delete_notification_patient(request, id):

    notification = PatientNotification.objects.get(id=id)
    notification.delete()

    return redirect('patient_notifications')

#edit profile patient
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Registration

def edit_patient_profile(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login_view')

    patient = Registration.objects.get(id=user_id)

    if request.method == "POST":

        patient.first_name = request.POST.get('first_name')
        patient.last_name = request.POST.get('last_name')
        patient.phone = request.POST.get('phone')
        patient.gender = request.POST.get('gender')
        patient.country = request.POST.get('country')
        patient.state = request.POST.get('state')
        patient.district = request.POST.get('district')
        patient.city_town = request.POST.get('city_town')
        patient.pincode = request.POST.get('pincode')
        patient.bloodgroup = request.POST.get('bloodgroup')
        patient.dob = request.POST.get('dob')

        patient.save()

        messages.success(request, "Profile Updated Successfully")
        return redirect('patient_profile')

    return render(request, 'edit_patient_profile.html', {
        'patient': patient
    })


#edit profile donor
def edit_donor_profile(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login_view')

    donor = Registration.objects.get(id=user_id)

    if request.method == "POST":

        donor.first_name = request.POST.get('first_name')
        donor.last_name = request.POST.get('last_name')
        donor.phone = request.POST.get('phone')
        donor.gender = request.POST.get('gender')
        donor.country = request.POST.get('country')
        donor.state = request.POST.get('state')
        donor.district = request.POST.get('district')
        donor.city_town = request.POST.get('city_town')
        donor.pincode = request.POST.get('pincode')
        donor.bloodgroup = request.POST.get('bloodgroup')
        donor.dob = request.POST.get('dob')

        donor.save()

        return redirect('donor_profile')

    return render(request, 'edit_donor_profile.html', {
        'donor': donor
    })

#admin notification
def admin_notifications(request):

    notifications = AdminNotification.objects.all().order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()

    return render(request, 'admin_notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })

#mark admin notification
def mark_admin_notification_read(request, id):

    notif = AdminNotification.objects.get(id=id)
    notif.is_read = True
    notif.save()

    return redirect('admin_notifications')

#delete admin notification
def delete_admin_notification(request, id):

    notif = AdminNotification.objects.get(id=id)
    notif.delete()

    return redirect('admin_notifications')