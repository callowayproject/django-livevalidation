# These dictionaries are very scary, use w/ care
from django.conf import settings
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from django.forms.fields import *
from django.forms.models import ModelChoiceField, ModelChoiceIterator
from validator import *

# Maps a specific Form class to a specific set of validators
# As of now it trumps all other validators
LV_VALIDATORS = {
    # form or formset class
    UserChangeForm: {
        # field name
        'username': {
            # validator class
            Format: {
                # parameters
                'pattern': r'^\w+$',
                'failureMessage': 'Alphanumeric characters only!'
            }
        }
    },
    PasswordChangeForm: {   
        'old_password':{
            Presence: {}
        },
        'new_password1':{
            Presence: {}
        },
        'new_password2':{
            Presence: {},
            Confirmation: {
                'match': 'id_new_password1'
            }
        }
    }
}

LV_VALIDATORS.update(getattr(settings, 'LV_VALIDATORS', {}))

# Overall field validators
# These are used everywhere by default
LV_FIELDS = {
    # field class
    DateTimeField: {
        # validator class
        Format: {
            # parameters
            'pattern': r'^(19|20)\d\d\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01]) ([0-1]\d|2[0-3]):([0-5]\d):([0-5]\d)$',
            'failureMessage': 'Must be in valid "YYYY-MM-DD HH:MM:SS" format!'
        }
    },
    DateField: {
        Format: {
            'pattern': r'^(19|20)\d\d\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$',
            'failureMessage': 'Must be in valid "YYYY-MM-DD" format!'
        }
    },        
    EmailField: {
        Email: {}
    },
    URLField:{
        Format:{
            'pattern': r'(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?',
            'failureMessage': 'Must be a valid URL!'
        }
    },
    ModelChoiceIterator:{
        Format:{
            'pattern':r'^[\w+|,]+$',
            'failureMessage': 'Must be a comma separated list of keys!'
        }
    },
    ModelChoiceField:{},
    IntegerField:{
        Format:{
            'pattern':r'^\d+$',
            'failureMessage': 'Must be a number!'
        }
    },
    FileField:{}
}
LV_FIELDS.update(getattr(settings, 'LV_FIELDS', {}))

# Salted password
#(md5|sha1|crypt)\$[0-9|A-f]{,5}\$[0-9|A-f]+$

# The last bit of javascript to place in the tag
# Does the automagic form submit
LV_EXTRA_SCRIPT = getattr(settings,'LV_EXTRA_SCRIPT',"""
var automaticOnSubmit = LV%(fieldname)s.form.onsubmit;
LV%(fieldname)s.form.onsubmit = function(){
    var valid = automaticOnSubmit();
    if (valid)
        return true;
    return false;
}
""")