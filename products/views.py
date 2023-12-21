from products.filters import ProductFilter
from rest_framework import filters
from django_filters import rest_framework as django_filters
from .serializers import ProductSerializer, UserSerializer
from products.models import Product, View
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from products.models import Category, Order
from .serializers import CategorySerializer, OrderSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = (django_filters.DjangoFilterBackend,
                       filters.SearchFilter)
    filterset_class = ProductFilter
    search_fields = ['name', 'description']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        view, created = View.objects.get_or_create(product=instance)
        if not created:
            view.count += 1
            view.save()

        serializer = self.get_serializer(instance)
        related_products = Product.objects.filter(
            category=instance.category).exclude(id=instance.id)[:4]
        related_serializer = ProductSerializer(related_products, many=True)
        return Response({
            'product': serializer.data,
            'related_products': related_serializer.data
        })

    @action(detail=False, methods=['get'])
    def most_viewed(self, request):
        most_viewed_products = Product.objects.annotate(
            most_view=Sum('view__count')
        ).order_by('-most_view')[:10]

        serializer = self.get_serializer(most_viewed_products, many=True)

        return Response(serializer.data)


@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
