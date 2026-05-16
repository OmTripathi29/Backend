from .models import Blog,BlogLike,BlogComment
from rest_framework import serializers


class BlogSerializer(serializers.ModelSerializer):
    author_email=serializers.EmailField(source='author.email', read_only=True)
    class Meta:
        model = Blog
        fields = [
            'id',
            'blog_image',
            'author_email',
            'title', 
            'content',
            'created_at'
        ]
class BlogLikeSerializer(serializers.ModelSerializer):  
    user_email=serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model = BlogLike
        fields = ['id', 'user_email', 'blog', 'created_at']

class BlogCommentSerializer(serializers.ModelSerializer):  
    user_email=serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model = BlogComment
        fields = ['id', 'user_email', 'blog', 'comment', 'created_at']