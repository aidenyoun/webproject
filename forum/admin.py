from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'content', 'views', 'created_at', 'updated_at')
    list_filter = ('category',)

admin.site.register(Post, PostAdmin)
