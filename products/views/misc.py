from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from products.models import Category
from products.serializers import CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
