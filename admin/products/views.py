from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from rest_framework.response import Response

class ProductViewSet(viewsets.ViewSet):
    # for /api/products route, GET request
    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    # for /api/products route, POST request
    def create(self, request):
        pass

    
    # the following 3 are endpoints for a product
    # pk: primary key; for route /api/product/<str:id>
    def retrieve(self, request, pk=None):
        pass


    # pk: primary key; for route /api/product/<str:id>
    def update(self, request, pk=None):
        pass


    # pk: primary key; for route /api/product/<str:id>
    def destroy(self, request, pk=None):
        pass