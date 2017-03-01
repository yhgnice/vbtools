#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by iFantastic on '2017/2/14 17:12'
from .models import CourseOrg, Teacher, CityDict
import xadmin


class CourseOrgAdmin(object):
	list_display = ['name', 'desc', 'click_num', 'fav_nums', 'address']
	list_filter = ['name', 'desc', 'click_num', 'fav_nums', 'address', ]
	search_fields = ['name', 'desc', 'click_num', 'fav_nums', 'address']


class TeacherAdmin(object):
	list_display = ['org', 'name', 'work_years', 'work_company', 'add_time']
	list_filter = ['org', 'name', 'work_years', 'work_company', 'add_time']
	search_fields = ['org', 'name', 'work_years', 'work_company', ]


class CityDictAdmin(object):
	list_display = ['name', 'desc', 'add_time']
	list_filter = ['name', 'desc', 'add_time']
	search_fields = ['name', 'desc', ]


xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(CityDict, CityDictAdmin)
