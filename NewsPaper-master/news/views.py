from datetime import datetime, timedelta
from django.utils.translation import gettext as _

from rest_framework import viewsets  # permissions

from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from .models import Post, Category, Author, User, PostCategory, Comment
from .serializers import (
    UserSerializer,
    AuthorSerializer,
    CategorySerializer,
    PostSerializer,
    PostCategorySerializer,
    CommentSerializer,
)
from .filters import PostFilter
from .forms import PostForm
from .tasks import inform_about_new_posts


class PostView(ListView):
    model = Post
    ordering = "-date_published"
    template_name = "posts.html"
    context_object_name = "posts"
    paginate_by = 10


class PostSearch(ListView):
    model = Post
    ordering = "-date_published"
    template_name = "search.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filterset"] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = "post"


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ("news.add_post",)
    form_class = PostForm
    model = Post
    template_name = "post_edit.html"

    def form_valid(self, form):
        post = form.save(commit=False)
        # author = Author.objects.get_or_create(user=self.request.user)[0]
        author = Author.objects.get(user=self.request.user)
        # post.author = author
        form.instance.author = self.request.user.author
        today = datetime.now()
        limit = today - timedelta(days=1)
        count = Post.objects.filter(author=author, date_published__gte=limit).count()
        if self.request.path == "/articles/create/":
            post.type = "AR"
        if count >= 3:
            return render(self.request, "post_create_limit.html")
        post.save()
        inform_about_new_posts.delay(post.pk)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["get_title"] = self.get_type()["title"]
        context["get_header"] = self.get_type()["header"]
        return context

    def get_type(self):
        if self.request.path == "/articles/create/":
            return {"title": _("Создать статью"), "header": _("Добавить статью")}
        else:
            return {"title": _("Создать новость"), "header": _("Добавить новость")}


class PostEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ("news.change_post",)
    form_class = PostForm
    model = Post
    template_name = "post_edit.html"


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ("news.delete_post",)
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("posts")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_not_author"] = not self.request.user.groups.filter(
            name="authors"
        ).exists()
        return context


class CategoryListView(LoginRequiredMixin, PostView):
    model = Post
    template_name = "category_list.html"
    context_object_name = "category_news_list"

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs["pk"])
        queryset = Post.objects.filter(category=self.category).order_by(
            "-date_published"
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_not_subscribed"] = (
            self.request.user not in self.category.subscribers.all()
        )
        context["is_subscribed"] = self.request.user in self.category.subscribers.all()
        context["category"] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = _("Вы успешно подписались на рассылку категории")
    return render(
        request, "un_subscribe.html", {"category": category, "message": message}
    )


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)

    message = _("Вы успешно отписались от рассылку категории")
    return render(
        request, "un_subscribe.html", {"category": category, "message": message}
    )


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name="authors")
    if not request.user.groups.filter(name="authors").exists():
        authors_group.user_set.add(user)
        Author.objects.create(user=user)
    return redirect("/news/profile/")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostCategoryViewSet(viewsets.ModelViewSet):
    queryset = PostCategory.objects.all()
    serializer_class = PostCategorySerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class NewsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(type="NW")
    serializer_class = PostSerializer


class ArticlesViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(type="AR")
    serializer_class = PostSerializer
