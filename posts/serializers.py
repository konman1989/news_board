from rest_framework import serializers

from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(error_messages={
        'required': 'Argument is either missing or wrong.',
        'blank': 'This field cannot be empty.'
    })
    link = serializers.CharField(error_messages={
        'required': 'Argument is either missing or wrong.',
        'blank': 'This field cannot be empty.'
    })

    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['pk', 'title', 'link', 'created_on', 'author', 'upvotes']


class CommentSerializer(serializers.ModelSerializer):
    content = serializers.CharField(error_messages={
        'required': 'Argument is either missing or wrong.',
        'blank': 'This field cannot be empty.'
    })

    author = serializers.PrimaryKeyRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['pk', 'content', 'created_on', 'author', 'post']