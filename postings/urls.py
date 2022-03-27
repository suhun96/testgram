from django.urls import path
from .views import CommentView, PostView , LikeView
urlpatterns = [
    path('/post' , PostView.as_view()),
    path('/comment', CommentView.as_view()),
    path('/like' , LikeView.as_view())
]
 