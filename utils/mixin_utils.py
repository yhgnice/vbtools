#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Nice... on '2017/2/24 10:16'
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
	@method_decorator(login_required(login_url='/login/'))
	def dispatch(self, request, *args, **kwargs):
		return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
