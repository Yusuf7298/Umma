from django.urls import path
from .views import *


urlpatterns = [
    path('', BlogListView.as_view(), name="home"),
    path('blogcomment/', blogcomment, name="blogcomment"),
    path('video_post/', VideoPost.as_view(), name="video_post"),
    path('image_post/', ImagePost.as_view(), name="image_post"),
    path('idea_post/', IdeaPost.as_view(), name="idea_post"),
    path('idea_post/new/', CreatePost.as_view(), name="create_post"),
    path('image_post/new/', CreateImagePost.as_view(), name="create_image_post"),
    path('video_post/new/', CreateVideoPost.as_view(), name="create_video_post"),
    path('content_post/new/', CreateIdeaPost.as_view(), name="create_idea_post"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="detail_post"),
    path('user_post/<str:username>', UserPostListView.as_view(), name="user-posts"),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name="update_post"),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name="delete_post"),


]