from livevalidation.validator import *
from livevalidation.settings import *
from django import template
from django.forms import fields

register = template.Library()

class ValidationNode(template.Node):
    def __init__(self, form, *opts):
        self.form = form
        self.opts = {'validMessage':' '}
        for opt in opts:
            a,b = map(str,opt.split('=')[:2])
            if a in ('onValid','onInvalid'):
                b = '%s()'%b
            self.opts[a] = b
    
    def render(self, context):
        result = ['<script type="text/javascript">']
        self.form = context[self.form]
        self.formcls = self.form.__class__
        try:
            # admin formset
            fields = self.form.form.fields
            prefix = '%s-'%self.form.prefix if self.form.form.prefix else ''
        except AttributeError:
            try:
                # regular form
                fields = self.form.fields
            except AttributeError:
                raise template.TemplateSyntaxError('Form %s has no fields'%self.form)
            prefix = '%s-'%self.form.prefix if self.form.prefix else ''
        for name,field in fields.items():
            result.append(self.do_field('%s%s'%(prefix,name),field))
        try:
            result.append(LV_EXTRA_SCRIPT%{'fieldname':'id_%s'%fields.keys()[1]})
        except:
            return ''
        result.append('</script>')
        return '\n\n'.join(filter(None,result))
        
    def do_field(self, name, field, count=0):
        fname = 'id_%s'%name
        # TODO: make a special case for the split dt field (id_0,id_1)
        #if isinstance(field, fields.SplitDateTimeField):
        #    fname += '_%d'%count
        if field.__class__ in LV_FIELDS and not LV_FIELDS[field.__class__]:
            self.opts.update(onlyOnSubmit=True)        
        lv = LiveValidation(fname, **self.opts)
        fail = field.default_error_messages.get('invalid',None)
        extrakw = {'validMessage':' '}
        if fail:
            extrakw['failureMessage'] = str(fail[:])
        if self.formcls in LV_VALIDATORS:
            if name in LV_VALIDATORS[self.formcls]:
                for v,kw in LV_VALIDATORS[self.formcls][name].items():
                    extrakw.update(kw)
                    lv.add(v,**extrakw)
                return str(lv)
        # We have to check for FileFields and ImageFields since if you are changing
        # a form, they will already be set, and you don't need to re-upload them.
        # TODO: Find a way around skipping file and image fields
        if hasattr(field,'required') and field.required and not isinstance(field, (fields.FileField, fields.ImageField)):
            lv.add(Presence, **extrakw)
        #else:
         #   return str(lv)
        if hasattr(field, 'max_length'):
            v = getattr(field,'max_length')
            if v: lv.add(Length, maximum=v, **extrakw)
        if hasattr(field, 'min_length'):
            v = getattr(field,'min_length')
            if v: lv.add(Length, minimum=v, **extrakw)
        if not (isinstance(field, fields.EmailField) or isinstance(field, fields.URLField)) and hasattr(field, 'regex'):
            lv.add(Format, pattern=field.regex.pattern, **extrakw)
        if field.__class__ in LV_FIELDS and LV_FIELDS[field.__class__]:
            for v,kw in LV_FIELDS[field.__class__].items():
                extrakw.update(kw)
                lv.add(v, **extrakw)
                
        if str(lv):
            return """try{
%s
}catch(e){}"""%str(lv)
        return ''
    
def live_validate(parser, token):
    """Live Validation JavaScript Generator for Django Forms

    {% live_validate <form> [option=value ...] %}
    
    Where the <form> is any django.forms.Form (or subclass) instance
    The optional option=value kwargs are in pairs as follows:
    
        -  validMessage = message to be used upon successful validation (DEFAULT: "Thankyou!")
        -  onValid = javascript function name to execute when field passes validation 
        -  onInvalid = javascript function name to execute when field fails validation
        -  insertAfterWhatNode = id of node to have the message inserted after (DEFAULT: the field that is being validated)
        -  onlyOnBlur = whether you want it to validate as you type or only on blur (DEFAULT: False)
        -  wait = the time you want it to pause from the last keystroke before it validates (milliseconds) (DEFAULT: 0)
        -  onlyOnSubmit = if it is part of a form, whether you want it to validate it only when the form is submitted (DEFAULT: False)
    """
    return ValidationNode(*token.split_contents()[1:])
register.tag(live_validate)
