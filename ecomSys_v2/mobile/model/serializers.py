from rest_framework import serializers

from category.serializers import CategorySerializer
from model.models import Mobile


class MobileSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Mobile
        exclude = ['deleted']

    def get_categories(self, obj):
        categories = obj.categories.all()
        return CategorySerializer(categories, many = True).data
