from django.contrib import admin

from .models import Profile, Article, Subjects, ProfilePhoto, MatchedLikes


class ArticleAdmin(admin.ModelAdmin):
    """Class allow 'created' display"""
    readonly_fields = ('created',)


admin.site.register(Article, ArticleAdmin)
admin.site.register(Profile)
admin.site.register(Subjects)
# admin.site.register(ProfilePhoto)
admin.site.register(MatchedLikes)
