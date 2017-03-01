# coding:utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic import View
from django.contrib.auth.hashers import make_password
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from operation.models import UserCourse, UserFavorite, Course, UserMessage
from organization.models import CourseOrg, Teacher
from .models import UserProfile
from .forms import LoginForm, RegisterForm, UploadImageForm
from utils.mixin_utils import LoginRequiredMixin


# Create your views here.

class CustomBackend(ModelBackend):
	def authenticate(self, username=None, password=None, **kwargs):
		try:
			user = UserProfile.objects.get(Q(username=username) | Q(email=username))
			if user.check_password(password):
				return user
		except Exception as e:
			return None


class RegisterView(View):
	def get(self, request):
		register_form = RegisterForm()
		return render(request, "register.html", {'register_form': register_form})
	
	def post(self, request):
		register_form = RegisterForm(request.POST)
		if register_form.is_valid():
			user_name = request.POST.get("username", "")
			pass_word = request.POST.get("password", "")
			user_profile = UserProfile()
			user_profile.username = user_name
			user_profile.email = user_name
			user_profile.password = make_password(pass_word)
			user_profile.save()


class LogoutView(View):
	def get(self, request):
		logout(request)
		from django.core.urlresolvers import resolve
		return HttpResponseRedirect(resolve('index'))


class LoginView(View):
	def get(self, request):
		return render(request, "login.html", {})
	
	def post(self, request):
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			
			user_name = request.POST.get("username", "")
			pass_word = request.POST.get("password", "")
			user = authenticate(username=user_name, password=pass_word)
			if user is not None:
				login(request, user)
				return render(request, "index.html", {})
			else:
				return render(request, "login.html", {"msg": "用户名或密码错误!"})
		else:
			print login_form
			return render(request, "login.html", {"login_form": login_form})


class UserInfoView(LoginRequiredMixin, View):
	"""用户信息"""
	
	def get(self, request):
		return render(request, 'usercenter-info.html', {})


class UploadImageView(LoginRequiredMixin, View):
	"""用户修改头像"""
	
	def post(self, request):
		image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
		
		if image_form.is_valid():
			# image = image_form.cleaned_data['image']
			# request.user.image = image
			image_form.save()
			
			return HttpResponse('{"status":"success",}', content_type='application/json')
		else:
			return HttpResponse('{"status":"fail",}', content_type='application/json')
		
		# return render(request, 'usercenter-info.html', {})


class MyCourseView(LoginRequiredMixin, View):
	"""我的课程"""
	
	def get(self, request):
		user_course = UserCourse.objects.filter(user=request.user)
		return render(request, 'usercenter-mycourse.html', {
			'user_course': user_course,
		})


class MyFavOrgView(LoginRequiredMixin, View):
	"""我的收藏 Org"""
	
	def get(self, request):
		org_list = []
		fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
		for fav_org in fav_orgs:
			org_id = fav_org.fav_id
			org = CourseOrg.objects.get(id=org_id)
			org_list.append(org)
		
		return render(request, 'usercenter-fav-org.html', {
			'org_list': org_list,
		})


class MyFavTeacherView(LoginRequiredMixin, View):
	"""我的收藏 teacher"""
	
	def get(self, request):
		teacher_list = []
		fav_teacher = UserFavorite.objects.filter(user=request.user, fav_type=3)
		for teacher in fav_teacher:
			teacher_id = teacher.fav_id
			teacher = Teacher.objects.get(id=teacher_id)
			teacher_list.append(teacher)
		
		return render(request, 'usercenter-fav-teacher.html', {
			'teacher_list': teacher_list,
		})


class MyFavCourseView(LoginRequiredMixin, View):
	"""我的收藏 course"""
	
	def get(self, request):
		course_list = []
		fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
		for fav_course in fav_courses:
			course_id = fav_course.fav_id
			course = Course.objects.get(id=course_id)
			course_list.append(course)
		
		return render(request, 'usercenter-fav-course.html', {
			'course_list': course_list,
		})


class MymessgaeView(LoginRequiredMixin, View):
	"""我的收藏 course"""
	
	def get(self, request):
		all_message = UserMessage.objects.all()
		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1
		
		p = Paginator(all_message, 3, request=request)
		
		message = p.page(page)
		
		return render(request, 'usercenter-message.html', {
			'message': message,
			
		})
