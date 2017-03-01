#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Nice... on '2017/2/27 11:15'
from django.conf.urls import url
from .views import UserInfoView, UploadImageView, MyCourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseView, \
	MymessgaeView

urlpatterns = [
	# 个人信息
	url(r'^info/$', UserInfoView.as_view(), name="user_info"),
	# 上传图片
	url(r'^image/$', UploadImageView.as_view(), name="upload_image"),
	# 我的课程
	url(r'^mycourse/$', MyCourseView.as_view(), name="mycourse"),
	# 我的收藏
	url(r'^myfav/org/$', MyFavOrgView.as_view(), name="myfav_org"),
	# 收藏的老师
	url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name="myfav_teacher"),
	# 收藏课程
	url(r'^myfav/course/$', MyFavCourseView.as_view(), name="myfav_course"),
	# 我的消息
	url(r'^mymessage/$', MymessgaeView.as_view(), name="mymessage"),

]
