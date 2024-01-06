from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order, OrderItem
from products.models import Product
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # gets all orders for the logged in user
        orders = Order.objects.filter(user=request.user)
        if  not orders:
            return Response({'error': 'No orders found'}, status=status.HTTP_404_NOT_FOUND)
        # passes the orders to the serializer
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        # creates a new order for the logged in user
        data = request.data
        if 'order_items' not in request.data:
            return Response({'error': 'No order items provided'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            order = Order.objects.create(user=request.user,
                                    city=data['city'], 
                                    street=data['street'], 
                                    state=data['state'], 
                                    country=data['country'], 
                                    zip_code=data['zip_code'], 
                                    phone=data['phone']
                                    )
            # get the order items from the request
            order_items = request.data.get('order_items')
        for item in order_items:
            product = Product.objects.get(id=item['product'])
            if product.stock < item['quantity']:
                return Response({'error': f'Not enough stock for {product.name}'}, status=status.HTTP_400_BAD_REQUEST)
            order_item = OrderItem.objects.create(order=order, 
                                                product=product,
                                                quantity=item['quantity'], 
                                                price=product.price)
            product.stock -= order_item.quantity
            product.save()
        order.total_cost = order.get_total_cost()
        order.save()
        serializer = OrderSerializer(order, many=False)
        return Response({'message': 'Order created', 'order': serializer.data}, status=status.HTTP_201_CREATED)