import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Club,Users, Membership
from django.db import connection
# Create your views here.

def hello_world(request):
    return HttpResponse("Hello, World! -courtesy of Dhruv Jain")

def login_page(request):
    return render(request, 'hello/login.html')
def club_user(request):
    return render(request, 'hello/club_user.html')
def new_club(request):
    return render(request, 'hello/new_club.html')
def save_club(request):
    if request.method == "POST":
        club_name = request.POST.get("club_name")
        num_courts = request.POST.get("num_courts")

        if club_name and num_courts:  # Ensure both fields are filled
            club = Club(name=club_name, num_courts=int(num_courts))
            club.save()  # Save to database using ORM
            request.session['club_id']= club.club_id
            return redirect('club_landing')  # Redirect after saving
    return render(request, 'hello/new_club.html', {"error": "Please fill in all fields."})

def club_landing(request):
    club_id = request.session.get('club_id')  # Retrieve club_id
    if club_id:
        club = Club.objects.get(club_id=club_id)
        return render(request, 'hello/club_landing.html', {"club": club})
    else:
        return redirect('login_page')  # If no session, send user to login

def validate_club(request):
    if request.method == "POST":
        club_id = request.POST.get("club_id")

        # Check if club exists in the database
        try:
            club = Club.objects.get(club_id=club_id)
            request.session['club_id'] = club.club_id  # Store in session

            # Redirect to landing page
            return redirect('club_landing')
        except Club.DoesNotExist:
            return render(request, "hello/existing_club.html", {"error_message": "Invalid Club ID. Please try again."})

    return render(request, "hello/existing_club.html")

def existing_club(request):
    return render(request, 'hello/existing_club.html')
def court_update(request, club_id):
    return render(request, "hello/court_update.html", {"club_id": club_id})
def update_court_submit(request):
    if request.method == "POST":
        club_id = request.session.get("club_id")  # Retrieve club ID

        if not club_id:
            return redirect("existing_club")  # Redirect if session expired

        new_court_count = request.POST.get("num_courts")  # Get new number

        if new_court_count and new_court_count.isdigit():  # Validate input
            new_court_count = int(new_court_count)

            try:
                club = Club.objects.get(club_id=club_id)  # Fetch the club
                club.num_courts = new_court_count  # Update field
                club.save()  # Save to DB

                return redirect("club_landing")  # Redirect to landing page
            except Club.DoesNotExist:
                return redirect("existing_club")  # Handle invalid club ID

    return redirect("court_update") 

def new_user(request):
    return render(request, 'hello/new_user.html')

def save_user(request):
    if (request.method == "POST"):
        name = request.POST.get('name')
        age = int(request.POST.get('age'))
        interest_level = request.POST.get('interest')

        myUser = Users(name=name, age=age, interest_level=interest_level)
        myUser.save()
        request.session['user_id'] = myUser.user_id
        return redirect('user_landing') 
    else:
        return redirect('new_user')

def user_landing(request):
    user_id = request.session.get('user_id')  # Retrieve user_id
    if user_id:
        try:
            user = Users.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return redirect('login_page')  # Handle invalid ID case
        return render(request, 'hello/user_landing.html', {"user": user})
    else:
        return redirect('login_page')  # If no user_id in session

def existing_user(request):
    return render(request, 'hello/existing_user.html')

def validate_user(request):
    if (request.method == "POST"):
        user_id = request.POST.get("user_id")
        try: 
            user = Users.objects.get(user_id=user_id)
            request.session['user_id'] = user_id
            return redirect('user_landing')
        except Users.DoesNotExist:
            return redirect(existing_user)
def add_club(request):
    return render(request, 'hello/add_club.html')

def add_club_submit(request):
    if request.method == "POST":
        club_name = request.POST.get("club_name")
        user_id = request.session.get("user_id")
        
        try:
            club = Club.objects.get(name = club_name)
            myMember = Membership(user_id = user_id, club_id= club.club_id)
            myMember.save()
            request.session['success_message'] = "Successfully joined the club!"
        except Club.DoesNotExist:
            return render(request, "hello/add_club.html", {
                "error_message": "Club not found. Please try again."
            })
    return redirect('user_landing')
def club_booking_chooser(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")  # or wherever appropriate

    clubs = Club.objects.raw("""
        SELECT  c.club_id, c.name
        FROM Membership  m
        JOIN Club c ON m.club_id = c.club_id
        WHERE m.user_id = %s
    """, [user_id])

    return render(request, "hello/club_booking_chooser.html", {"clubs": clubs})  
def booking_details(request):
    if request.method == "POST":
        club_id = request.POST.get("club_id")
        request.session["selected_club_id"] = club_id  # Save it for final booking
        return render(request, "hello/booking_details.html", {"club_id": club_id})
    return redirect("club_booking_chooser")
def submit_booking(request):
    if request.method == "POST":
        # Retrieve data from the form submission
        user_id = request.session.get("user_id")
        club_id = request.session.get("selected_club_id")
        court_id = request.POST.get("court_id")
        datetime_str = request.POST.get("booking_datetime")  # Make sure to format this correctly (e.g., 'YYYY-MM-DD HH:MM:SS')
        print(court_id)
        print(club_id)
        # Call the stored procedure
        with connection.cursor() as cursor:
            cursor.callproc("make_booking", [user_id, club_id, court_id, datetime_str])
            result = cursor.fetchall()  # Get the result of the SELECT statement

        # The result should be a list with a tuple containing the message, e.g., [('Booking successful',)]
        message = result[0][0] if result else "Unknown error occurred"

        # Handle success or error based on the message
        if message == "Booking successful":
            return redirect('user_landing')  # Redirect to the user landing page
        else:
            return render(request, "hello/booking_details.html", {
                "error_message": message  # Show the error message to the user
            })
def user_monthly_report(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect('login')  # Or however you handle unauthorized access

    club_names = []
    booking_counts = []

    with connection.cursor() as cursor:
        cursor.callproc("get_monthly_user_club_bookings", [user_id])
        results = cursor.fetchall()  # [(club_name1, count1), (club_name2, count2), ...]

    for row in results:
        club_names.append(row[0])
        booking_counts.append(row[1])

    return render(request, 'hello/user_monthly_report.html', {
        "club_names": json.dumps(club_names),
        "booking_counts": json.dumps(booking_counts)
    })
def club_report(request):
    club_id = request.session.get('club_id')
    if not club_id:
        return redirect('login')  # fallback

    total_bookings = 0
    most_booked_court = None
    age_data = []
    interest_data = []
    age_labels = []
    interest_labels = []
    with connection.cursor() as cursor:
        cursor.callproc('get_club_report', [club_id])

        total_bookings = cursor.fetchone()[0]

        cursor.nextset()
        row = cursor.fetchone()
        most_booked_court = row[0] if row else "N/A"

        cursor.nextset()
        results = cursor.fetchall()
        for row in results:
            age_labels.append(row[0])
            age_data.append(row[1])


        cursor.nextset()
        results = cursor.fetchall()
        for row in results:
            interest_labels.append(row[0])
            interest_data.append(row[1])


    context = {
        'total_bookings': total_bookings,
        'most_booked_court': most_booked_court,
        'age_data': age_data,
        'interest_data': interest_data,
        'interest_labels': interest_labels,
        'age_labels': age_labels
    }
    print(context)
    return render(request, 'hello/club_report.html', context)





