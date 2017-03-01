#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by iFantastic on '2017/2/17 15:17'
import itchat

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    return msg['Text']

itchat.auto_login()
itchat.run()