from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Post, Comment, Vote
from .permissions import IsOwner
from .serializers import PostSerializer, CommentSerializer


class PostView(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        queryset = Post.objects.get(pk=pk).comments
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        post = Post.objects.get(pk=pk)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post, author=self.request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_url_kwarg = "pk2"

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        self._check_comment_belongs_to_post(instance, kwargs.get("pk"))
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        self._check_comment_belongs_to_post(instance, kwargs.get("pk"))
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        self._check_comment_belongs_to_post(instance, kwargs.get("pk"))
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self._check_comment_belongs_to_post(instance, kwargs.get("pk"))
        return self.destroy(request, *args, **kwargs)

    def _check_comment_belongs_to_post(self, instance, pk):
        if instance.post_id != pk:
            raise Http404


class Upvote(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs.get("pk"))
        return Response({"upvotes": instance.upvotes},
                        status=status.HTTP_200_OK)

    def post(self, request, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs.get("pk"))
        try:
            Vote.objects.create(user=request.user, post=instance)
        except IntegrityError:
            raise ValidationError("You have already upvoted this post")

        return Response("Your upvote has been sumbitted",
                        status=status.HTTP_201_CREATED)

    def delete(self, request, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs.get("pk"))

        try:
            vote = Vote.objects.get(user=request.user, post=instance)
        except ObjectDoesNotExist:
            raise ValidationError(
                "You can vote against only if you upvoted previously")
        vote.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
