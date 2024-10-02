from rest_framework import serializers
from .models import User , Order, OrderItem, TransportationFee
from django.contrib.auth import authenticate


# model for signing up
class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user
    

# model for logging in
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials, please try again.")
        else:
            raise serializers.ValidationError("Both email and password are required.")

        data['user'] = user
        return data
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'username']    
        
class TransportationFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportationFee
        fields = ['amount']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['name', 'price', 'quantity']
    
    
class OrderSerializer(serializers.ModelSerializer):
    orderId = serializers.IntegerField(source='id', read_only=True)
    order_date = serializers.DateTimeField(source='created_at', format='%Y-%m-%d', read_only=True)
    user = UserSerializer(read_only=True)
    items = ItemSerializer(many=True)  # Serializing multiple items
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    transportation_fee = serializers.DecimalField(source='transportation_fee.amount', max_digits=6, decimal_places=2)
    

    class Meta:
        model = Order
        fields = ["orderId",'order_date','total_amount','transportation_fee',"user",'items']  

    def create(self, validated_data):
        # First, extract the list of items from the validated data
        items_data = validated_data.pop('items')

        transportation_fee = validated_data.pop('transportation_fee')

        order = Order.objects.create(**validated_data, transportation_fee=transportation_fee)

        # Now iterate over items_data and create the OrderItem linked to the Order
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
            
        # Calculate and set total amount
        order.total_amount = order.calculate_total()
        order.save()

        return order
