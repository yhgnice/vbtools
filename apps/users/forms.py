#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by iFantastic on '2017/2/16 11:17'
from django import forms
from captcha.fields import CaptchaField
 

from users.models import UserProfile


class LoginForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True,min_length=6)
	

class RegisterForm(forms.Form):
	email = forms.EmailField(required=True)
	password = forms.CharField(required=True,min_length=6)
	captcha = CaptchaField(error_messages={"invalid":u"验证码错误!"})
	

class UploadImageForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['image']
		
	