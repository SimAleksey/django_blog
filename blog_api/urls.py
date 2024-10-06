from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('comment', views.CommentViewSet)
router.register('articles', views.ArticleViewSet)
router.register('todo', views.TodoViewSet)



urlpatterns = [
    # path('', views.api_root),
    # path('categories/', views.CategoryListView.as_view()),
    # path('categories/<int:pk>/', views.api_category_detail),
    # path('categories/<int:pk>/', views.CategoryDetailView.as_view()),
    # path('comments/', views.CommentListView.as_view()),
    # path('comments/<int:pk>/', views.api_comment_detail),
    # path('comments/<int:pk>/', views.CommentDetailView.as_view()),
    # path('articles/', views.ArticleListView.as_view()),
    # path('articles/<int:pk>/', views.ArticleDetailView.as_view()),
    path('register/', views.UserRegistrationView.as_view()),
    path('login/', views.UserLoginView.as_view()),
]

urlpatterns += router.urls
