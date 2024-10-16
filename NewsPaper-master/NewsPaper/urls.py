from django.contrib import admin
from django.urls import path, include
from news import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"authors", views.AuthorViewSet)
router.register(r"categories", views.CategoryViewSet)
router.register(r"posts", views.PostViewSet)
router.register(r"news", views.NewsViewSet, basename="news-list")
router.register(r"articles", views.ArticlesViewSet, basename="articles-list")
router.register(r"posts_categories", views.PostCategoryViewSet)
router.register(r"comments", views.CommentViewSet)


urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path("pages/", include("django.contrib.flatpages.urls")),
    path("news/", include("news.urls")),
    path("articles/", include("news.urls")),
    path("accounts/", include("allauth.urls")),
    path("api/v1/", include(router.urls)),
    path("api/v1/auth/", include("rest_framework.urls")),
]
