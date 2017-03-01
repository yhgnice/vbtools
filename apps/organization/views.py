# coding:utf-8
from django.db.models import Q
from django.shortcuts import render, HttpResponse
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from courses.models import Course
from .models import CourseOrg, Teacher, CityDict
from .forms import UserAskForm

from .models import CourseOrg
from  operation.models import UserFavorite


# Create your views here.



class OrgView(View):
	def get(self, request):
		all_orgs = CourseOrg.objects.all()
		hot_orgs = all_orgs.order_by("-click_num")[:3]
		
		all_citys = CityDict.objects.all()
		
		# 机构搜索
		search_keywords = request.GET.get('keywords', "")
		
		if search_keywords:
			all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) |
			                           Q(desc__icontains=search_keywords))
		
		# 城市筛选
		city_id = request.GET.get('city', "")
		if city_id:
			all_orgs = all_orgs.filter(city_id=int(city_id))
		
		# 类别筛选
		category = request.GET.get('ct', "")
		if category:
			all_orgs = all_orgs.filter(category=category)
		
		# 排序
		sort = request.GET.get('sort', "")
		if sort:
			if sort == 'students':
				
				all_orgs = all_orgs.order_by("-students")
			elif sort == 'courses':
				all_orgs = all_orgs.order_by("-course_nums")
			else:
				pass
		
		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1
		
		p = Paginator(all_orgs, 3, request=request)
		
		orgs = p.page(page)
		org_nums = all_orgs.count()
		return render(request, "org-list.html", {
			"all_orgs": orgs,
			"all_citys": all_citys,
			"org_nums": org_nums,
			"city_id": city_id,
			"category": category,
			"hot_orgs": hot_orgs,
			"sort": sort,
		})


class AddUserView(View):
	"""用户添加提交"""
	
	def post(self, request):
		user_ask = UserAskForm(request.POST)
		if user_ask.is_valid():
			user_ask = user_ask.save(commit=True)
			return HttpResponse('{"status":"success"}', content_type='application/json')
		else:
			return HttpResponse('{"status":"fail","msg":u"请填写正确信息"}')


class OrgHomeView(View):
	"""机构首页"""
	
	def get(self, request, org_id):
		current_page = 'home'
		course_org = CourseOrg.objects.get(id=int(org_id))
		course_org.click_num += 1
		course_org.save()
		all_courses = course_org.course_set.all()
		all_teacher = course_org.teacher_set.all()
		
		# 判断用户是否登陆
		has_fav = False
		if request.user.is_authenticated():
			if UserFavorite.objects.filter(user_id=request.user, fav_id=course_org.id, fav_type=2):
				has_fav = True
		
		return render(request, 'org-detail-homepage.html', {
			'all_courses': all_courses,
			'all_teacher': all_teacher,
			'course_org': course_org,
			'current_page': current_page,
			'has_fav': has_fav,
			
		})


class OrgCourseView(View):
	"""机构课程列表"""
	
	def get(self, request, org_id):
		current_page = 'course'
		course_org = CourseOrg.objects.get(id=int(org_id))
		all_courses = course_org.course_set.all()
		has_fav = False
		if request.user.is_authenticated():
			if UserFavorite.objects.filter(user_id=request.user, fav_id=course_org.id, fav_type=2):
				has_fav = True
		
		return render(request, 'org-detail-course.html', {
			'all_courses': all_courses,
			'course_org': course_org,
			'current_page': current_page,
			'has_fav': has_fav,
			
		})


class OrgDescView(View):
	"""机构课程列表"""
	
	def get(self, request, org_id):
		current_page = 'desc'
		course_org = CourseOrg.objects.get(id=int(org_id))
		all_courses = course_org.course_set.all()
		has_fav = False
		if request.user.is_authenticated():
			if UserFavorite.objects.filter(user_id=request.user, fav_id=course_org.id, fav_type=2):
				has_fav = True
		return render(request, 'org-detail-desc.html', {
			'all_courses': all_courses,
			'course_org': course_org,
			'current_page': current_page,
			'has_fav': has_fav,
			
		})


