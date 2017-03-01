#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by iFantastic on '2017/2/17 18:02'
from django.conf.urls import url

from .views import CourseListView, CourseDetailView, CourseInfolView, CourseCommentlView, AddCommentlView, VideoPlayView

urlpatterns = [
	url(r'^list/$', CourseListView.as_view(), name="course_list"),
	url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),
	url(r'^info/(?P<course_id>\d+)/$', CourseInfolView.as_view(), name="course_info"),
	# 评论信息
	url(r'^comment/(?P<course_id>\d+)/$', CourseCommentlView.as_view(), name="course_comment"),
	# 添加评论
	url(r'^add_comment/$', AddCommentlView.as_view(), name="add_comments"),
	# video 信息
	url(r'^video/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name="video_play"),
]
