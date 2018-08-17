from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index),
    path('generic/', views.generic),
    path('elements/',views.elementpage),
    path('article/<int:article_id>/', views.article_page,name ='article_page'),
    path('apply_author/',views.apply_author),
    path('authors/',views.authors),
    path('author/<int:author_id>/',views.author,name = "author"),
    path('hello/',views.hello),
    path('articles/',views.listing),
] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)