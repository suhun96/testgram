from django.urls import path
from .views import FollowView, SignUpView , SignInView

urlpatterns = [
    path('/signup' , SignUpView.as_view()),
    path('/signin' , SignInView.as_view()),
    path('/follow' , FollowView.as_view())
]
