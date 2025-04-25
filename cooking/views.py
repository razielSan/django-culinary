from django.shortcuts import render, redirect
from django.db.models import F, Q
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from django.views.generic import TemplateView

from cooking.models import Post, Category, Comment
from cooking.forms.post import PostAddForm
from cooking.forms.comment import CommentForm
from cooking.forms.user import LoginForm, RegistrationForm
from cooking.serializer import PostSerializer, CategorySerializer


# Delete views

# Пример views как функции
def delete_post(request, pk: int):
    """Удаление поста"""
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect("index")


# Пример views как класса
class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy("index")
    context_object_name = "post"
    extra_context = {"title": "Удалить статью"}


# Update views

# Пример views как класса
class PostUpdate(UpdateView):
    """Изменение статьи по форме"""

    model = Post
    form_class = PostAddForm
    template_name = "cooking/article_add_form.html"
    extra_context = {"title": "Редактирование статьи"}


# Index views

# Пример views как функции
def index(request):
    """Для главной страницы"""
    posts = Post.objects.all()
    context = {
        "title": "Главная страница",
        "posts": posts,
    }

    return render(request, "cooking/index.html", context)


# Пример views как класс
class Index(ListView):
    """Для главной страницы"""

    model = Post
    context_object_name = "posts"
    extra_context = {"title": "Главная"}
    template_name = "cooking/index.html"


# Buttons category views

# Пример views как функции
def category_list(request, pk: int):
    """Реакция на нажатие кнопки категорий"""
    posts = Post.objects.filter(Q(category_id=pk) & Q(is_published=True))
    context = {
        "title": posts[0].category,
        "posts": posts,
    }

    return render(request, "cooking/index.html", context)


# Пример views как класс
class ArticleByCategory_class(Index):
    """Реакция на нажатие кнопки категорий"""

    def get_queryset(self):
        """ " Здесь переделываем фильтрации"""
        return Post.objects.filter(
            category_id=self.kwargs["pk"],
            is_published=True,
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        """Для динамических данных"""
        context = super().get_context_data()
        category = Category.objects.get(pk=self.kwargs["pk"])
        context["title"] = category.title
        return context


# Post detail

# Пример views как функции
def post_detail(request, pk: int):
    """Страница статьи"""

    post = Post.objects.get(pk=pk)
    Post.objects.filter(pk=pk).update(watched=F("watched") + 1)

    ext_post = Post.objects.all().order_by("-watched").exclude(pk=pk)[:5]
    context = {
        "title": post.title,
        "post": post,
        "ext_post": ext_post,
        "comments": Comment.objects.filter(post=post),
    }

    if request.user.is_authenticated:
        context["comment_form"] = CommentForm()
    return render(request, "cooking/article_detail.html", context)


# Пример views как класс
class PostDetail_class(DetailView):
    """Страница статьи"""

    model = Post
    template_name = "cooking/article_detail.html"

    def get_queryset(self):
        post = Post.objects.filter(pk=self.kwargs["pk"])
        return post

    def get_context_data(self, **kwargs):
        """Для динамических данных"""
        context = super().get_context_data()
        Post.objects.filter(pk=self.kwargs["pk"]).update(watched=F("watched") + 1)
        post = Post.objects.get(pk=self.kwargs["pk"])
        ext_post = (
            Post.objects.all().order_by("-watched").exclude(pk=self.kwargs["pk"])[:5]
        )
        context["ext_post"] = ext_post
        context["title"] = post.title
        if self.request.user.is_authenticated:
            context["comment_form"] = CommentForm()
        return context


# Пример views как класс
class AddPost(CreateView):
    """Добавление статьи от пользователя без админки"""

    form_class = PostAddForm
    template_name = "cooking/article_add_form.html"
    extra_context = {"title": "Добавить статью"}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# Пример views как функции
def add_post(request):
    """Добавления статьи от пользователя, без админки"""

    if request.method == "POST":
        form = PostAddForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post.objects.create(**form.cleaned_data)
            post.save()
            return redirect("post_detail", post.pk)
    else:
        form = PostAddForm()

    context = {
        "title": "Добавить статью",
        "form": form,
    }

    return render(request, "cooking/article_add_form.html", context=context)


def user_login(request):
    """Аутентификация пользователя"""
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, message="Вы успешно вошли в аккаунт")
            return redirect("index")
    else:
        form = LoginForm()

    context = {"title": "Авторизация пользователя", "form": form}
    return render(request, "cooking/login.html", context)


def user_logout(request):
    """Выход пользователя"""
    logout(request)
    return redirect("index")


def user_register(request):
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("user_login")
    else:
        form = RegistrationForm()

    context = {
        "title": "Регистрация пользователя",
        "form": form,
    }
    return render(request, "cooking/register.html", context=context)


# Search

# пример views как функции
def search(request):
    """Поиск слова в заголовках и содержаниях статьи"""
    data = request.GET["q"]
    posts = Post.objects.filter(
        Q(title__icontains=data) | Q(content__icontains=data),
    )
    context = {
        "posts": posts,
    }
    return render(request, "cooking/index.html", context=context)


# пример views как класса
class SearchResult(Index):
    """Поиск слова в заголовках и содержаниях статьи"""

    def query_set(self):
        word = self.request.GET.get("q")
        posts = Post.objects.fitler(
            Q(title__icontains=word) | Q(content__icontains=word),
        )
        return posts


def add_comment(request, post_id):
    """Добавление комментария к статьям"""
    if request.method == "POST":
        form = CommentForm(data=request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = Post.objects.get(pk=post_id)

            comment.save()

            messages.success(request, message="Ваш комментарий успешно добавленн")
        else:
            errors = form.errors.get_json_data().get("text")[0].get("message")
            messages.error(request, f"Поле комментарий: {errors}")

    return redirect("post_detail", post_id)


def profile(request, user_id: int):
    user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(author=user)
    context = {
        "title": "Личная страница",
        "user": user,
        "posts": posts,
    }
    return render(request, "cooking/profile.html", context)


class UserChangePassword(PasswordChangeView):
    """Простой способ смены пароля пользователя"""

    template_name = "cooking/password_change_form.html"
    success_url = reverse_lazy("index")


class CookingApi(ListAPIView):
    """Выдача всех статей по API"""

    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer


class CookingApiDetail(RetrieveAPIView):
    """Выдача статьи по API"""

    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)


class CookingApiCategory(ListAPIView):
    """Выдача всех категорий по API"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CookingApiCategoryDetail(RetrieveAPIView):
    """Выдача категории по API"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SwaggerApiDoc(TemplateView):
    """Документация API"""

    template_name = "swagger/swagger_ui.html"
    extra_context = {"schema_url": "openapi-schema"}
