from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from .filters import ProductFilter

@api_view(['GET'])
def product_list(request):
    #products = Product.objects.all()
    filterset = ProductFilter(request.GET, queryset=Product.objects.all().order_by('id'))
    serializer = ProductSerializer(filterset.qs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)