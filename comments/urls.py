from django.urls import path
from .views import CommentListCreateView

urlpatterns = [
    path('<int:ticket_id>/comments/', CommentListCreateView.as_view(), name='comments'),
]