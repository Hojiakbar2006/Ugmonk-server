from rest_framework import serializers
from products.models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# serializers.py


class ProductSerializer(serializers.ModelSerializer):
    most_view = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'discount', 'price',
            'image', 'category', 'stock', 'most_view']
