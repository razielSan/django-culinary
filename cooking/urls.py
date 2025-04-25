from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.views.decorators.cache import cache_page

from cooking import views
from cooking.yasg import urlpatterns as api_doc_urls, schema_view


urlpatterns = [
    # path("", views.index, name="index"),
    # path("", cache_page(60 * 15)(views.Index.as_view()), name="index"), # Кэшируем url на базе файловой системы
    path("", views.Index.as_view(), name="index"),

    path("post/<int:pk>/update/", views.PostUpdate.as_view(), name="post_update"),
    # path("post/<int:pk>/delete/", views.delete_post, name="delete_post"),
    path("post/<int:pk>/delete/", views.PostDelete.as_view(), name="delete_post"),
    path("post/<int:post_id>/comment/", views.add_comment, name="add_comment"),
    path("user/<int:user_id>/profile/", views.profile, name="profile"),
    path("category/<int:pk>/", views.category_list, name="category_list"),
    # path("category/<int:pk>", views.ArticleByCategory_class.as_view(), name="category_list"),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    # path("post/<int:pk>/", views.PostDetail_class.as_view(), name="post_detail"),
    path("post/add/", views.AddPost.as_view(), name="add_post"),
    # path("post/add/", views.add_post, name="add_post"),
    path("user/login/", views.user_login, name="user_login"),
    path("user/logout/", views.user_logout, name="user_logout"),
    path("user/register/", views.user_register, name="user_register"),
    path("search/", views.search, name="search"),
    path(
        "user/change_password/",
        views.UserChangePassword.as_view(),
        name="change_password",
    ),
    # API
    path("posts/api/", views.CookingApi.as_view(), name="CookingApi"),
    path(
        "posts/api/<int:pk>/", views.CookingApiDetail.as_view(), name="CookingApiDetail"
    ),
    path(
        "category/api/", views.CookingApiCategory.as_view(), name="CookingApiCategory"
    ),
    path(
        "category/api/<int:pk>/",
        views.CookingApiCategoryDetail.as_view(),
        name="CookingApiCategoryDetail",
    ),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]

urlpatterns += api_doc_urls