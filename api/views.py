from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSignupSerializer, UserLoginSerializer, OrderSerializer
from .models import Order
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.tokens import RefreshToken
from .models import TransportationFee
from .serializers import TransportationFeeSerializer

class UserSignupView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
            }
        ),
        responses={
            201: openapi.Response(
                description="User created successfully",
               
            ),
            400: "Bad Request"
        },
        operation_description="Create a new user account"
    )
    
    def post(self, request, *args, **kwargs):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


   
    
class UserLoginView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
            }
        ),
        responses={
            200: openapi.Response(
                description="Login successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'user': openapi.Schema(type=openapi.TYPE_STRING),
                        'accessToken': openapi.Schema(type=openapi.TYPE_STRING),
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            401: "Unauthorized"
        },
        operation_description="Login to existing account"
    )
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                "message": "Login successful",
                "user": user.username,
                "accessToken": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OrderView(APIView):
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                description='Bearer {token}',
                default='Bearer '
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['items'],
            properties={
                'items': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        required=['name', 'price', 'quantity'],
                        properties={
                            'name': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='Name of the food item',
                                example='Wakye'
                            ),
                            'price': openapi.Schema(
                                type=openapi.TYPE_NUMBER,
                                format=openapi.FORMAT_FLOAT,
                                description='Price of the item',
                                example=2.99
                            ),
                            'quantity': openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description='Quantity of items to order',
                                example=1
                            ),
                        }
                    ),
                    example=[
                        {
                            "name": "Bread",
                            "price": 5.99,
                            "quantity": 2
                        },
                        {
                            "name": "Koose",
                            "price": 5.99,
                            "quantity": 2
                        },
                        {
                            "name": "Wakye",
                            "price": 2.99,
                            "quantity": 1
                        }
                    ]
                )
            }
        ),
        responses={
            201: openapi.Response(
                description="Orders created successfully",
                examples={
                    "application/json": {
                        "message": "Orders created successfully",
                        "orders": [
                            {
                                "id": 1,
                                "name": "Bread",
                                "price": 5.99,
                                "quantity": 2,
                                "total": 11.98
                            },
                            {
                                "id": 2,
                                "name": "Koose",
                                "price": 5.99,
                                "quantity": 2,
                                "total": 11.98
                            },
                            {
                                "id": 3,
                                "name": "Wakye",
                                "price": 2.99,
                                "quantity": 1,
                                "total": 2.99
                            }
                        ]
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request",
                examples={
                    "application/json": {
                        "error": "Invalid request",
                        "details": "Missing or invalid items array"
                    }
                }
            ),
            401: openapi.Response(
                description="Unauthorized",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            )
        },
        operation_description="Create multiple orders at once. Provide an array of items, each containing name, price, and quantity. Requires Bearer token authentication."
    )
    
  
  
    def post(self, request, *args, **kwargs):
        # Parse the incoming data
        serializer = OrderSerializer(data=request.data)

        # Check if the data is valid
        if serializer.is_valid():
            # Save the order and associate it with the authenticated user
            serializer.save(user=request.user)

            return Response({"message": "Order created successfully", "order": serializer.data}, status=status.HTTP_201_CREATED)

        # Return an error response if the data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class OrderListView(APIView):
    def get(self, request, *args, **kwargs):
        # Retrieve all orders
        orders = Order.objects.all().prefetch_related('items').select_related('user')  # Optimize queries
        
        # Serialize the orders
        serializer = OrderSerializer(orders, many=True)
        
        return Response(serializer.data)
    
    



class TransportationFeeUpdateAPIView(APIView):
    def get(self, request):
        try:
            fee = TransportationFee.objects.first()
            serializer = TransportationFeeSerializer(fee)
            return Response(serializer.data)
        except TransportationFee.DoesNotExist:
            return Response({"error": "Transportation fee not set."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        fee = TransportationFee.objects.first()
        serializer = TransportationFeeSerializer(fee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "fee": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)