from django.db import models
from django.core.validators import MinValueValidator
from HouseRentManagementApp.models import UserProfile

class House(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Booked', 'Booked'),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="houses_owned")
    house_no = models.CharField(max_length=255, unique=True)
    room_size = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    pincode = models.IntegerField(validators=[MinValueValidator(100000)])
    state = models.CharField(max_length=255)
    image1 = models.ImageField(upload_to='house_images/')
    image2 = models.ImageField(upload_to='house_images/')
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Available")
    price = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.house_no} - {self.area} ({self.status})"


class BookingRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Booked', 'Booked'),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="booking_requests")
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name="bookings")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user.username} - {self.house.house_no} ({self.status})"


class HelpDeskModel(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="help_requests")
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name="help_requests")
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="help_queries_received")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Help Request by {self.user.user.username} for {self.house.house_no}"
