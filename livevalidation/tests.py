import unittest
from livevalidation.validator import test
from livevalidation.templatetags.lv_tags import live_validate
from django import template

test()

class TestValidation(unittest.TestCase):
    def test_form(self):
        from django.contrib.auth.forms import UserChangeForm
        t = template.Template('{% load lv_tags %}{% live_validate form %}')
        print t.render(template.Context({'form':UserChangeForm()}))
        