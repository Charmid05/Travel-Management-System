from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .forms import CreateUserForm, GuestForm
from .models import Guest
from tour.models import Destination, Airline, Hotel
from .decorators import unauthenticated_user, allowed_users
from .filters import GuestFilter

# Create your views here.

# @login_required
# def user_add_booking(request):
#     if request.method == 'POST':
#         form = UserAddBookingForm(request.POST)
#         if form.is_valid():
#             guest_booking = form.save(commit=False)
#             guest_booking.user_id = request.user  # Attach the logged-in user to the booking
#             guest_booking.save()
#             messages.success(request, 'Booking has been successfully added!')
#             return redirect('user-booking-list')  # Redirect to booking list or booking confirmation page
#     else:
#         form = UserAddBookingForm()
#     return render(request, 'user_add_booking.html', {'form': form})
# @login_required
# def user_booking_list(request):
#     bookings = Guest.objects.filter(user_id=request.user)
#     return render(request, 'user_booking_list.html', {'bookings': bookings})


@login_required(login_url=login)
# @allowed_users(allowed_roles=['admin'])
def add_staff(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'New staff added - \'' + username + '\'')
            return redirect('home')
    context = {'form': form}
    return render(request, 'ums/add_staff.html', context)


def register_page(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'New user registered: {username}')
            return redirect('home')  # Redirect to the home page after successful registration
    else:
        form = CreateUserForm()
    
    context = {'form': form}
    return render(request, 'ums/register.html', context)


# @unauthenticated_user
# def login_page(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.info(request, 'Username or Password is incorrect')

#     context = {}
#     return render(request, 'ums/login.html', context)


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_staff:  # If the user is admin, redirect to the admin home
                return redirect('home')  # Change this to the admin view
            else:
                return redirect('user-dashboard')  # Redirect to the user dashboard
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'ums/login.html', context)

# views.py
@login_required(login_url='login')
def user_dashboard(request):
    # Assuming you have a `Guest` model where each user has their own bookings.
    user_guests = Guest.objects.filter(user_id=request.user)

    context = {
        'user_guests': user_guests,
    }
    return render(request, 'ums/user_dashboard.html', context)



def logout_user(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin', 'staff'])  # Uncomment this line if you have role-based access decorators
def home(request):
    if not request.user.is_staff:
        return redirect('user-dashboard')  # Redirect regular users to their dashboard
    
    guest_count = Guest.objects.count()
    destination_count = Destination.objects.count()
    hotel_count = Hotel.objects.count()
    airline_count = Airline.objects.count()

    guests = Guest.objects.all()
    guestFilter = GuestFilter(request.GET, queryset=guests)
    guests = guestFilter.qs

    context = {
        'guest_count': guest_count,
        'destination_count': destination_count, 
        'hotel_count': hotel_count, 
        'airline_count': airline_count,
        'guests': guests,
        'guestFilter': guestFilter
    }
    return render(request, 'ums/dashboard.html', context)



# @login_required(login_url='login')
# # @allowed_users(allowed_roles=['admin', 'staff'])
# def guests(request):
#     guests = Guest.objects.all()
#     context = {'guests': guests}
#     return render(request, 'ums/guests.html', context)

@login_required(login_url='login')
def guests(request):
    # Get all guests
    guests = Guest.objects.all()


    guest_data = []
    for guest in guests:
        guest_info = {
            'guest': guest,
            'user_name': guest.user_id.username,  
            'phone_number': guest.user_id.phone,  
            'email': guest.user_id.email,
        }
        guest_data.append(guest_info)

    context = {
        'guest_data': guest_data
    }

    return render(request, 'ums/guests.html', context)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin', 'staff'])
def addGuest(request):
    form = GuestForm()
    if request.method == 'POST':
        form = GuestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('guests')
    context = {'form': form}
    return render(request, 'ums/add_guest.html', context)

from django.shortcuts import render, redirect
from .forms import GuestForm  # Assuming the form is called GuestForm

@login_required(login_url='login')
def CreateNewBooking(request):
    form = GuestForm()

    if request.method == 'POST':
        form = GuestForm(request.POST)
        if form.is_valid():
            # Associate the booking with the authenticated user
            guest_booking = form.save(commit=False)
            guest_booking.user = request.user  # Set the user field to the logged-in user
            guest_booking.save()

            # Redirect to the user dashboard after a successful booking creation
            return redirect('user-dashboard')

    context = {'form': form}
    return render(request, 'ums/create_booking.html', context)



@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin', 'staff'])
def updateGuest(request, id):
    guest = Guest.objects.get(id=id)
    form = GuestForm(instance=guest)
    if request.method == 'POST':
        form = GuestForm(request.POST, instance=guest)
        if form.is_valid():
            form.save()
            return redirect('guests')
    context = {'form': form}
    return render(request, 'tour/update_form.html', context)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin', 'staff'])
def deleteGuest(request, id):
    guest = Guest.objects.get(id=id)
    guest.delete()
    return redirect('guests')