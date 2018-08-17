from django.contrib import admin
from django.contrib.auth.admin import User
from .models import Article,BlogIntro,Author,UserProfile,Tag,Category
# Register your models here.
# 
class AuthorAdmin(admin.ModelAdmin):
	list_display = ('retime',)
	list_filter = ('retime',)
class ArticleAdmin(admin.ModelAdmin):
	list_display = ('title','author','pagetime')
	list_filter = ('pagetime','author','tags')
admin.site.register(Article,ArticleAdmin)
admin.site.register(BlogIntro)
admin.site.register(Author,AuthorAdmin)
admin.site.register(Tag)
admin.site.register(Category)


