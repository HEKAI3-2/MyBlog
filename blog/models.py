# coding=utf-8
from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
	""" 用户信息表"""
	nid = models.AutoField(primary_key=True)
	phone = models.CharField(max_length=11, null=True, unique=True)
	# 传入的文件都上传到avatars文件夹下
	avatar = models.FileField(upload_to="avatars/", default="avatars/default.png", verbose_name="头像")
	create_time = models.DateTimeField(auto_now_add=True)

	blog = models.OneToOneField(to="Blog", to_field="nid", null=True)

	def __str__(self):
		return self.username

	# admin表设置中文
	class Meta:
		# 因为是英文系的，后面会多个s
		verbose_name = "用户信息"
		# 显示复数的时候也显示这个
		verbose_name_plural = verbose_name


class Blog(models.Model):
	"""
	博客信息
	"""
	nid = models.AutoField(primary_key=True)
	title = models.CharField(max_length=64)  # 个人博客标题
	site = models.CharField(max_length=32, unique=True)  # 个人博客后缀
	theme = models.CharField(max_length=32)  # 博客主题

	def __str__(self):
		return self.title

	class Meta:
		# 因为是英文系的，后面会多个s
		verbose_name = "blog站点"
		# 显示复数的时候也显示这个
		verbose_name_plural = verbose_name


class Category(models.Model):
	"""
	个人博客文章分类
	"""
	nid = models.AutoField(primary_key=True)
	title = models.CharField(max_length=32)  # 分类标题
	blog = models.ForeignKey(to="Blog", to_field="nid")  # 外键关联博客，一个博客站点可以有多个分类

	def __str__(self):
		return self.title

	class Meta:
		# 因为是英文系的，后面会多个s
		verbose_name = "文章分类"
		# 显示复数的时候也显示这个
		verbose_name_plural = verbose_name


class Tag(models.Model):
	"""
	标签
	"""
	nid = models.AutoField(primary_key=True)
	title = models.CharField(max_length=32)  # 标签名
	blog = models.ForeignKey(to="Blog", to_field="nid")  # 所属博客

	def __str__(self):
		return self.title

	class Meta:
		# 因为是英文系的，后面会多个s
		verbose_name = "标签"
		# 显示复数的时候也显示这个
		verbose_name_plural = verbose_name


class Article(models.Model):
	"""
	文章
	"""
	nid = models.AutoField(primary_key=True)
	# 在这里设置中文显示verbose_name
	title = models.CharField(max_length=50, verbose_name="文章标题")  # 文章标题
	desc = models.CharField(max_length=255)  # 文章描述
	create_time = models.DateTimeField()  # 创建时间
	# 为了简化查找，不用跨表查询
	# 评论数
	comment_count = models.IntegerField(verbose_name="评论数",default=0)
	# 点赞数
	up_count = models.IntegerField(verbose_name="点赞数",default=0)
	# 踩
	down_count = models.IntegerField(verbose_name="踩数",default=0)

	category = models.ForeignKey(to="Category", to_field="nid", null=True)
	user = models.ForeignKey(to="UserInfo", to_field="nid")
	tags = models.ManyToManyField(  # 中介模型
		to="Tag",
		through="Article2Tag",
		through_fields=("article", "tag"),  # 注意顺序！！！
	)

	def __str__(self):
		return self.title

	class Meta:
		# 因为是英文系的，后面会多个s
		verbose_name = "文章"
		# 显示复数的时候也显示这个
		verbose_name_plural = verbose_name


class ArticleDetail(models.Model):
	"""
	文章详情表
	"""
	nid = models.AutoField(primary_key=True)
	content = models.TextField()
	article = models.OneToOneField(to="Article", to_field="nid")

	class Meta:
		# 因为是英文系的，后面会多个s
		verbose_name = "文章详情"
		# 显示复数的时候也显示这个
		verbose_name_plural = verbose_name


class Article2Tag(models.Model):
	"""
	文章和标签的多对多关系表
	"""
	nid = models.AutoField(primary_key=True)
	article = models.ForeignKey(to="Article", to_field="nid")
	tag = models.ForeignKey(to="Tag", to_field="nid")

	def __str__(self):
		return "{}---{}".format(self.article.title,self.tag.title)

	class Meta:
		unique_together = (("article", "tag"),)
		# 因为是英文系的，后面会多个s
		verbose_name = "文章-标签"
		# 显示复数的时候也显示这个
		verbose_name_plural = verbose_name


class ArticleUpDown(models.Model):
	"""
	点赞表
	"""
	nid = models.AutoField(primary_key=True)
	user = models.ForeignKey(to="UserInfo", null=True)
	article = models.ForeignKey(to="Article", null=True)
	is_up = models.BooleanField(default=True)

	class Meta:
		unique_together = (("article", "user"),)
		# 因为是英文系的，后面会多个s
		verbose_name = "文章点赞"
		# 显示复数的时候也显示这个
		verbose_name_plural = verbose_name


class Comment(models.Model):
	"""
	评论表
	"""
	nid = models.AutoField(primary_key=True)
	article = models.ForeignKey(to="Article", to_field="nid")
	user = models.ForeignKey(to="UserInfo", to_field="nid")
	content = models.CharField(max_length=255)  # 评论内容
	create_time = models.DateTimeField(auto_now_add=True)
	# admin里面可以不填
	parent_comment = models.ForeignKey("self", null=True, blank=True)

	def __str__(self):
		return self.content

	class Meta:
		# 因为是英文系的，后面会多个s
		verbose_name = "评论"
		# 显示复数的时候也显示这个
		verbose_name_plural = verbose_name
