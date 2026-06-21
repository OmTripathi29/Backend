from django.urls import path
from .views import blog_list,create_blog,update_blog,like_blog,comment_blog,get_all_comments


urlpatterns = [

    path("read/",blog_list),
    path("read/<int:blog_id>/",blog_list),
    path("update/<int:blog_id>/",update_blog),
    path("create/",create_blog),
    path("like_unlike/<int:blog_id>/",like_blog),
    path("comment/write/<int:blog_id>/",comment_blog),
    path("comment/get_all/<int:blog_id>/",get_all_comments),
]
