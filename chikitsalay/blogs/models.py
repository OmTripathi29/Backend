from django.db import models
import chikitsalay.settings as settings
from django.core.validators import FileExtensionValidator
class Blog(models.Model):
    
    blog_image=models.ImageField(upload_to='blog/images/', null=True, blank=True,validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png','webp'],)])
    author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='blogs')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    
class BlogLike(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='blog_likes')
    blog=models.ForeignKey(Blog, on_delete=models.CASCADE,related_name='likes')
    created_at=models.DateTimeField(auto_now_add=True)  
    class Meta:
        unique_together = ('user', 'blog')
        
    def __str__(self):
        return f"{BlogLike.objects.filter(blog=self.blog).count()} likes for {self.blog.title}"
        
class BlogComment(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='blog_comments')
    blog=models.ForeignKey(Blog, on_delete=models.CASCADE,related_name='comments')
    comment=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)


    