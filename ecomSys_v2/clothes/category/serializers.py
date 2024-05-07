from rest_framework import serializers
from category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['deleted', 'created_at', 'updated_at']
