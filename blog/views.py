# coding=utf-8
from django.shortcuts import render, redirect, HttpResponse
# 使用forms内的文件生成HTML
from blog import forms, models
from django.contrib import auth
from django.http import JsonResponse
# 分组计数
from django.db.models import Count
from django.db.models import F
import json



# Create your views here.

# 自己生成验证码的登录
def login(request):
	# if request.is_ajax():  # 如果是AJAX请求
	if request.method == "POST":
		# 初始化一个给AJAX返回的数据
		ret = {"status": 0, "msg": ""}
		# 从提交过来的数据中 取到用户名和密码
		username = request.POST.get("username")
		pwd = request.POST.get("password")
		valid_code = request.POST.get("valid_code")  # 获取用户填写的验证码
		print(valid_code)
		print("用户输入的验证码".center(120, "="))
		if valid_code and valid_code.upper() == request.session.get("valid_code", "").upper():
			# 验证码正确
			# 利用auth模块做用户名和密码的校验
			user = auth.authenticate(username=username, password=pwd)
			if user:
				# 用户名密码正确
				# 给用户做登录
				auth.login(request, user)
				ret["msg"] = "/index/"
			else:
				# 用户名密码错误
				ret["status"] = 1
				ret["msg"] = "用户名或密码错误！"
		else:
			ret["status"] = 1
			ret["msg"] = "验证码错误"

		return JsonResponse(ret)
	return render(request, "login.html")


# 获取验证码图片的视图
def get_valid_img(request):
	# with open("valid_code.png", "rb") as f:
	#     data = f.read()
	# 自己生成一个图片
	from PIL import Image, ImageDraw, ImageFont
	import random

	# 获取随机颜色的函数
	def get_random_color():
		return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

	# 生成一个图片对象
	img_obj = Image.new(
		'RGB',
		(220, 35),
		get_random_color()
	)
	# 在生成的图片上写字符
	# 生成一个图片画笔对象
	draw_obj = ImageDraw.Draw(img_obj)
	# 加载字体文件， 得到一个字体对象
	font_obj = ImageFont.truetype("static/font/kumo.ttf", 28)
	# 开始生成随机字符串并且写到图片上
	tmp_list = []
	for i in range(5):
		u = chr(random.randint(65, 90))  # 生成大写字母
		l = chr(random.randint(97, 122))  # 生成小写字母
		n = str(random.randint(0, 9))  # 生成数字，注意要转换成字符串类型

		tmp = random.choice([u, l, n])
		tmp_list.append(tmp)
		draw_obj.text((20 + 40 * i, 0), tmp, fill=get_random_color(), font=font_obj)

	print("".join(tmp_list))
	print("生成的验证码".center(120, "="))
	# 不能保存到全局变量
	# global VALID_CODE
	# VALID_CODE = "".join(tmp_list)

	# 保存到session
	request.session["valid_code"] = "".join(tmp_list)
	# 加干扰线
	# width = 220  # 图片宽度（防止越界）
	# height = 35
	# for i in range(5):
	#     x1 = random.randint(0, width)
	#     x2 = random.randint(0, width)
	#     y1 = random.randint(0, height)
	#     y2 = random.randint(0, height)
	#     draw_obj.line((x1, y1, x2, y2), fill=get_random_color())
	#
	# # 加干扰点
	# for i in range(40):
	#     draw_obj.point((random.randint(0, width), random.randint(0, height)), fill=get_random_color())
	#     x = random.randint(0, width)
	#     y = random.randint(0, height)
	#     draw_obj.arc((x, y, x+4, y+4), 0, 90, fill=get_random_color())

	# 将生成的图片保存在磁盘上
	# with open("s10.png", "wb") as f:
	#     img_obj.save(f, "png")
	# # 把刚才生成的图片返回给页面
	# with open("s10.png", "rb") as f:
	#     data = f.read()

	# 不需要在硬盘上保存文件，直接在内存中加载就可以
	from io import BytesIO
	io_obj = BytesIO()
	# 将生成的图片数据保存在io对象中
	img_obj.save(io_obj, "png")
	# 从io对象里面取上一步保存的数据
	data = io_obj.getvalue()
	return HttpResponse(data)


