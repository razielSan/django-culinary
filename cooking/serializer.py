from rest_framework import serializers

from cooking.models import Post, Category


class PostSerializer(serializers.ModelSerializer):
    """Поля которые будут отображаться в API"""

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "category",
            "content",
            "created_at",
            "author",
        )


class CategorySerializer(serializers.ModelSerializer):
    """Поля которые будут отображаться в API"""
    class Meta:
        model = Category
        fields = (
            "id",
            "title",
        )