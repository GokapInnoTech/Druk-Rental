from django.db import models
from HouseRentManagementApp.models import UserProfile
# Create your models here.
class House(models.Model):
    STATUS = [
        ('Available', 'Available'),
        ('Booked','Booked'),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    house_no = models.CharField(max_length=255)
    room_size = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    pincode = models.IntegerField()
    state = models.CharField(max_length=255)
    image1 = models.ImageField()
    image2 = models.ImageField()
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS, default="Available")
    price = models.IntegerField()

    def __str__(self):
        return self.house_no


class BookingRequest(models.Model):
    STATUS = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Booked','Booked'),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS, default="Pending")

    # def __str__(self):
    #     return "User" + self.user.user.username + " Booked house " + self.house