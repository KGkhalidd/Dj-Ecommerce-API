from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Product, Review
from .serializers import ProductSerializer, ReviewSerializer
from .filters import ProductFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg

@api_view(['GET'])
def product_list(request):
    filterset = ProductFilter(request.GET, queryset=Product.objects.all().order_by('id'))
    paginator = PageNumberPagination()
    paginator.page_size = 2
    queryset = paginator.paginate_queryset(filterset.qs, request)
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def product_create(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({'message': 'Product was created successfully!', 'data': serializer.data}, status= status.HTTP_201_CREATED)
    return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def product_update(request, pk):
    product = get_object_or_404(Product, id=pk)
    if product.user != request.user:
        return Response({'message': 'You are not authorized to update this product!'}, status= status.HTTP_401_UNAUTHORIZED)
    serializer = ProductSerializer(instance=product, data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({'message': 'Product was updated successfully!', 'data': serializer.data}, status= status.HTTP_200_OK)
    return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def product_delete(request, pk):
    product = get_object_or_404(Product, id=pk)
    if product.user != request.user:
        return Response({'message': 'You are not authorized to update this product!'}, status= status.HTTP_401_UNAUTHORIZED)
    product.delete()
    return Response({'message': 'Product was deleted successfully!'}, status= status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_create_or_update(request, pk):
    product = get_object_or_404(Product, id=pk)
    # .first() returns the first element in the queryset or None if the queryset is empty.
    review =  Review.objects.filter(user= request.user, product=product).first()
    # if no review exists, create a new one
    if review is None:
        serializer = ReviewSerializer(data=request.data)
    # else update the existing one
    else:
        if review.user != request.user:
            return Response({'message': 'You are not allowed to update this review.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(user=request.user, product=product)
        '''
        calculate the average rating for the product
        The aggregate function returns a dictionary where the key is the string passed to the Avg function 
        appended with __avg and the value is the calculated average.
        '''
        avg_ratings = Review.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']
        product.ratings = avg_ratings
        product.save()
        return Response({'message': 'Review was created/updated successfully!', 'data': serializer.data}, status= status.HTTP_201_CREATED)
    return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def review_delete(request, pk):
    review = get_object_or_404(Review, id=pk)
    if review.user != request.user:
        return Response({'message': 'You are not authorized to delete this review!'}, status= status.HTTP_401_UNAUTHORIZED)
    product = review.product
    review.delete()
    avg_ratings = Review.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']
    product.ratings = avg_ratings
    product.save()
    return Response({'message': 'Review was deleted successfully!'}, status= status.HTTP_204_NO_CONTENT)