# 注销
def logout(request):
	auth.logout(request)
	return redirect("/index/")


# 注销
def logout(request):
	auth.logout(request)
	return redirect("/index/")


# 注册的视图函数
def register(request):
	# from表单提交
	if request.method == "POST":
		# 定义一个字典做Ajax提交
		ret = {"status": 0, "msg": "", }

		# 接收提交过来的数据,只有正常的键值对，没有图像
		form_obj = forms.RegForm(request.POST)
		print(request.POST)
		# 帮我做校验,先校验内置的，在校验clean_开头的规则,整个循环走完，在调用clean()方法
		if form_obj.is_valid():
			# 校验成功，去数据库创建一个新的用户,models继承AbstractUser，使用creat_user
			# 多一个键值对，re_password
			form_obj.cleaned_data.pop('re_password')
			# 自己取文件、图片的数据
			avatar_img = request.FILES.get("avatar")
			# models.UserInfo.objects.create_user(avatar=avatar_img, **form_obj.cleaned_data)
			models.UserInfo.objects.create_user(avatar=avatar_img, **form_obj.cleaned_data)
			# 注册成功 跳转页面
			ret["msg"] = "/index/"
			return JsonResponse(ret)
		# return HttpResponse("注册成功")
		else:
			print(form_obj.errors)
			# 有错误将status给个值
			ret["status"] = 1
			# 错误封装到msg里面
			ret["msg"] = form_obj.errors
			return JsonResponse(ret)
	# return render(request, "register.html", {"form_obj": form_obj})
	# return HttpResponse("信息有误，注册失败")
	# 生成from对象
	form_obj = forms.RegForm()
	return render(request, "register.html", {"form_obj": form_obj})


def index(request):
	# 查询所有文章列表
	article_list = models.Article.objects.all()
	return render(request, "index.html", {"article_list": article_list})


# 校验用户名是否已经存在
def check_username_exist(request):
	ret = {"status": 0, "msg": "", }
	username = request.GET.get("username")
	is_exist = models.UserInfo.objects.filter(username=username)
	if is_exist:
		ret["status"] = 1
		ret["msg"] = "用户名已经被注册"
	return JsonResponse(ret)


# 个人博客主页
def home(request, username):
	# 拿到username
	# print(username)
	user = models.UserInfo.objects.filter(username=username).first()
	if not user:
		return HttpResponse("404")

	# 用户存在，找出所有用户写的所有文章
	blog = user.blog
	article_list = models.Article.objects.filter(user=user)
	# 文章分类及每个分类下的文章数，分类查文章
	# 拿到文章分类列表
	# category_list = models.Category.objects.filter(blog=blog)
	# 分组
	category_list = category_list = models.Category.objects.filter(blog=blog).annotate(c=Count("article")).values(
		"title", "c")
	# <QuerySet [{'title': '技术', 'c': 0}, {'title': '斗鱼', 'c': 1}]>
	# print(ret)
	# 基于Queryset查询不需要加set
	# models.Category.objects.filter(blog=blog).values("article_title")
	# print(category_list)

	# 拿到标签列表及分类
	tag_list = models.Tag.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c")
	# 按日期归档
	archive_list = models.Article.objects.filter(user=user).extra(
		# 需要转义%
		select={"archive_ym": "date_format(create_time,'%%Y-%%m')"}
	).values("archive_ym").annotate(c=Count("nid")).values("archive_ym", "c")
	return render(request, 'home.html', {
		'blog': blog,
		"article_list": article_list,
		# "category_list": category_list,
		"category_list": category_list,
		"tag_list": tag_list,
		"archive_list": archive_list,
	})


