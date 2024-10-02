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


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')  # Each item belongs to one order
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.name} (Quantity: {self.quantity}, Price: {self.price})'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"

