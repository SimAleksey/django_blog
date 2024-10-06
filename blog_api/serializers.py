from rest_framework import serializers
from blog_app.models import Category, Comment, Article, Todo
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


# class CategorySerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField()
#     slug = serializers.SlugField(read_only=True)
#
#     def create(self, validated_data):
#         category = Category.objects.create(
#             title=validated_data['title'],
#             slug=validated_data['slug']
#         )
#         category.save()
#         return category
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data['title']
#         instance.slug = slugify(validated_data['title'])
#         instance.save()
#         return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']


# class CommentSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     text = serializers.CharField()
#     created_at = serializers.DateTimeField(read_only=True)
#     author = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all()
#     )
#     article = serializers.PrimaryKeyRelatedField(
#         queryset=Article.objects.all()
#     )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at', 'author', 'article']


# class ArticleSerializer(serializers.Serializer):
#     title = serializers.CharField()
#     short_description = serializers.CharField()
#     full_description = serializers.CharField()
#     views = serializers.IntegerField(read_only=True)
#     preview = serializers.ImageField()
#     created_at = serializers.DateTimeField(read_only=True)
#     updated_at = serializers.DateTimeField(read_only=True)
#     category = serializers.PrimaryKeyRelatedField(
#         queryset=Category.objects.all()
#     )
#     author = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all()
#     )
#     slug = serializers.SlugField(read_only=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class UserLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']


class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        required=True,
        write_only=True,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        password = attrs.pop('password')
        password2 = attrs.pop('password2')
        if password != password2:
            raise serializers.ValidationError(detail='Пароли должны быть одинаковыми')

        attrs['password'] = password
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)

        user.set_password(password)
        user.save()
        return user


class ArticleSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'short_description', 'full_description', 'views', 'preview',
                  'created_at', 'updated_at', 'category', 'author', 'comments', 'likes', 'dislikes']
        read_only_fields = ['views']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        category = Category.objects.get(pk=instance.category.id)
        user = User.objects.get(pk=instance.author.id)
        category_serialized = CategorySerializer(category, many=False)
        user_serialized = UserSerializer(user, many=False)
        data['category'] = category_serialized.data
        data['author'] = user_serialized.data

        return data


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['title', 'user', 'description', 'created_at', 'is_finished']
        read_only_fields = ['user']