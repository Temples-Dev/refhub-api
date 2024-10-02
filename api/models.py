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




class TransportationFee(models.Model):
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=10.00)  # Default value

    def __str__(self):
        return f"Transportation Fee: {self.amount}"



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
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    transportation_fee = models.ForeignKey(TransportationFee, on_delete=models.SET_NULL, null=True)
    
    
    def calculate_total(self):
        # Calculate the total based on item prices and transportation fee
        total = sum(item.price * item.quantity for item in self.items.all())
        total += self.transportation_fee.amount
        return total
    
    def save(self, *args, **kwargs):
        # Recalculate total amount before saving
        self.total_amount = self.calculate_total()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Order #{self.id}"


