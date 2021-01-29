from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import generics
from rest_framework.response import Response
from .models import Category, Post, PostView, Comment, Like
from .serializers import CategorySerializer, CommentCreateSerializer, PostListSerializer, PostDetailSerializer, PostCreateUpdateSerializer, CommentSerializer, LikeCreateSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from .permissions import IsOwner
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

class CategoryList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    # queryset = Category.objects.filter(name='World')

# class LikeView():

class PostList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostListSerializer
    # queryset = Post.objects.all()
    queryset = Post.objects.filter(status="p")

class UserPostList(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = PostListSerializer
    # queryset = Post.objects.filter(author=request.user)

    def get_queryset(self):
        queryset = Post.objects.filter(author=self.request.user)
        return queryset

class PostCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostCreateUpdateSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostDetailSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'

class PostUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = PostCreateUpdateSerializer
    queryset = Post.objects.all()
    lookup_field = "slug"
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

class PostDelete(generics.DestroyAPIView):
    serializer_class = PostDetailSerializer
    queryset = Post.objects.all()
    lookup_field = "slug"
    permission_classes = [IsAuthenticated]

class CreateCommentAPI(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer
    queryset = Comment.objects.all()
    lookup_field = "slug"
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)

    # def get_queryset(self):
    #     queryset = Question.objects.all()
    #     title = self.kwargs["title"]
    #     queryset = queryset.filter(quiz__title=title)
    #     return queryset

class CreateLikeAPI(generics.CreateAPIView):
    serializer_class = LikeCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        like_qs = Like.objects.filter(user=request.user, post=post)
        if like_qs.exists():
            like_qs[0].delete()
        else:
            Like.objects.create(user=request.user, post=post)
        data = {
            "messages": 'like'
        }
        return Response(data)