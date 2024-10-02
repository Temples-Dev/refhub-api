from django.urls import path
from django.urls import path


from .views import UserSignupView, UserLoginView, OrderView, OrderListView,TransportationFeeUpdateAPIView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('orders/', OrderView.as_view(), name='orders'),
     path('orderss/', OrderListView.as_view(), name='order-list'),
     path('transportation-fee/', TransportationFeeUpdateAPIView.as_view(), name='update-transporation'),
     
]


