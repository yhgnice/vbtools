#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by iFantastic on '2017/2/14 17:42'

import xadmin
from xadmin import views
from .models import EmailVerifyrecord, UserProfile, Banner


class EmailVerifyrecordAdmin(object):
	list_display = ['code', 'email', 'send_type', 'send_time']
	search_fields = ['code', 'email', 'send_type']
	list_filter = ['code', 'email', 'send_type', 'send_time']


# free_query_filter  = ['code','email','send_type','send_time']

# exclude = ['send_time']
# fields = ('code', 'email')


class BannerAdmin(object):
	list_display = ['title', 'url', 'index', 'add_time']
	search_fields = ['title', 'url', 'index']
	list_filter = ['title', 'url', 'index', 'add_time']


class UserProfileAdmin(object):
	list_display = ['nick_name', 'birday', 'gender', 'address', 'mobile', 'image', ]
	search_fields = ['nick_name', 'birday', 'gender', 'address', 'mobile', 'image']
	list_filter = ['nick_name', 'birday', 'gender', 'address', 'mobile', 'image', ]


class BaseSetting(object):
	enable_themes = True
	use_bootswatch = True  # 设置主题


class GlobalSettings(object):
	site_title = "Search Google"
	site_footer = "Google.lnc"
	menu_style = "accordion"  # 设置menu


xadmin.site.register(EmailVerifyrecord, EmailVerifyrecordAdmin)
xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
