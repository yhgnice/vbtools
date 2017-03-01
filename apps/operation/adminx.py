#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by iFantastic on '2017/2/15 11:22'

from .models import UserAsk, CourseComments, UserFavorite, UserMessage, UserCourse
import xadmin


class UserAskAdmin(object):
	list_display = ['name', 'mobile', 'course_name', 'add_time']
	list_filter = ['name', 'mobile', 'course_name']
	search_fields = ['name', 'mobile', 'course_name', 'add_time']


class CourseCommentsAdmin(object):
	list_display = ['user', 'course', 'comment', 'add_time']
	list_filter = ['user', 'course', 'comment', 'add_time']
	search_fields = ['user', 'course', 'comment', ]


class UserFavoriteAdmin(object):
	list_display = ['user', 'fav_id', 'fav_type', 'add_time']
	list_filter = ['user', 'fav_id', 'fav_type', 'add_time']
	search_fields = ['user', 'fav_id', 'fav_type']


class UserMessageAdmin(object):
	list_display = ['user', 'message', 'has_read', 'add_time']
	list_filter = ['user', 'message', 'has_read', 'add_time']
	search_fields = ['user', 'message', 'has_read']


class UserCourseAdmin(object):
	list_display = ['user', 'course', 'add_time']
	list_filter = ['user', 'course', 'add_time']
	search_fields = ['user', 'course', ]

 
xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
