
from django.urls import path
from. import views

urlpatterns = [
    path('',views.home,name="home"),
    path('register/',views.register,name="register"),
    path('user_login/', views.user_login,name='user_login'),
    path('contact/',views.contact,name='contact'),
    path('about/', views.about,name='about'),
    path('request_blood/', views.request_blood, name='request_blood'),
    path('find_donors/',views.find_donors,name='find_donors'),
    path('donate_form/', views.donate_form,name='donate_form'),
    path('know more/', views.uses,name='uses'),
    path('admin_login/',views.admin_login,name='admin_login'),
    path('donorpage/', views.donorpage, name='donorpage'),
    path('patientpage/',views.patientpage, name='patientpage'),
    path('adminpage/', views.adminpage, name='adminpage'),
    path('donate_blood/',views.donate_blood,name='donate_blood'),
    path('camps/',views.camps,name='camps'),
    path('availability/',views.availability,name='availability'),
    path('send-message/<int:id>',views.send_message,name='send_message'),
    path('login_view/',views.login_view,name='login_view'),
    path('logout/', views.user_logout, name='user_logout'),
    path('mydonations/',views.donations,name='donations'),
    path('donor_profile/',views.donor_profile,name='donor_profile'),
    path('patient_profile/',views.patient_profile,name='patient_profile'),
    path('admin_requests/',views.admin_requests,name='admin_requests'),
    path('donor_details/',views.donor_details,name='donor_details'),
    path('rewards/',views.rewards,name='rewards'),

    path('patient_details/',views.patient_details,name='patient_details'),
    path('appointment_approve/',views.appointments,name='appointments'),
    path('approve_donation/<int:id>/', views.approve_donation, name='approve_donation'),
    path('reject_donation/<int:id>/', views.reject_donation, name='reject_donation'),
    path('availability/',views.availability,name='availability'),
    path('patient_request/',views.patient_request,name='patient_request'),
    path('admin_reports/',views.admin_reports,name='admin_reports'),
    path('approve_request/<int:id>/', views.approve_request, name='approve_request'),
    path('donor_notification/',views.donor_notification,name='donor_notification'),
    path('mark_as_read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('delete_notification/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('mark_all_read/', views.mark_as_read, name='mark_all_read'),
    path('reject_request/<int:id>/',views.reject_request,name='reject_request'),
    path('donor_requests/',views.donor_requests,name='donor_requests'),
    path('bloodcamps/',views.blood_camps,name='blood_camps'),
    path('updatecamp/<int:id>/',views.edit_camp,name='edit_camp'),
    path('register_camps/',views.register_camp,name='register_camp'),
    path('deletecamp/<int:id>/',views.delete_camp,name='delete_camp'),
    path('blood_banks/',views.blood_banks,name='blood_banks'),
    path('delete_blood_bank/',views.delete_blood_bank,name='delete_blood_bank'),
    path('edit_donor_profile/', views.edit_donor_profile, name='edit_donor_profile'),
    path('patient_blood_banks/',views.patient_blood_banks,name='patient_blood_banks'),
    path('patient_notifications/',views.patient_notifications,name='patient_notifications'),
    path('mark_as_read_patient/',views.mark_as_read_patient,name='mark_as_read_patient'),
    path('edit_patient_profile/',views.edit_patient_profile,name='edit_patient_profile'),
    path('delete_notification_patient/<int:id>/', views.delete_notification_patient, name='delete_notification_patient'),
        # Admin notifications page
    path('admin-notifications/', views.admin_notifications, name='admin_notifications'),

    # Mark single notification as read
    path('admin-notification/read/<int:id>/', views.mark_admin_notification_read, name='mark_admin_notification_read'),

    # Delete notification
    path('admin-notification/delete/<int:id>/', views.delete_admin_notification, name='delete_admin_notification')
]
