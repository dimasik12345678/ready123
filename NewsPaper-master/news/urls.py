from django.urls import path
from .views import (
    PostView,
    PostDetail, PostSearch, PostCreate, PostEdit, PostDelete,
    ProfileView, upgrade_me, CategoryListView,
    subscribe, unsubscribe
)
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60)(PostView.as_view()), name='posts'),
    path('<int:pk>', cache_page(300)(PostDetail.as_view()), name='post'),
    path('search/', PostSearch.as_view(), name='search'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/upgrade/', upgrade_me, name='upgrade'),
    path('categories/<int:pk>/', CategoryListView.as_view(), name='categories'),
    path('categories/<int:pk>/subscribe/', subscribe, name='subscribe'),
    path('categories/<int:pk>/unsubscribe/', unsubscribe, name='unsubscribe')
]
