from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.conf import settings
from .models import House, BookingRequest, HelpDeskModel
from HouseRentManagementApp.models import UserProfile, OTP
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def AllUser(request):
    u = UserProfile.objects.filter(verified=True).exclude(user=request.user)
    if request.method == "POST":
        search = request.POST.get("search")
        u = UserProfile.objects.filter(user__first_name__icontains=search, verified=True).exclude(user=request.user)
    page = request.GET.get('page', 1)

    paginator = Paginator(u, 10)
    try:
        u = paginator.page(page)
    except PageNotAnInteger:
        u = paginator.page(1)
    except EmptyPage:
        u = paginator.page(paginator.num_pages)
    return render(request, 'all-user.html', {'user':u})


def AddAdmin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        DOB = request.POST.get('dob')
        profile_pic = request.FILES.get('pic')
        gender=request.POST.get('gender')
        address= request.POST.get('address')
        
        if pass1!=pass2:
            msg='Password should be same.'
            return render(request,'add-admin.html',{'msg':msg})
        if len(contact)!=10:
            msg='Contact should be 10 digit.'
            return render(request,'add-admin.html',{'msg':msg})
        try:
            user=User.objects.create_user(
                username=username,
                email=email,
                password=pass1,
                first_name=first_name,
                last_name=last_name
                )
        except:
            msg='Usename already exist.'
            return render(request,'add-admin.html',{'msg':msg})
        UserProfile.objects.create(
            user=user,
            profilePicture=profile_pic,
            contact_No=contact,
            address=address,
            gender=gender,
            DOB=DOB,
            userType="Admin"
            )
        return redirect('all-user')
    return render(request, 'add-admin.html')


def Profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request,'profile.html')


