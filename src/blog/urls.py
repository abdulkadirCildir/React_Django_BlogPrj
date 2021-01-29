from django.urls import path
from .views import CategoryList, CreateCommentAPI, PostList, PostDetail, PostCreate, PostUpdate, PostDelete, UserPostList, CreateLikeAPI

urlpatterns = [
    path("category/", CategoryList.as_view(), name="category_list"),
    path("list/", PostList.as_view(), name="post_list"),
    path("postlist/", UserPostList.as_view(), name="user_list"),
    path("create/", PostCreate.as_view(), name="post_create"),
    path("detail/<str:slug>/", PostDetail.as_view(), name="post_detail"),
    path("update/<str:slug>/", PostUpdate.as_view(), name="post_update"),
    path("delete/<str:slug>/", PostDelete.as_view(), name="post_delete"),
    path("comment/<str:slug>/", CreateCommentAPI.as_view(), name="create_comment"),
    path("like/<str:slug>/", CreateLikeAPI.as_view(), name="post_like"),
]