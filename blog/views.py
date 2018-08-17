#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from . import models
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import time
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# 导入分页相关模块
import qrcode
from io import *
import base64

def index(request):
	articles = models.Article.objects.filter(category=1)
	blogintros = models.BlogIntro.objects.all()
	return render(request,'blog/index.html',{'blogintros':blogintros,'articles':articles})

def generic(request):
	return render(request,'blog/generic.html')

def elementpage(request):
	return render(request,'blog/elements.html')

def article_page(request,article_id):
	article = models.Article.objects.get(pk=article_id)
	# author = models.Author.get(nickname=article['author'])
	# others = author.article_set.all()
	qr_url = request.path
	img = qrcode.make('http://39.108.166.148:8000'+qr_url)
	buf = BytesIO()
	img.save(buf)
	image_stream = buf.getvalue()
	codeimg = base64.b64encode(image_stream)
	codeimg = str(codeimg)
	codeimg = codeimg[2:-1]
	return render(request,'blog/article_page.html',{'article':article,'codeimg':codeimg,})


def apply_author(request):
	return render(request,'blog/apply_author.html')

def author(request,author_id):
	author = models.Author.objects.get(pk=author_id)
	return render(request,'blog/author.html',{'author':author})

def authors(request):
	authors = models.Author.objects.filter(op=True)
	return render(request,'blog/authors.html',{'authors':authors})

def hello(request):
	curtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime());
	try:
		if request == 'POST':
			username = request.POST.get('name','')
			password1 = request.POST.get('password1','')
			password1 = request.POST.get('password1','')
			email = request.POST.get('email','')
			errors = []
			#注册表单传过来的数据需要一些基本的验证
			registerForm=RegisterForm({'username':username,'password1':password1,'password2':password2,'email':email})
			if not registerForm.is_valid():
				errors.extend(registerForm.errors.values())
				return render_to_response("blog/userregister.html",RequestContext(request,{'curtime':curtime,'username':username,'email':email,'errors':errors}))
			if password1!=password2:
				errors.append("两次输入的密码不一致!")
				return render_to_response("blog/userregister.html",RequestContext(request,{'curtime':curtime,'username':username,'email':email,'errors':errors}))
				#用User模型查找要注册的用户名是否存在，如果用户已经存在就需要提示注册的客户更换用户名
			filterResult=User.objects.filter(username=username)

			if len(filterResult)>0:
				errors.append("用户名已存在")
				return render_to_response("blog/userregister.html",RequestContext(request,{'curtime':curtime,'username':username,'email':email,'errors':errors}))
			#直接利用User模型把通过验证的用户数据存入数据库
            #需要注意的是，保存密码信息时需要使用set_password方法（因为这里有个加密的过程）	
			user=User()
			user.username=username
			user.set_password(password1)
			user.email=email
			user.save()
			#用户扩展信息 profile
            #存储用户的扩展信息（这里是用户的电话号码），这里用到自定义的用户扩展模型UserProfile
			profile=UserProfile()
			profile.user_id=user.id
			profile.save()
			#用户登录前需要先进行验证，要不然会出错
			newUser=auth.authenticate(username=username,password=password1)
			if newUser is not None:
				auth.login(request, newUser)#用户登陆
				return HttpResponseRedirect("/")
	except Exception as e:
		errors.append(str(e))
		return render(request,"blog/hello.html",{'curtime':curtime,'username':username,'email':email,'errors':errors})
	return render(request,"blog/hello.html",{'curtime':curtime})

def listing(request):
	article_list = models.Article.objects.all()
	paginator = Paginator(article_list,10)
	#每页10条数据
	page = request.GET.get('page')
	#获取前台传来的页码参数
	try:
		articles = paginator.page(page)
		#返回前台传来的页码编号
	except PageNotAnInteger:
		articles = paginator.page(1)
		#如果没有页码，默认第一次访问，返回第一页
	except EmptyPage:
		articles = paginator.page(paginator.num_pages)
		#如果页码超出范围，则返回最后一页
	return render(request,'blog/articles.html',{'articles':articles})