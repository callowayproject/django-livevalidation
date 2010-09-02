Django Live Validation
======================
 
Django Live Validation provides quick and easy client-side form validation which validates as you type.
It uses the `Live Validation <http://livevalidation.com/>`_ JS library in conjunction with Django Forms.
This is by no means a replacement to Django's built in form validation, but it is a suppliment which is purely client-side baed which cuts down on server-side requests for validation. 
This version of django-livevalidation requires Django >= 1.2, for previous versions please use this project: http://opensource.washingtontimes.com/projects/django-livevalidation/


Install
--------

Place ``'livevalidaiton'`` into your ``INSTALLED_APPS`` and make sure it is above the Django admin since it overrides some of the admin templates::

    INSTALLED_APPS = (
        'livevalidation',
        ...
        'django.contrib.admin',
    )
 

Usage
------

To use livevalidation in your templates, make sure you load the headers first before doing anything::

    {% include 'livevalidation/header.html' %}
    
This loads the JS library at ``js/livevalidation_standalone.compressed.js`` and the CSS at ``css/livevalidation.css``. Feel free to tweak the CSS to your liking

Now you can use the templatetag to validate a form instance::

    {% live_validate form [option=value ...] %}
    
Where the ``form`` is any ``django.forms.Form`` (or subclass) instance. 
The optional option=value kwargs are in pairs as follows:

-  **validMessage** - message to be used upon successful validation (DEFAULT: "Thankyou!")
-  **onValid** - javascript function name to execute when field passes validation 
-  **onInvalid** - javascript function name to execute when field fails validation
-  **insertAfterWhatNode** - id of node to have the message inserted after (DEFAULT: the field that is being validated)
-  **onlyOnBlur** - whether you want it to validate as you type or only on blur (DEFAULT: False)
-  **wait** - the time you want it to pause from the last keystroke before it validates (milliseconds) (DEFAULT: 0)
-  **onlyOnSubmit** - if it is part of a form, whether you want it to validate it only when the form is submitted (DEFAULT: False)