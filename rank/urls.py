from django.urls import path
from .views import CommentView

urlpatterns = [
    path('/comment/<str:user_id>', CommentView.as_view())
]
