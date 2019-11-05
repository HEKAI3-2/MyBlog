from django.conf.urls import url, include
from blog import views

urlpatterns = [
	# 后台管理
	url(r'^backend/add_article/', views.add_article),
	# 点赞
	url(r'up_down/', views.up_down),
	url(r'comment/', views.comment),
	# 评论树状展示
	url(r'comment_tree/(\d+)/', views.comment_tree),

	# 文章详情页
	url(r'(\w+)/article/(\d+)/$', views.article_detail),
	# 个人博客路由
	url(r'(\w+)/$', views.home),

]