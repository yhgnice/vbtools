# coding:utf-8
from __future__ import unicode_literals
from  datetime import datetime
 

from django.db import models


# Create your models here.
from organization.models import CourseOrg, Teacher


class Course(models.Model):
	course_org = models.ForeignKey(CourseOrg, verbose_name=u"机构名称", null=True)
	name = models.CharField(max_length=50, verbose_name=u"课程名")
	desc = models.CharField(max_length=300, verbose_name=u"课程描述")
	detail = models.TextField(verbose_name=u"课程详情")
	teacher = models.ForeignKey(Teacher, verbose_name=u"讲师", blank=True, null=Teacher)
	degree = models.CharField(verbose_name=u"难度", choices=(("cj", u"初级"), ("zj", u"中级"), ("gj", u"高级")), max_length=10)
	learn_time = models.IntegerField(default=0, verbose_name=u"学习时长(分钟)")
	students = models.IntegerField(default=0, verbose_name=u"当前学习人数")
	fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
	image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"封面图片", max_length=100)
	click_nums = models.IntegerField(default=0, verbose_name=u"点击量")
	category = models.CharField(max_length=20, verbose_name=u"课程类别", default=u'后端开发')
	tag = models.CharField(max_length=20, verbose_name=u"课程标签", default="")
	youneed_know = models.CharField(max_length=300, verbose_name=u"课程须知", default="")
	teacher_tell = models.CharField(max_length=300, verbose_name=u"老师告诉你", default="")
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
	
	class Meta:
		verbose_name = u"课程"
		verbose_name_plural = verbose_name
	
	def __unicode__(self):
		return self.name
	
	def get_zj_nums(self):
		# 可以访问外键的连接属性 获取章节数
		return self.lesson_set.all().count()
	
	def get_learn_users(self):
		return self.usercourse_set.all()[:5]
	
	def get_course_lesson(self):
		return self.lesson_set.all()
	
		
	


class Lesson(models.Model):
	course = models.ForeignKey(Course, verbose_name=u"课程")
	name = models.CharField(max_length=100, verbose_name=u"章节名")
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
	
	class Meta:
		verbose_name = u"章节"
		verbose_name_plural = verbose_name
	
	def __unicode__(self):
		return self.name
	
	def get_lesson_video(self):
		return  self.video_set.all()


class Video(models.Model):
	lesson = models.ForeignKey(Lesson, verbose_name=u"章节")
	name = models.CharField(max_length=100, verbose_name=u"视频名")
	url = models.CharField(max_length=200,default="http://www.iqiyi.com/v_19rrakb0jk.html#vfrm=24-9-0-1", verbose_name=u"连接地址")
	learn_time = models.IntegerField(default=0, verbose_name=u"(分钟)")
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
	
	class Meta:
		verbose_name = u"视频"
		verbose_name_plural = verbose_name
	
	def __unicode__(self):
		return self.lesson.name


class CourseResource(models.Model):
	course = models.ForeignKey(Course, verbose_name=u"课程")
	name = models.CharField(max_length=100, verbose_name=u"名称")
	download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name=u"资源地址")
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
	
	class Meta:
		verbose_name = u"课程资源"
		verbose_name_plural = verbose_name
	
	def __unicode__(self):
		return self.name
