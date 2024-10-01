from django.urls import path
from .views import UserSignupView, UserLoginView, OrderView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('orders/', OrderView.as_view(), name='orders'),
]
