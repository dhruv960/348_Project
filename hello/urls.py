from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello_world, name = 'hello_world'),
    path('login/', views.login_page, name='login'),
    path('club-user/', views.club_user, name='club_user'),
    path('new-club/', views.new_club, name='new_club'),
    path('save-club/', views.save_club, name='save_club'),
    path('club-landing/', views.club_landing, name='club_landing'),
    path('validate-club/', views.validate_club, name='validate_club'),
    path('existing-club/', views.existing_club, name='existing_club'),
    path("club_landing/<int:club_id>/update_courts/", views.court_update, name="court_update"),
    path("update_court_submit/", views.update_court_submit, name="update_court_submit"),
    path('new-user/', views.new_user, name ='new_user'),
    path('save-user/', views.save_user, name='save_user'),
    path('user-landing/', views.user_landing, name='user_landing'),
    path('existing-user/', views.existing_user, name='existing_user'),
    path('validate-user/', views.validate_user, name='validate_user'),
    path("add-club/", views.add_club, name="add_club"),
    path("add-club-submit/", views.add_club_submit, name="add_club_submit"),
    path('make-booking/', views.club_booking_chooser, name='club_booking_chooser'),
    path('booking-details/', views.booking_details, name='booking_details'),
    path('submit-booking/', views.submit_booking, name='submit_booking'),
    path("user-monthly-report/", views.user_monthly_report, name="user_monthly_report"),
    path('club_report/', views.club_report, name='club_report'),
]

