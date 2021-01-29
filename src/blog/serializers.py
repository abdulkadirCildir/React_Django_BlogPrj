from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.fields import SerializerMethodField
from rest_framework.utils import serializer_helpers
from .models import Category, Post, PostView, Comment, Like
from django.db.models import Q

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            # "categories"
        )

class LikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['like_count']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "id",
            "user",
            "post",
            "time_stamp",
            "content"
        )
        lookup_field = "slug"

    def get_user(self, obj):
        return obj.user.username

    def get_post(self, obj):
        return obj.post.title

class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = (
            "user",
            "content"
        )


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            # "id",
            "owner",
            "title",
            "content",
            "image",
            "category",
            "publish_date",
            "last_update",
            "author",
            "status",
            "slug",
            "comments",
            "comment_count",
            "like_count",
            "postview_count"
        )

    def get_owner(self, obj):
        request = self.context['request']
        if request.user.is_authenticated:
            if obj.author == request.user:
                return True
            return False

class PostListSerializer(serializers.ModelSerializer):
    detail_url = serializers.HyperlinkedIdentityField(view_name='post_detail', lookup_field='slug')
    author = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "detail_url",
            "title",
            "content",
            "image",
            "category",
            "publish_date",
            "last_update",
            "author",
            "status",
            "slug",
            "comments",
            "comment_count",
            "like_count",
            "postview_count"
        )
        lookup_field = "slug"
    
    def get_author(self, obj):
        return obj.author.username

    def get_category(self, obj):
        return obj.category.name

class PostDetailSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Post.OPTIONS)
    update_url = serializers.HyperlinkedIdentityField(view_name='post_update', lookup_field='slug')
    delete_url = serializers.HyperlinkedIdentityField(view_name='post_delete', lookup_field='slug')
    create_comment_url = serializers.HyperlinkedIdentityField(view_name='create_comment', lookup_field='slug')
    like_url = serializers.HyperlinkedIdentityField(view_name='post_like',lookup_field='slug')
    author = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "update_url",
            "delete_url",
            "create_comment_url",
            "like_url",
            "has_liked",
            "owner",
            "title",
            "content",
            "image",
            "category",
            "publish_date",
            "last_update",
            "author",
            "status",
            "slug",
            "comments",
            "comment_count",
            "like_count",
            "postview_count"
        )
        lookup_field = "slug"

    def get_author(self, obj):
        return obj.author.username

    def get_category(self, obj):
        return obj.category.name
    
    def get_owner(self, obj):
        request = self.context['request']
        if request.user.is_authenticated:
            if obj.author == request.user:
                return True
            return False

    def get_has_liked(self, obj):
        request = self.context['request']
        if request.user.is_authenticated:
            if Post.objects.filter(Q(like__user=request.user) & Q(like__post=obj)).exists():
                return True
            return False