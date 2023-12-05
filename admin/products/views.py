from rest_framework import viewsets, status
from .models import Product, User
from .serializers import ProductSerializer
from .producer import publish
from rest_framework.response import Response
from rest_framework.views import APIView
import random

class ProductViewSet(viewsets.ViewSet):
    # for /api/products route, GET request
    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    # for /api/products route, POST request
    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_created', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
    # the following 3 are endpoints for a product
    # pk: primary key; for route /api/product/<str:id>
    def retrieve(self, request, pk=None):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    # pk: primary key; for route /api/product/<str:id>
    def update(self, request, pk=None):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(instance=product, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_updated', serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


    # pk: primary key; for route /api/product/<str:id>
    def destroy(self, request, pk=None):
        product = Product.objects.get(id=pk)
        product.delete()
        publish('product_deleted', pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class UserAPIView(APIView):
    # To get a random user
    def get(self, _):
        users = User.objects.all()
        user = random.choice(users)
        return Response({
            'id':user.id
        })