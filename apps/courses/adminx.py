#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by iFantastic on '2017/2/14 17:49'

from .models import Course, CourseResource, Video, Lesson

import xadmin


class CourseAdmin(object):
	list_display = ['name','desc','detail','degree','add_time','students']
	list_filter = ['name','desc','detail','degree','add_time','students']
	search_fields = ['name','desc','detail','degree','add_time','students']
 

class CourseResourceAdmin(object):
	list_display = ['course', 'name', 'download', 'add_time',]
	list_filter = ['course', 'name', 'download', 'add_time',]
	search_fields = ['course', 'name', 'download', 'add_time',]
 

class VideoAdmin(object):
 
	list_display = ['lesson', 'name', 'add_time', ]
	list_filter = ['lesson', 'name','add_time' ]
	search_fields = ['lesson', 'name', 'add_time',]
 


class LessonAdmin(object):
	list_display = ['course', 'name', 'add_time', ]
	list_filter = ['course', 'name','add_time' ]
	search_fields = ['course', 'name', 'add_time',]
 


xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
