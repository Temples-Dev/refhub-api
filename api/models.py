from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # By default, Django provides email, username, and password fields in AbstractUser.
    # We override USERNAME_FIELD to use email for authentication.
    
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'  # Set email as the field for login
    REQUIRED_FIELDS = ['username']  # Username is still required for uniqueness

    def __str__(self):
        return self.email


class Order(models.Model):
    name = models.CharField(max_length=255)  # Item name
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Item price
    quantity = models.PositiveIntegerField()  # Item quantity

    def __str__(self):
        return f'{self.name} (Quantity: {self.quantity}, Price: {self.price})'