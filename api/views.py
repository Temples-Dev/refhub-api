from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSignupSerializer, UserLoginSerializer, OrderSerializer
from .models import Order
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
            )
        },
        operation_description="Create multiple orders at once. Provide an array of items, each containing name, price, and quantity."
    )
    
    # def post(self, request):
    #     serializer = OrderSerializer(data=request.data)
    #     if serializer.is_valid():
    #         order = serializer.save()
    #         return Response({
    #             "message": "Order submitted successfully",
    #             "orders": order.items.values() 
    #         }, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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