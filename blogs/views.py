from rest_framework.decorators import api_view,permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response   
from rest_framework import status
from .serializers import BlogSerializer, BlogCommentSerializer
from django.shortcuts import get_object_or_404
from .models import Blog,BlogLike, BlogComment


@api_view(['GET'])
def blog_list(request, blog_id=None):

    if not blog_id:
        blogs = Blog.objects.select_related("author").order_by('-created_at')

        paginator = LimitOffsetPagination()
        paginated_blog = paginator.paginate_queryset(blogs, request)

        if paginated_blog is not None:
            serializer = BlogSerializer(paginated_blog, many=True)
            return paginator.get_paginated_response(serializer.data)

    else:
        blog = get_object_or_404(Blog, id=blog_id)

        serializer = BlogSerializer(blog)

        return Response(
            {
                "message": "Blog retrieved successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def create_blog(request):
    if request.method == 'POST':
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({
                "message": "Blog created successfully",
                "data": serializer.data
                }, status=status.HTTP_201_CREATED)
        return Response({
            "message": "Failed to create blog",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)\


@api_view(['PUT', 'PATCH', 'DELETE'])
def update_blog(request,blog_id):
    blog=Blog.objects.filter(id=blog_id).first()
    if not blog:
        return Response({
            "message":"Blog not found"
        },status=status.HTTP_404_NOT_FOUND)
    
    elif request.method in ['PUT', 'PATCH']:
        serializer = BlogSerializer(blog, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Blog updated successfully",
                "data": serializer.data
                }, status=status.HTTP_200_OK)
        return Response({
            "message": "Failed to update blog",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        blog.delete()
        return Response({
            "message": "Blog deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_blog(request, blog_id):
    blog=get_object_or_404(Blog, id=blog_id)
    user=request.user
    if BlogLike.objects.filter(user=user, blog=blog).exists():
        BlogLike.objects.filter(user=user,blog=blog).delete()
        return Response({
            "message": "Blog unliked successfully"
        }, status=status.HTTP_200_OK)
    else:
        BlogLike.objects.create(user=user, blog=blog)
        return Response({
            "message": "Blog liked successfully"
        }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_blog(request, blog_id):
    blog=get_object_or_404(Blog, id=blog_id)
    user=request.user
    comment_blog=request.data.get("comment")
    if not comment_blog:
        return Response({
            "message": "Comment cannot be empty"
        }, status=status.HTTP_400_BAD_REQUEST)      
    BlogComment.objects.create(user=user, blog=blog, comment=comment_blog)
    return Response({
            "message": "Comment added successfully"})
    
@api_view(['GET'])
def get_all_comments(request,blog_id):
    blog=get_object_or_404(Blog, id=blog_id).first()
    if not blog:
        return Response({
            "message": "Blog not found"
        }, status=status.HTTP_404_NOT_FOUND)
    comments=BlogComment.objects.filter(blog=blog).all()
    pagination=LimitOffsetPagination()
    paginated_comments=pagination.paginate_queryset(comments, request)
    if paginated_comments is not None:
        serializer=BlogCommentSerializer(paginated_comments, many=True)
        return pagination.get_paginated_response(serializer.data)
    
    return Response({
        "message": "No comments found for this blog"},status=status.HTTP_404_NOT_FOUND)
    
    
   


    


 
 

