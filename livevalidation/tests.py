from doctest import testmod

from django.test import TestCase
from django import template
from django.contrib.auth.forms import UserChangeForm

from livevalidation import validator


class TestValidation(TestCase):
    def test_form(self):
        t = template.Template('{% load live_validation %}{% live_validate form %}')
        content = t.render(template.Context({'form':UserChangeForm()}))
        
        look_for = [
            "LVid_username.add(Validate.Format, { failureMessage: 'Alphanumeric characters only!', pattern: new RegExp(/^\w+$/), validMessage: ' ' });",
            "LVid_last_name.add(Validate.Length, { failureMessage: 'Enter a valid value.', maximum: 30, validMessage: ' ' });",
            #"LVid_email.add(Validate.Email, { failureMessage: 'Enter a valid e-mail address.', validMessage: ' ' });",
            "LVid_last_login.add(Validate.Format, { failureMessage: 'Must be in valid \"YYYY-MM-DD HH:MM:SS\" format!', pattern: new RegExp(/^(19|20)\d\d\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01]) ([0-1]\d|2[0-3]):([0-5]\d):([0-5]\d)$/), validMessage: ' ' });",
        ]
        
        for text in look_for:        
            self.assert_(content.find(text) >- 1)
        
    def test_validator(self):
        testmod(validator)
