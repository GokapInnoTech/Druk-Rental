"""houserentproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
#from HouseRentManagementApp import views
from HouseRentManagementApp.views import (
    IndexPage,
    AboutPage,
    ContactPage,
    ServicesPage,
    LoginPage,
    Logout,
    SignPage,
    OwnerSign,
    ForgotPage,
    ForgotPassword,
    SendEmailForForgotPassword
    )
from AdminApp.views import (
    AllUser,
    ViewUser,
    AddAdmin,
    Profile, 
    DeleteUser,
    ChangePassword,
    EditProfile,
    EditHouse,
    RentHouse,

    ViewHouse,
    MyBooking,
    AddHouse,
    CustomerRequest,
    BookHouse,
    DeletePublicBooking,
    MyHouse,
    Location,

    HelpDesk,
    AdminHelpDesk,
    ApproveOwner,
    ApproveAdmin,
    ApprovedCustomer,
    ApproveOwnerRequest,
    ApproveCustomerRequest,
    ConfirmBooking,
    AvailableHouse,

    Dashboard
)

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',IndexPage,name='index') , 
    path('about/', AboutPage, name='about'),
    path('contact/', ContactPage, name='contact'),
    path('services/', ServicesPage),
    path('login/', LoginPage, name='login'),
    path('logout/', Logout, name='logout'),
    path('sign/', SignPage, name='sign'),
    path('owner-sign/', OwnerSign, name='owner-sign'),
    path('forgot/', ForgotPage),
    path('forgotpassword/',ForgotPassword,name='forgotpassword'),
    path('sendotp/',SendEmailForForgotPassword,name="sendotp"),

    path('change-password/', ChangePassword, name="change-password"),
    path('profile/',Profile,name='profile'),
    path('delete-user/<int:id>/', DeleteUser, name='delete-user'),
    path('edit-profile/<int:id>/', EditProfile, name='edit-profile'),
    path('edit-house/<int:id>/', EditHouse, name='edit-house'),
    path('my-house/', MyHouse, name='my-house'),
    path('add-house/', AddHouse, name='add-house'),
    path('rent-house/', RentHouse, name='rent-house'),
    path('view-house/<int:id>/', ViewHouse, name='view-house'),
    path('book-house/<int:id>/', BookHouse, name='book-house'),
    path('delete-booking/<int:id>/', DeletePublicBooking, name='delete-booking'),
    path('my-booking/', MyBooking, name="my-booking"),
    path('customer-request/', CustomerRequest, name="customer-request"),

    path('helpdesk/', HelpDesk, name='helpdesk'),
    path('admin-helpdesk/', AdminHelpDesk, name='admin-helpdesk'),
    path('all-user/', AllUser, name='all-user'),
    path('view-user/<int:id>/', ViewUser, name='view-user'),
    path('add-admin/', AddAdmin, name='add-admin'),
    path('approve-owner/', ApproveOwner, name='approve-owner'),
    path('approve-admin/', ApproveAdmin, name='approve-admin'),
    path('approved-customer/', ApprovedCustomer, name='approved-customer'),
    path('approve-owner-request/<int:id>/', ApproveOwnerRequest, name='approve-owner-request'),
    path('approve-customer-request/<int:id>/', ApproveCustomerRequest, name='approve-customer-request'),
    path('confirm-booking/<int:id>/', ConfirmBooking, name='confirm-booking'),
    path('available-house/<int:id>/', AvailableHouse, name='available-house'),
    path('location/<int:id>/', Location, name='location'),

    path('dashboard/', Dashboard, name='dashboard')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
