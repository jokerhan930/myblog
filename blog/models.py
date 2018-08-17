from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class UserProfile(models.Model):  
    user=models.OneToOneField(User,unique=True,verbose_name=('用户'),on_delete=models.CASCADE)  
    def __str__(self):
    	return self.user.username

class Tag(models.Model):
	name = models.CharField(max_length=32)
	def __str__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(max_length=32)
	def __str__(self):
		return self.name

class Author(models.Model):
	nickname = models.OneToOneField(User,verbose_name=('用户'),on_delete=models.CASCADE)
	sex = models.NullBooleanField()
	ace = models.NullBooleanField()
	op = models.NullBooleanField()
	email = models.EmailField(max_length=75,default="xxxx@xx.com")
	avatar = models.ImageField(null=True,blank=True)
	description = models.TextField(null=False,default="这个人很懒，啥都没说！")
	retime = models.DateField(auto_now_add=True)
	passagenum = models.IntegerField()
	fansnum = models.IntegerField()
	def __str__(self):
		return self.nickname.username

class Article(models.Model):
	title = models.CharField(max_length=32,default="标题")
	subs = models.TextField(null=False,default="简介")
	content = models.TextField(null=True)
	email = models.EmailField(max_length=75,default="xxxx@xx.com")
	image = models.ImageField(upload_to="photos",default="none")
	author = models.ForeignKey(Author,on_delete=models.CASCADE)
	#作者字段 外键 一对多 对应Author表
	pagetime = models.DateField(auto_now_add=True)
	tags = models.ManyToManyField(Tag, blank=True)
	#标签字段 外键 多对多 数据库中会新建 article_tags表
	category = models.ForeignKey(Category,on_delete=models.CASCADE)
	#目录字段 外键 一对多 对应Category表
	thumup = models.IntegerField(default=0)
	views = models.PositiveIntegerField(default=0)
	def increase_views(self):
		self.views += 1
		self.save(update_fields=['views'])
	#views 访问量字段 随访问自增
	def __str__(self):
		return self.title

class Comment(models.Model):
	belong_user = models.ForeignKey(User,related_name="User",on_delete=models.CASCADE)
	belong_article = models.ForeignKey(Article,related_name="Article",on_delete=models.CASCADE)
	content = models.TextField(null=False)
	msgtime = models.DateField(auto_now_add=True)
	def __str__(self):
		return self.text[:20]

class BlogIntro(models.Model):
	icon = models.CharField(max_length=24,default="iconname")
	title = models.CharField(max_length=32,default="介绍")
	content = models.TextField(null=True)
	def __str__(self):
		return self.title