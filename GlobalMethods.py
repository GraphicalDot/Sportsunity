#!/usr/bin/env python
#-*- coding: utf-8 -*-

def unicode_or_bust(obj, encoding='utf-8'):
        if isinstance(obj, basestring):
                if not isinstance(obj, unicode):
                        obj = unicode(obj, encoding)                                                                                                                                                         
        return obj                                                                                                                                                                                           
