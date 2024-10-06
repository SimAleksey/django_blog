from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from blog_app.models import Category, Comment, Article, Todo
import json
from rest_framework.decorators import api_view
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    ArticleSerializer,
    UserRegistrationSerializer,
    TodoSerializer,
    UserLoginSerializer
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView


@extend_schema(tags=['Auth'])
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()

    serializer_class = UserRegistrationSerializer


@extend_schema(tags=['Auth'])
class UserLoginView(APIView):
    def post(self, request):
        user = authenticate(
            username=request.data['username'],
            password=request.data['password']
        )
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'})


def api_root(request):
    endpoints = [
        'categories/',
        'categories/{pk}/',
        'comments/',
        'comments/{pk}/',
    ]
    return JsonResponse(endpoints, safe=False)


# def api_categories_list(request):
#     result = []
#     categories = Category.objects.all()
#     for category in categories:
#         result.append({
#             'id': category.pk,
#             'title': category.title,
#             'slug': category.slug
#         })
#
#     return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')


# @api_view(['GET', 'POST'])
# def api_categories_list(request):
#     if request.method == 'GET':
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, many=True)
#         return Response(serializer.data)
#     else:
#         serializer = CategorySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)


class CategoryListView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# @api_view(['GET', 'PUT', 'DELETE'])
# def api_category_detail(request, pk):
#     category = Category.objects.get(pk=pk)
#     if request.method == 'GET':
#         serializer = CategorySerializer(category, many=False)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CategorySerializer(category, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         category.delete()
#         return Response('deleted')


# @api_view(['GET'])
# def api_comments_list(request):
#     comments = Comment.objects.all()
#     serializer = CommentSerializer(comments, many=True)
#     return Response(serializer.data)


class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# @api_view(['GET'])
# def api_comment_detail(request, pk):
#     comment = Comment.objects.get(pk=pk)
#     serializer = CommentSerializer(comment, many=False)
#     return Response(serializer.data)


class ArticleListView(generics.ListCreateAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


@extend_schema(tags=['Categories'])
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@extend_schema(tags=['Comments'])
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


@extend_schema(tags=['Articles'])
class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('category', 'author')
    ordering_fields = ('views', 'created_at')


@extend_schema(tags=['Todo'])
class TodoViewSet(ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
