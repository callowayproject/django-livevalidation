"""
Python Wrapper for Live Validation JavaScript

Generates javascript using template tags to comply with the LiveValidation library.
When used in combination, any form instance can be turned into javascript code that
validates the form fields before posting the form. This reduces server load by cutting
down on requests containing invalid fields (eg email=IAmSoNotAnEmail) and
improves user experience with live feedback and reduces human error.
"""

def inner(items):
    """
    Sorted items to display as compatable js objects (eg bool,regex)
    """
    for k,v in sorted(items):
        if k == 'is_':
            k = 'is'
        if isinstance(v,bool):
            yield '%s: %s'%(k,repr(v).lower())
        elif k == 'pattern':
            yield '%s: new RegExp(/%s/)'%(k,v)
        else:
            yield '%s: %r'%(k,v)
            
class Meta:
    """
    Abstract meta class for formatting the javascript commands
    """
    def __init__(self, *a, **kw):
        self.a = a
        self.kw = kw
        
    def format_kw(self):
        return '{ %s }'%', '.join(inner(self.kw.items()))
        
        
    def format_a(self):
        if not len(self.a): return
        if isinstance(self.a[0],basestring):
            return repr(self.a[0])
        elif isinstance(self.a[0],bool):
            return repr(self.a[0]).lower()
        return self.a[0]
        
    def __str__(self):
        if len(self.a):
            return 'Validate.%s( %s, %s)'% (
                self.__class__.__name__,
                self.format_a(),
                self.format_kw()
            )
        return 'Validate.%s, %s'% (
            self.__class__.__name__,
            self.format_kw()
        )

class Presence(Meta):
    """Validates that a value is present (ie. not null, undefined, or an empty string)
    
    args:
        - value - {mixed} - value to be checked
    
    kwargs:
        - failureMessage (optional) - {String} - message to be used upon validation failure (DEFAULT: "Can't be empty!")
        
        >>> print Presence('hello world', failureMessage='Supply a value!')
        Validate.Presence( 'hello world', { failureMessage: 'Supply a value!' })
    """
    
class Format(Meta):
    """Validates a value against a regular expression
    
    args:
        - value - {mixed} - value to be checked

    kwargs:
        - failureMessage (optional) - {String} - message to be used upon validation failure (DEFAULT: "Not valid!")
        - pattern - {RegExp} - regular expression to validate against (DEFAULT: /./i)
        - negate - {Boolean} - if true will be valid if the value DOES NOT match the regular expression (DEFAULT: false)
        
        >>> # check that 'validation' exists in the string, case insensitive...
        >>> print Format('live validation', pattern = r'^validation$', failureMessage = 'Failed!' )
        Validate.Format( 'live validation', { failureMessage: 'Failed!', pattern: new RegExp(/^validation$/) })
    """
        
class Numericality(Meta):
    """Validates that the value is numeric and: is an integer, is a specific number,
    is more than a minimum number, less than a maximum number, is within a range of numbers, or a combination of these
    
    args:
        - value - {mixed} - value to be checked

    kwargs:
        - notANumberMessage (optional) - {String} - message to be used when validation fails because value is not a number (DEFAULT: "Must be a number!")
        - notAnIntegerMessage (optional) - {String} - message to be used when validation fails because value is not an integer (DEFAULT: "Must be an integer!")
        - wrongNumberMessage (optional) - {String} - message to be used when validation fails when 'is_' param is used (DEFAULT: "Must be {is}!")
        - tooLowMessage (optional) - {String} - message to be used when validation fails when 'minimum' param is used (DEFAULT: "Must not be less than {minimum}!")
        - tooHighMessage (optional) - {String} - message to be used when validation fails when 'maximum' param is used (DEFAULT: "Must not be more than {maximum}!")
        - is_ (optional) - {mixed} - the value must be equal to this numeric value
        - minimum (optional) - {mixed} - the minimum numeric allowed
        - maximum (optional) - {mixed} - the maximum numeric allowed
        - onlyInteger (optional) - {Boolean} - if true will only allow integers to be valid (DEFAULT: false)
    
        >>> # check that value is an integer between -5 and 2000 exists in the string, case insensitive...
        >>> print Numericality( 2000.0, minimum= -5, maximum= 2000)
        Validate.Numericality( 2000.0, { maximum: 2000, minimum: -5 })
    """
    