# 左侧边框
def get_left_menu(username):
	user = models.UserInfo.objects.filter(username=username).first()
	if not user:
		return HttpResponse("404")
	blog = user.blog
	category_list = category_list = models.Category.objects.filter(blog=blog).annotate(c=Count("article")).values(
		"title", "c")
	# 拿到标签列表及分类
	tag_list = models.Tag.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c")
	# 按日期归档
	archive_list = models.Article.objects.filter(user=user).extra(
		# 需要转义%
		select={"archive_ym": "date_format(create_time,'%%Y-%%m')"}
	).values("archive_ym").annotate(c=Count("nid")).values("archive_ym", "c")
	return category_list, tag_list, archive_list


# 文章详情
def article_detail(request, username, pk):
	"""

	:param request:
	:param username:用户
	:param pk:文章主键
	:param
	:return:article_list:评论
	"""
	user = models.UserInfo.objects.filter(username=username).first()
	if not user:
		return HttpResponse("404")
	blog = user.blog
	article_obj = models.Article.objects.filter(pk=pk).first()
	# print(blog)
	category_list, tag_list, archive_list = get_left_menu(username)

	comment_list = models.Comment.objects.filter(article_id=pk)
	return render(request, "article_detail.html", {
		"article": article_obj,
		"blog": blog,
		"category_list": category_list,
		"tag_list": tag_list,
		"archive_list": archive_list,
		"comment_list": comment_list,
	})


def up_down(request):
	print(request.POST)
	article_id = request.POST.get("article_id")
	is_up = json.loads(request.POST.get("is_up"))
	response = {"state": True}
	# 点赞的人
	user = request.user
	# 写入数据库
	try:
		models.ArticleUpDown.objects.create(user=user, article_id=article_id, is_up=is_up)
		if is_up:
			models.Article.objects.filter(pk=article_id).update(up_count=F("up_count") + 1)
		else:
			models.Article.objects.filter(pk=article_id).update(down_count=F("down_count") + 1)
	except Exception as e:
		response["state"] = False
		response['first_action'] = models.ArticleUpDown.objects.filter(user=user, article_id=article_id).first().is_up
		print(response)

	# 发ajax就返回字典
	return JsonResponse(response)


def comment(request):
	print(request.POST)
	pid = request.POST.get("pid")
	article_id = request.POST.get("article_id")
	content = request.POST.get("content")
	user_pk = request.user.pk
	respose = {}
	if not pid:
		# 根评论
		commemt_obj = models.Comment.objects.create(article_id=article_id, user_id=user_pk, content=content)
	else:
		commemt_obj = models.Comment.objects.create(article_id=article_id, user_id=user_pk, content=content,
													parent_comment_id=pid)
	respose["create_time"] = commemt_obj.create_time.strftime("%Y-%m-%d")
	respose["content"] = commemt_obj.content
	respose["username"] = commemt_obj.user.username
	return JsonResponse(respose)


def comment_tree(request, article_id):
	ret = list(models.Comment.objects.filter(article_id=article_id).values("pk", "content", "parent_comment_id"))
	print(ret)
	return JsonResponse(ret, safe=False)


def add_article(request):
	if request.method == "POST":
		title = request.POST.get('title')
		article_content = request.POST.get('article_content')
		user = request.user

		from bs4 import BeautifulSoup

		bs = BeautifulSoup(article_content, "html.parser")
		desc = bs.text[0:150] + "..."

		# 过滤非法标签
		for tag in bs.find_all():

			print(tag.name)

			if tag.name in ["script", "link"]:
				tag.decompose()

		article_obj = models.Article.objects.create(user=user, title=title, desc=desc)
		models.ArticleDetail.objects.create(content=str(bs), article=article_obj)

		return HttpResponse("添加成功")

	return render(request, 'add_article.html')


from bbs import settings
import os, json


def upload(request):
	print(request.FILES)
	obj = request.FILES.get("upload_img")

	print("name", obj.name)

	path = os.path.join(settings.MEDIA_ROOT, "add_article_img", obj.name)

	with open(path, "wb") as f:
		for line in obj:
			f.write(line)

	res = {
		"error": 0,
		"url": "/media/add_article_img/" + obj.name
	}

	return HttpResponse(json.dumps(res))
	# return HttpResponse("OK")