class OrgTeacherView(View):
	"""机构课程列表"""
	
	def get(self, request, org_id):
		current_page = 'teacher'
		course_org = CourseOrg.objects.get(id=int(org_id))
		
		all_teacher = course_org.teacher_set.all()
		has_fav = False
		if request.user.is_authenticated():
			if UserFavorite.objects.filter(user_id=request.user, fav_id=course_org.id, fav_type=2):
				has_fav = True
		return render(request, 'org-detail-teachers.html', {
			'all_teacher': all_teacher,
			'course_org': course_org,
			'current_page': current_page,
			'has_fav': has_fav,
			
		})


class AddFavView(View):
	"""用户收藏 and  取消收藏"""
	
	def post(self, request):
		fav_id = request.POST.get('fav_id', 0)
		fav_type = request.POST.get('fav_type', 0)
		
		if not request.user.is_authenticated():
			# 判断用户是否登陆
			return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
		exist_records = UserFavorite.objects.filter(user_id=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
		if exist_records:
			# 用户已经存在 表示删除
			exist_records.delete()
			if int(fav_type) == 1:
				course = Course.objects.get(id=int(fav_id))
				course.fav_nums -= 1
				if course.fav_nums < 0:
					course.fav_nums = 0
				course.save()
			elif int(fav_type) == 2:
				course_org = CourseOrg.objects.get(id=int(fav_id))
				course_org.fav_nums -= 1
				if course_org.fav_nums < 0:
					course_org.fav_nums = 0
				course_org.save()
			elif int(fav_type) == 3:
				teacher = Teacher.objects.get(id=int(fav_id))
				teacher.fav_nums -= 1
				if teacher.fav_nums < 0:
					teacher.fav_nums = 0
				
				teacher.save()
			else:
				pass
			
			return HttpResponse('{"status":"success","msg":"收藏 "}', content_type='application/json')
		else:
			user_fav = UserFavorite()
			if int(fav_id) > 0 and int(fav_type) > 0:
				user_fav.user = request.user
				user_fav.fav_id = int(fav_id)
				user_fav.fav_type = int(fav_type)
				user_fav.save()
				if int(fav_type) == 1:
					course = Course.objects.get(id=int(fav_id))
					course.fav_nums += 1
					course.save()
				elif int(fav_type) == 2:
					course_org = CourseOrg.objects.get(id=int(fav_id))
					course_org.fav_nums += 1
					course_org.save()
				elif int(fav_type) == 3:
					teacher = Teacher.objects.get(id=int(fav_id))
					teacher.fav_nums += 1
					teacher.save()
				else:
					pass
				
				return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
			else:
				return HttpResponse('{"status":"fail","msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
	"""课程讲师列表"""
	
	def get(self, request):
		all_teacher = Teacher.objects.all()
		sort = request.GET.get('sort', "")
		
		# 课程搜索
		search_keywords = request.GET.get('keywords', "")
		
		if search_keywords:
			all_teacher = all_teacher.filter(Q(name__icontains=search_keywords) |
			                                 Q(work_company__icontains=search_keywords) |
			                                 Q(work_position__icontains=search_keywords))
		
		# 排序
		if sort:
			if sort == 'hot':
				all_teacher = all_teacher.order_by("-click_nums")
		
		sorted_teacher = Teacher.objects.all().order_by("-click_nums")[:4]
		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1
		p = Paginator(all_teacher, 20, request=request)
		
		all_teacher = p.page(page)
		return render(request, "teachers-list.html", {
			'all_teacher': all_teacher,
			'sorted_teacher': sorted_teacher,
			'sort': sort,
		})


class TeacherDetailView(View):
	"""课程讲师列表"""
	
	def get(self, request, teacher_id):
		teacher = Teacher.objects.get(id=int(teacher_id))
		teacher.click_nums += 1
		teacher.save()
		all_courses = Course.objects.filter(teacher=teacher)
		
		# 讲师排行
		sorted_teacher = Teacher.objects.all().order_by("-click_nums")[:4]
		
		# 收藏
		has_teacher_faved = False
		if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
			has_teacher_faved = True
		
		has_org_faved = False
		if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
			has_org_faved = True
		
		return render(request, "teacher-detail.html", {
			'teacher': teacher,
			'all_courses': all_courses,
			'sorted_teacher': sorted_teacher,
			'has_teacher_faved': has_teacher_faved,
			'has_org_faved': has_org_faved,
			
		})