def ViewUser(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    u = UserProfile.objects.get(id=id)

    return render(request, 'view-user.html',{'user':u})


def DeleteUser(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    u = User.objects.get(id=id)
    u.delete()
    return redirect('all-user')


def ApproveOwnerRequest(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    u = UserProfile.objects.get(id=id)
    u.verified = True
    u.save()
    return redirect('approve-owner')



def EditProfile(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    u = UserProfile.objects.get(id=id)
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        pic = request.FILES.get('pic')
        contact = request.POST.get('contact')

        if len(contact)!=10:
            msg = "Contact number should be 10 digit"
            return render(request,'edit-profile.html', {'details':u, 'msg':msg})
        
        if pic:
            u.profilePicture = pic
        u.DOB = dob
        u.address = address
        u.gender = gender
        u.contact_No = contact

        u.user.email = email
        u.user.first_name = first_name
        u.user.last_name = last_name
        u.user.save()
        u.save()
        return redirect('profile')
    return render(request,'edit-profile.html', {'details':u})



def ChangePassword(request):
    if not request.user.is_authenticated:
        return redirect('login')
    msg = ''
    if request.method == "POST":
        username = request.user.username
        oldpass = request.POST.get('oldpass')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1!=password2:
            msg='New and Confirm Password should be same.'
            return render(request,'changepass.html', {'msg':msg})
              
        user = User.objects.get(username=username)
        newpass = user.check_password(oldpass)
        
        if newpass:
            user.set_password(password1)
            user.save()
            data=authenticate(username=username,password=password1)
            if data !=None:
                login(request,data)
                return redirect('profile')
        msg='Old Password should be same.'
    return render(request,'changepass.html', {'msg':msg})


def MyHouse(request):
    if not request.user.is_authenticated:
        return redirect('login')
    h = House.objects.filter(user=UserProfile.objects.get(user=request.user))
    return render(request, 'my-house.html',{'houses':h})
# def Location(request,location):
#     return render(request, 'see-location.html')
def Location(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    h = House.objects.get(id=id)
    # house = get_object_or_404(House, location=location)  # Retrieve house by location
    return render(request, 'see-location.html', {'house': h})

def RentHouse(request):
    if not request.user.is_authenticated:
        return redirect('login')
    u = UserProfile.objects.get(user=request.user)
    if u.userType == "Owner":
        h = House.objects.filter(user=UserProfile.objects.get(user=request.user))
    else:
        h = House.objects.filter(status='Available')
    if request.method == "POST":
        search = request.POST.get('search')
        
        if u.userType == "Public":
            h = House.objects.filter(status='Available', city__icontains=search)
        elif u.userType == "Owner":
            h = House.objects.filter(user=UserProfile.objects.get(user=request.user), city__icontains=search)
        else:
            h = House.objects.filter(status='Available', city__icontains=search)
    page = request.GET.get('page', 1)

    paginator = Paginator(h, 10)
    try:
        h = paginator.page(page)
    except PageNotAnInteger:
        h = paginator.page(1)
    except EmptyPage:
        h = paginator.page(paginator.num_pages)
    return render(request, 'rent-house.html',{'houses':h})


def AddHouse(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        house_no = request.POST.get('house_no')
        room_size = request.POST.get('room_size')
        area = request.POST.get('area')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        location = request.POST.get('location')
        price = request.POST.get('price')
        state = request.POST.get('state')

        House.objects.create(
            user = UserProfile.objects.get(user=request.user),
            house_no = house_no,
            room_size = room_size,
            area = area,
            city = city,
            pincode = pincode,
            image1 = image1,
            image2 = image2,
            location = location,
            price = price,
            state = state
        )
        return redirect('rent-house')
    return render(request, 'add-house.html')


def EditHouse(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    h = House.objects.get(id=id)
    if request.method == "POST":
        house_no = request.POST.get('house_no')
        room_size = request.POST.get('room_size')
        area = request.POST.get('area')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        location = request.POST.get('location')
        price = request.POST.get('price')
        state = request.POST.get('state')

        if image1:
            h.image1 = image1
        if image2:
            h.image2 = image2
        
        h.house_no = house_no
        h.room_size = room_size
        h.area = area
        h.city = city
        h.pincode = pincode
        h.location = location
        h.price = price
        h.state = state
        h.save()
        return redirect('rent-house')
    return render(request, 'edit-house.html', {'house':h})


def ViewHouse(request,id):
    if not request.user.is_authenticated:
        return redirect('login')
    h = House.objects.get(id=id)
    return render(request, 'view-house.html',{'house_details':h})


def MyBooking(request):
    if not request.user.is_authenticated:
        return redirect('login')
    booking = BookingRequest.objects.filter(user=UserProfile.objects.get(user=request.user))
    return render(request, 'public-book-status.html',{'booking':booking})


def CustomerRequest(request):
    if not request.user.is_authenticated:
        return redirect('login')
    booking = BookingRequest.objects.filter(house__user=UserProfile.objects.get(user=request.user), status="Pending")
    return render(request, 'customer-request.html',{'requests':booking})


def ApprovedCustomer(request):
    booking = BookingRequest.objects.filter(house__user=UserProfile.objects.get(user=request.user), status="Accepted")
    return render(request, 'approved-customers.html',{'requests':booking})


def ApproveCustomerRequest(request, id):
    c = BookingRequest.objects.get(id=id)
    c.status = "Accepted"
    c.save()
    return redirect('approved-customer')


def ConfirmBooking(request, id):
    c = BookingRequest.objects.get(id=id)
    if c.house.status == "Booked":
        msg = 'House is already booked'
        booking = BookingRequest.objects.filter(house__user=UserProfile.objects.get(user=request.user), status="Accepted")
        return render(request, 'approved-customers.html',{'requests':booking, 'msg':msg})
    c.status = "Booked"
    c.house.status = "Booked"
    c.house.save()
    c.save()

    return redirect('approved-customer')


def AvailableHouse(request, id):
    h = House.objects.get(id=id)
    h.status = "Available"
    h.save()
    return redirect('rent-house')


def BookHouse(request,id):
    if not request.user.is_authenticated:
        return redirect('login')
    h = House.objects.get(id=id)
    user = UserProfile.objects.get(user=request.user)
    BookingRequest.objects.create(
        user = user,
        house = h
    )
    return redirect('my-booking')


def DeletePublicBooking(request,id):
    if not request.user.is_authenticated:
        return redirect('login')
    booking = BookingRequest.objects.get(id=id)
    booking.delete()
    return redirect('customer-request')


def HelpDeskView(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_profile = UserProfile.objects.get(user=request.user)  # Fetch the user profile
    booked_houses = BookingRequest.objects.filter(user=user_profile, status="Booked").select_related('house')

    if not booked_houses.exists():
        return render(request, 'user-helpdesk.html', {'error': 'You cannot send a message. You must book a house first.'})

    if request.method == "POST":
        message_text = request.POST.get('message')

        for booking in booked_houses:
            house_owner = booking.house.user  # Fetch house owner
            house_owner_email = house_owner.user.email  # House owner email
            admin_email = 'admin@example.com'  # Change this to actual admin email

            # Save message in the database
            HelpDeskModel.objects.create(
                user=user_profile,
                house=booking.house,
                owner=house_owner,
                message=message_text
            )

            # Email Body
            subject = "HelpDesk Query - Home Rental Service"
            body = f"""
            Hi {house_owner.user.first_name},

            {request.user.first_name} has booked your house ({booking.house.house_no}) and wants to contact you.

            User Email: {request.user.email}
            House Owner Email: {house_owner_email}

            Message:
            {message_text}

            Regards,
            Home Rental Service
            """

            # Send Email to Owner & CC Admin
            send_mail(subject, body, settings.EMAIL_HOST_USER, [house_owner_email, admin_email], fail_silently=True)

        return render(request, 'user-helpdesk.html', {'success': 'Your message has been sent successfully.'})

    return render(request, 'user-helpdesk.html')

def ApproveOwner(request):
    if not request.user.is_authenticated:
        return redirect('login')
    unverified = UserProfile.objects.filter(userType="Owner", verified=False)
    return render(request, 'approve-owner.html',{'verified':unverified})



def ApproveAdmin(request):
    if not request.user.is_authenticated:
        return redirect('login')
    unverified = UserProfile.objects.filter(userType="Admin", verified=False)
    return render(request, 'approve-admin.html',{'verified':unverified})


def AdminHelpDesk(request):
    u = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        email = request.POST.get('email')
        message = request.POST.get('message')

        subject = 'From Home Rental Service'
        from_email = settings.EMAIL_HOST_USER
        to_email = [email]
        if u.userType == "Admin":
            body = f'Hi,  \n \n \t  email: {email} \n \n \t message: {message} \n\n Thanks, \n From Admin, \nHome Rental Service'
        else:
            body = f'Hi {email}, \n \n \t message: {message} \n\n Thanks, \n From Owner, \nHome Rental Service'         
        send_mail(subject, body, from_email, to_email, fail_silently=True)

    return render(request, 'admin-helpdesk.html')


def Dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    total_verified_owner = UserProfile.objects.filter(userType="Owner", verified=True).count()
    total_unverified_owner = UserProfile.objects.filter(userType="Owner", verified=False).count()

    total_verified_admin = UserProfile.objects.filter(userType="Admin", verified=True).count()
    total_unverified_admin = UserProfile.objects.filter(userType="Admin", verified=False).count()

    available_house = House.objects.filter(status="Available").count()
    booked_house = House.objects.filter(status="Booked").count()

    customer_request = BookingRequest.objects.filter(status="Pending").count()

    my_house = House.objects.filter(user=UserProfile.objects.get(user=request.user)).count()
    my_available_house = House.objects.filter(user=UserProfile.objects.get(user=request.user), status="Available").count()

    my_booking = BookingRequest.objects.filter(user=UserProfile.objects.get(user=request.user)).count()

    Dict = {
        "total_verified_owner":total_verified_owner,
        "total_unverified_owner":total_unverified_owner,
        "total_verified_admin":total_verified_admin,
        "total_unverified_admin":total_unverified_admin,
        "available_house":available_house,
        "booked_house":booked_house,
        "customer_request":customer_request,

        "my_house": my_house,
        "my_available_house":my_available_house,

        "my_booking":my_booking
    }
    return render(request, 'dashboard.html',Dict)