class Length(Meta):
    """Validates the length of a value is a particular length,
    is more than a minimum, less than a maximum, or between a range of lengths
    
    args:
        - value - {mixed} - value to be checked
    
    kwargs:
        - wrongLengthMessage (optional) - {String} - message to be used when validation fails when 'is_' param is used (DEFAULT: "Must be {is_} characters long!")
        - tooShortMessage (optional) - {String} - message to be used when validation fails when 'minimum' param is used (DEFAULT: "Must not be less than {minimum} characters long!")
        - tooLongMessage (optional) - {String} - message to be used when validation fails when 'maximum' param is used (DEFAULT: "Must not be more than {maximum} characters long!")
        - is_ (optional) - {mixed} - the value must be this length
        - minimum (optional) - {mixed} - the minimum length allowed
        - maximum (optional) - {mixed} - the maximum length allowed
        
        >>> # check that value is between 3 and 255 characters long...
        >>> print Length( 'cow', minimum=3, maximum=255  )
        Validate.Length( 'cow', { maximum: 255, minimum: 3 })
    """
    
class Inclusion(Meta):
    """Validates that a value falls within a given set of values
    
    args:
        - value - {mixed} - value to be checked
    
    kwargs:
        - failureMessage (optional) - {String} - message to be used upon validation failure (DEFAULT: "Must be included in the list!")
        - within - {Array} - an array of values that the value should fall in (DEFAULT: Empty array)
        - allowNull (optional) - {Boolean} - if true, and a null value is passed in, validates as true (DEFAULT: false)
        - partialMatch (optional) - {Boolean}- if true, will not only validate against the whole value to check, but also if it is a substring of the value (DEFAULT: false)
        - caseSensitive (optional) - {Boolean} - if false will compare strings case insensitively(DEFAULT: true)
        
        >>> print Inclusion( 'cat', within = [ 'cow', 277, 'catdog' ], allowNull = True, partialMatch = True, caseSensitive= False)
        Validate.Inclusion( 'cat', { allowNull: true, caseSensitive: false, partialMatch: true, within: ['cow', 277, 'catdog'] })
    """
  
class Exclusion(Meta):
    """Validates that a value does not fall within a given set of values
    
    args:
        - value - {mixed} - value to be checked
    
    kwargs:  
        - failureMessage (optional) - {String} - message to be used upon validation failure (DEFAULT: "Must not be included in the list!")
        - within - {Array} - an array of values that the given value should not fall in (DEFAULT: Empty array)
        - allowNull (optional) - {Boolean} - if true, and a null value is passed in, validates as true (DEFAULT: false)
        - partialMatch (optional) - {Boolean} - if true, will not only validate against the whole value to check, but also if it is a substring of the value (DEFAULT: false)
        - caseSensitive (optional) - {Boolean} - if false will compare strings case insensitively(DEFAULT: true)
        
        >>> print Exclusion( 'pig', within = [ 'cow', 277, 'catdog' ], allowNull = True, partialMatch = True, caseSensitive= False)
        Validate.Exclusion( 'pig', { allowNull: true, caseSensitive: false, partialMatch: true, within: ['cow', 277, 'catdog'] })
    """
    
class Acceptance(Meta):
    """Validates that a value equates to true (for use primarily in detemining if a checkbox has been checked)
    
    args:
        - value - {mixed} - value to be checked
    
    kwargs:
        - failureMessage (optional) - {String} - message to be used upon validation failure (DEFAULT: "Must be accepted!")
        
        >>> print Acceptance( True, failureMessage="You must be true!" )
        Validate.Acceptance( true, { failureMessage: 'You must be true!' })
    """

class Confirmation(Meta):
    """Validates that a value matches that of a given form field
    
    args:
        - value - {mixed} - value to be checked
    
    kwargs:
        - failureMessage (optional) - {String} - message to be used upon validation failure (DEFAULT: "Does not match!")
        - match -{mixed} - a reference to, or string id of the field that this should match

        >>> print Confirmation( 'open sesame', match = 'myPasswordField', failureMessage= "Your passwords don't match!" )
        Validate.Confirmation( 'open sesame', { failureMessage: "Your passwords don't match!", match: 'myPasswordField' })
    """
    
class Email(Meta):
    """Validates a value is a valid email address
    
    args:
        - value - {mixed} - value to be checked
    
    kwargs:
        - failureMessage (optional) - {String} - message to be used upon validation failure (DEFAULT: "Must be a valid email address!")
    
        >>> print Email( 'live@validation.com', failureMessage= "I am an overridden message!" )
        Validate.Email( 'live@validation.com', { failureMessage: 'I am an overridden message!' })
    """
    
class Custom(Meta):
    """Validates a value against a custom function that returns true when valid or false when not valid.
    You can use this to easily wrap any special validations that are not covered by the core ones,
    in a way that the LiveValidation class can use to give the feedback, without having to worry about the details.
    
    args:
        - value - {mixed} - value to be checked
    
    kwargs:
        - against - {Function} - a function that will take the value and an object of arguments and return true or false(DEFAULT: function( value, args ){ return true; } )
        - args - {Object} - an object of named arguments that will be passed to the custom function so are accessible through this object (DEFAULT: Empty object)
        - failureMessage (optional) - {String} - message to be used upon validation failure (DEFAULT: "Not valid!")
        
    #>>> # Pass a function that checks if a number is divisible by one that you pass it in args object
    #>>> # In this case, 5 is passed, so should return true and validation will pass
    #>>> Custom( 55, against="function(value,args){ return !(value % args.divisibleBy) }", args= "{divisibleBy: 5}" )
    #... "Validate.Custom( 55, { against: function(value,args){ return !(value % args.divisibleBy) }, args: {divisibleBy: 5} } );"
    """
    
