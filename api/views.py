from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSignupSerializer, UserLoginSerializer, OrderSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



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
            
            ),
            401: "Unauthorized"
        },
        operation_description="Login to existing account"
        )
    
    
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response({"message": "Login successful", "user": user.username}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
class OrderView(APIView):
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=['name', 'price', 'quantity'],
                properties={
                    'name': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Name of the food item',
                        example='Burger'
                    ),
                    'price': openapi.Schema(
                        type=openapi.TYPE_NUMBER,
                        format=openapi.FORMAT_FLOAT,
                        description='Price of the item',
                        example=5.99
                    ),
                    'quantity': openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description='Quantity of items to order',
                        example=2
                    ),
                }
            )
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
                                "name": "Burger",
                                "price": 5.99,
                                "quantity": 2,
                                "total": 11.98
                            },
                            {
                                "id": 2,
                                "name": "Pizza",
                                "price": 12.99,
                                "quantity": 1,
                                "total": 12.99
                            }
                        ]
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request",
                examples={
                    "application/json": {
                        "error": "Invalid order data",
                        "details": [
                            {
                                "order": 1,
                                "errors": {
                                    "price": ["Price must be a positive number"]
                                }
                            }
                        ]
                    }
                }
            )
        },
        operation_description="Create multiple orders at once. Each order should contain name, price, and quantity."
    )
    
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            return Response({'message': 'Order submitted successfully', 'orders': OrderSerializer(order).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)