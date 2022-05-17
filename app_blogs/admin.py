from django.contrib import admin

from app_blogs.models import Blog, BlogAuthor, BlogModerator, BlogArticle


class AdminBlog(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at']
    list_display_links = ['id', 'title', 'created_at']


class AdminBlogAuthor(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']


class AdminBlogModerator(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']


class AdminBlogArticle(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at']
    list_display_links = ['id', 'title', 'created_at']


admin.site.register(Blog, AdminBlog)
admin.site.register(BlogAuthor, AdminBlogAuthor)
admin.site.register(BlogModerator, AdminBlogModerator)
admin.site.register(BlogArticle, AdminBlogArticle)