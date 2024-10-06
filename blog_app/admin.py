from django.contrib import admin
from .models import Category, Article, Comment, SearchHistory, Todo


# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug']
    list_display_links = ['id', 'title']
    prepopulated_fields = {'slug': ('title',)}


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'views', 'created_at', 'updated_at', 'category', 'author']
    list_display_links = ['id', 'title']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views']
    list_editable = ['category', 'author']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'article', 'author']
    list_filter = ['article']

class TodoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'created_at', 'user']
    list_display_links = ['id']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(SearchHistory)
admin.site.register(Todo, TodoAdmin)