class now(Meta):
    """Validates a passed in value using the passed in validation function,
    and handles the validation error for you so it gives a nice true or false reply
    
    args:
        - validationFunction - {Function} - reference to the validation function to be used (ie Validate.Presence )
        - value - {mixed} - value to be checked
    
    kwargs:
        - Parameters to be used for the validation (optional depends upon the validation function)
    
        >>> print now( Numericality, '2007', is_= 2007 )
        Validate.now( Numericality, '2007', { is: 2007 })
    """
    def format_a(self):
        return '%s, %r'%(self.a[0].__name__,self.a[1])

class LiveValidation:
    """The LiveValidation class sets up a text, checkbox, file, or password input,
    or a textarea to allow its value to be validated in real-time based upon the validations you assign to it.
 
    args:
        - element - {String} - the string id of the element to validate
 
    kwargs:
        - validMessage (optional) - {String} - message to be used upon successful validation (DEFAULT: "Thankyou!")
        - onValid (optional) - {Function} - function to execute when field passes validation (DEFAULT: function(){ this.insertMessage( this.createMessageSpan() ); this.addFieldClass(); } )
        - onInvalid (optional) - {Function} - function to execute when field fails validation (DEFAULT: function(){ this.insertMessage( this.createMessageSpan() ); this.addFieldClass(); })
        - insertAfterWhatNode (optional) - {mixed} - reference or id of node to have the message inserted after (DEFAULT: the field that is being validated)
        - onlyOnBlur (optional) - {Boolean} - whether you want it to validate as you type or only on blur (DEFAULT: false)
        - wait (optional) - {Integer} - the time you want it to pause from the last keystroke before it validates (milliseconds) (DEFAULT: 0)
        - onlyOnSubmit (optional) - {Boolean} - if it is part of a form, whether you want it to validate it only when the form is submitted (DEFAULT: false)
    
        >>> usern = LiveValidation('id_username', wait=10)
        >>> usern.add(Format, pattern= r'/^hello$/i') #doctest: +ELLIPSIS
        <livevalidation.validator.LiveValidation instance at...
        >>> usern.disable() #doctest: +ELLIPSIS
        <livevalidation.validator.LiveValidation instance at...
        >>> usern.enable() #doctest: +ELLIPSIS
        <livevalidation.validator.LiveValidation instance at...
        >>> usern.remove(Format, minimum= r'/^woohoo+$/') #doctest: +ELLIPSIS
        <livevalidation.validator.LiveValidation instance at...
        """
    def __init__(self,element,**kw):
        self.element = element.replace('-', '_')
        self.commands = ["var LV%s =  new LiveValidation('%s', { %s });"%\
                         (self.element,element,','.join(inner(kw.items())))]
        
    def add(self, validator, **kw):
        """
        Validates a passed in value using the passed in validation function,
        and handles the validation error for you so it gives a nice true or false reply.
        """
        self._format('add',validator(**kw))
        return self
    
    def extend(self, item):
        for i in item:
            self.add(i[0],**i[1])
            
    def remove(self, validator, **kw):
        """
        Removes a specific validation from the stack of validations that have been added
        
        Note - you must pass it EXACTLY the same arguments as you used to add the validation
        """
        self._format('remove',validator(**kw))
        return self  
    
    def enable(self):
        """
        A helper to enable a disabled field.

        Will cause validations to be performed on the field again, after having been previously disabled.
        """
        self._format('enable','')
        return self
   
    def disable(self):
        """
        A helper to disable a field, so that validations are not run on it,
        and its value will not be posted if part of a form.
        It will also remove any previous validation message and field class.
        """
        self._format('disable','')
        return self
    
    def destroy(self):
        """
        Will unregister all events of the LiveValidation object (preserving
        previously defined events) and remove it from any LiveValidationForm it might belong to.

        This is useful if you don't want a field to be a LiveValidation field any longer,
        or need to redefine a field as a new LiveValidation object with different parameters.
        """
        self._format('destroy','')
        return self
    
    def _format(self,*a):
        a = (self.element,)+a
        self.commands.append('LV%s.%s(%s);'%a)
        
    def __str__(self):
        if len(self.commands) > 1:
            return '\n'.join(self.commands)
        return ''

    
