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
