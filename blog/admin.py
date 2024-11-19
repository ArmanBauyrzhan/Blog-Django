from django.contrib import admin
from .models import Post, Comment, Tag, Subscription

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at', 'is_public', 'is_visible_on_request')
    list_filter = ('is_public', 'is_visible_on_request', 'created_at', 'tags')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'content', 'created_at')
    list_filter = ('created_at', 'post')
    search_fields = ('content', 'user__username', 'post__title')
    prepopulated_fields = {'slug': ('content',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'subscribed_to')
    list_filter = ('subscriber', 'subscribed_to')
    search_fields = ('subscriber__username', 'subscribed_to__username')
