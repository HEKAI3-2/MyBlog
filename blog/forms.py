# coding=utf-8
"""bbs用到的form类"""

from django import forms
# 从from组件导入widgets属性
from django.forms import widgets
# 导入错误类
from django.core.exceptions import ValidationError
# 导入models
from blog import models


# 定义一个注册的from类

class RegForm(forms.Form):
	username = forms.CharField(
		# 限制信息
		max_length=16,
		label="用户名",
		# 错误提示
		error_messages={
			"max_length": "用户名最长16位",
			"required": "用户名不能为空",
		},
		# 设定input框的样式
		widget=forms.widgets.TextInput(
			attrs={"class": "form-control"}
		)
	)

	password = forms.CharField(
		min_length=6,
		label="密码",
		widget=forms.widgets.PasswordInput(
			attrs={"class": "form-control"},
			# 输入密码不消失
			render_value=True,
		),
		# 错误提示
		error_messages={
			"min_length": "密码最少6位",
			"required": "密码不能为空",
		}
	)

	re_password = forms.CharField(
		min_length=6,
		label="确认密码",
		widget=forms.widgets.PasswordInput(
			attrs={"class": "form-control"},
			# 输入密码不消失
			render_value=True,
		),
		# 错误提示
		error_messages={
			"min_length": "密码最少6位",
			"required": "密码不能为空",
		}
	)

	email = forms.EmailField(
		label="邮箱",
		widget=forms.widgets.EmailInput(
			attrs={"class": "form-control"}
		),
		error_messages={
			'invalid': "邮箱格式不正确",
			"required": "邮箱不能为空",
		}
	)

	# 重写username字段的局部钩子
	def clean_username(self):
		# 检测数据库中是否有相同的username
		# 找到提交的username
		username = self.cleaned_data.get("username")
		# 从数据库找是否有相同数据
		is_exist = models.UserInfo.objects.filter(username=username)
		if is_exist:
			# 表示用户名已注册
			# ret["status"] = 1
			# ret["msg"] = "用户名已经存在"
			# return JsonResponse(ret)
			self.add_error("username", ValidationError("用户名已存在"))
		else:
			return username

	# 重写username字段的局部钩子
	def clean_email(self):
		# 检测数据库中是否有相同的email
		# 找到提交的email
		email = self.cleaned_data.get("email")
		# 从数据库找是否有相同数据
		is_exist = models.UserInfo.objects.filter(email=email)
		if is_exist:
			self.add_error("email", ValidationError("邮箱已存在"))
		else:
			# 必须有返回值，不然会出现raise ValueError('The given username must be set')错误
			return email

	# 重写全局钩子函数，对确认密码做校验
	def clean(self):
		password = self.cleaned_data.get("password")
		re_password = self.cleaned_data.get("re_password")
		if re_password and re_password != password:
			self.add_error("re_password", ValidationError("两次密码不一致"))
		# 没错误直接返回
		else:
			return self.cleaned_data

		'''
	def _clean_form(self):
		try:
            cleaned_data = self.clean()
        except ValidationError as e:
            self.add_error(None, e)
        else:
            if cleaned_data is not None:
                self.cleaned_data = cleaned_data
		'''
