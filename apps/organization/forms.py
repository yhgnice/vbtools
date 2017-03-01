#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by iFantastic on '2017/2/17 17:54'

import re
from django import forms
from operation.models import UserAsk
 
class UserAskForm(forms.ModelForm):
	class Meta:
		model = UserAsk
		fields = ['name','mobile','course_name']
	
	# def clean_mobile(self):
	# 	mobile = self.cleaned_data['mobile']
	# 	regex = re.compile(r'1\d{10}', mobile)
	# 	if regex:
	# 		return regex
	# 	else:
	# 		raise forms.ValidationError(u'手机号码错误',code="mobile_invlead")
 
		
	
 