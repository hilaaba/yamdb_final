from django.contrib import admin

from .models import Category, Comment, Genre, GenreTitle, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


class TitleAdmin(admin.ModelAdmin):
    pass
    list_display = ('name', 'year', 'category')
    search_fields = ('name', 'category__name', 'description')
    list_filter = ('year', 'category')


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('genre', 'title')
    search_fields = ('genre', 'title')
    list_filter = ('title',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'score', 'title')
    search_fields = ('text', 'title__name')
    list_filter = ('author', 'score')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'review')
    list_filter = ('author',)
    search_fields = ('review__text', 'text')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
