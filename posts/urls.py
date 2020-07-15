from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'posts_api'

router = DefaultRouter()
router.register(r"posts", views.PostView, basename="posts")
urlpatterns = router.urls

urlpatterns += [
    path('posts/<int:pk>/comments/', views.CommentView.as_view(),
         name='comments'),
    path('posts/<int:pk>/comments/<int:pk2>/',
         views.CommentDetailView.as_view(), name='comments_detail'),
    path('posts/<int:pk>/upvote/', views.Upvote.as_view(),
         name='post_upvote'),
]
