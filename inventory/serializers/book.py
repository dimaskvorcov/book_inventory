from rest_framework import serializers
from inventory.models.book import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('user', 'created_at')