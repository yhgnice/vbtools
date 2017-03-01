# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse
from django.views.generic.base import View
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from operation.models import UserFavorite, CourseComments, UserCourse
from .models import Course, CourseOrg, Teacher, Video, Lesson, CourseResource
from utils.mixin_utils import LoginRequiredMixin



# Create your views here.

class CourseListView(View):
	def get(self, request):
		all_course = Course.objects.all().order_by("-add_time")
		hot_course = Course.objects.all().order_by("-click_nums")[:3]
		
		
		# 课程搜索
		search_keywords = request.GET.get('keywords',"")
		
		if search_keywords:
			all_course =all_course.filter(Q(name__icontains=search_keywords)|
			                              Q(desc__icontains=search_keywords)|
			                              Q(detail__icontains=search_keywords))
			
		
		
		sort = request.GET.get('sort', "")
		# 课程排序
		if sort:
			if sort == 'students':
				
				all_course = all_course.order_by("-students")
			elif sort == 'hot':
				all_course = all_course.order_by("-click_nums")
			else:
				pass
		
		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1
		
		p = Paginator(all_course, 3, request=request)
		
		all_course = p.page(page)
		return render(request, "course-list.html", {
			'all_course': all_course,
			'sort': sort,
			'hot_course': hot_course,
		})


class CourseDetailView(View):
	"""课程详情页"""
	
	def get(self, request, course_id):
		course = Course.objects.get(id=int(course_id))
		course.click_nums += 1
		course.save()
		
		# 热门推荐
		tag = course.tag
		if tag:
			relate_course = Course.objects.filter(tag=tag)[:2]
		else:
			relate_course = []
		
		# 用户收藏
		has_fav_course = False
		has_fav_org = False
		
		if request.user.is_authenticated():
			if UserFavorite.objects.filter(user_id=request.user, fav_id=course.id, fav_type=1):
				has_fav_course = True
			if UserFavorite.objects.filter(user_id=request.user, fav_id=course.course_org.id, fav_type=2):
				has_fav_org = True
		
		return render(request, "course-detail.html", {
			'course': course,
			'relate_course': relate_course,
			'has_fav_course': has_fav_course,
			'has_fav_org': has_fav_org,
			
		})


class CourseInfolView(LoginRequiredMixin, View):
	"""课程章节信息"""
	
	def get(self, request, course_id):
		
		course = Course.objects.get(id=int(course_id))
		course.students +=1
		course.save()
		# 查询用户是否已经关联了该课程
		
		user_courses = UserCourse.objects.filter(user=request.user, course=course)
		if not user_courses:
			user_course = UserCourse(user=request.user, course=course)
			user_course.save()
		
		all_resource = CourseResource.objects.filter(course=course)
		
		return render(request, "course-video.html", {
			'course': course,
			'all_resource': all_resource,
			
		})


class CourseCommentlView(LoginRequiredMixin, View):
	"""课程评论信息"""
	
	def get(self, request, course_id):
		course = Course.objects.get(id=int(course_id))
		user_courses = UserCourse.objects.filter(course=course)
		user_ids = [user_course.user.id for user_course in user_courses]
		# 取出所有课程ID
		all_user_course = UserCourse.objects.filter(user__in=user_ids)
		
		course_ids = [user_course.course.id for user_course in user_courses]
		# 学过此课程用户还学过其他的课程
		relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")
		all_resource = CourseResource.objects.filter(course=course)
		return render(request, "course-comment.html", {
			'course': course,
			'all_resource': all_resource,
			'relate_courses': relate_courses,
		})


class AddCommentlView(View):
	"""添加评论信息"""
	
	def post(self, request):
		if not request.user.is_authenticated():
			return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
		
		course_id = request.POST.get("course_id", 0)
		comments = request.POST.get("comments", "")
		if course_id > 0 and comments:
			course_comments = CourseComments()
			course = Course.objects.get(id=int(course_id))
			course_comments.course = course
			course_comments.user = request.user
			course_comments.comment = comments
			course_comments.save()
			
			return HttpResponse('{"status":"success","msg":"添加成功"}', content_type='application/json')
		else:
			return HttpResponse('{"status":"fail","msg":"添加失败"}', content_type='application/json')


class VideoPlayView(LoginRequiredMixin, View):
	"""视频播放页面"""
	
	def get(self, request, video_id):
    
		video  = Video.objects.get(id=int(video_id))
		course = video.lesson.course
		course.students +=1
		course.save()
		# 查询用户是否已经关联了该课程
		
		user_courses = UserCourse.objects.filter(user=request.user, course=course)
		if not user_courses:
			user_course = UserCourse(user=request.user, course=course)
			user_course.save()
		
		all_resource = CourseResource.objects.filter(course=course)
		
		return render(request, "course-play.html", {
			'course': course,
			'all_resource': all_resource,
			'video': video,
			
		})

