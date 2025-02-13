from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now

class Menu(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(99999)] )
    def __str__(self):
        return f'{self.title} : {str(self.price)}'
    
class Booking(models.Model):
    name = models.CharField(max_length=255)
    no_of_guests = models.IntegerField(6)
    booking_date = models.DateTimeField(default=now)
    def __str__(self):
        return f"{self.name} - {self.booking_date}"