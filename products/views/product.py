from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from products.models import Product, View
from products.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Increase the view count
        view = View.objects.get_or_create(product=instance)
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
