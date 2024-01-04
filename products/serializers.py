from rest_framework import serializers
from .models import Product, Review



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'brand', 'category', 'ratings', 'stock', 'created', 'user', 'reviews']