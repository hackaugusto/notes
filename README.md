pynotes
-------

Dark things that I want to remember myself about python

Meta classes
------------

- Do not forget that a metaclass must subclass `type` not `object`
- `__metaclass__` can be either a function (with the same signature as `type`) or a `type` subclass

ABC and meta classes doesn't seem to go quite well together, for instance:

    class Meta(type):
        def __new__(metaclass, name, bases, attributes):
            print(metaclass)
            type.__new__(metaclass, name, bases, attributes)
        
    class MyList(UserList):
        # this will work fine and will print "MyList" into the screen
        __metaclass__ = Meta
      
    class SubList(MyList):
        # On the other hand, this will _not_ work
        pass
        
To solve this case is just a matter of making `Meta` a subclass of `UserList`

type inheritance
----------------

This PEP defines the method resolution order (MRO) [Subtyping Built-in Types](http://legacy.python.org/dev/peps/pep-0253/)

- old style MRO: left-to-right depth first
- new style MRO:

As of python 2.7.6:

`cStringIO.StringIO` is not a class, it is a c function wrapper `<type 'builtin_function_or_method'>` that cannot be used for subclassing check, the instance returned by the function are named `cStringIO.StringI` for string input and `cStringIO.StringO` for output, these types are exported to python as `cStringIO.InputType` and `cStringIO.OutputType`.

`collections.namedtuple` are a different beast, they are created by `exec`ing a code template that creates a subclass of `tuple`, so there is no type `namedtuple`, only subclasses of `tuple`. You can _lossely_ check for a `namedtuple` using `issubclass(obj.__class__, tuple)`, this will return `True` for subclasses of `tuple` and `False` for `tuple` itself.



Decorators
----------

- Take care while decorating methods (because the wrapper function will be the method and not the decorated function) [Read about the descriptor protocol to know what is going on]

super
-----

It is a class

descriptors
-----------

This pep describes the descriptor protocol [Making Types Look More Like Classes ](http://legacy.python.org/dev/peps/pep-0252/) [`__methods__` seems to have been dropped]

It defines how attributes are defined (to be introspected):

    class MetaClass(type): pass
    class NormalClass(MetaClass): pass
    obj = NormalClass()

Attribute lookup order for `obj.attr`:

- `obj.__class__.__dict__` if the value has `__set__` (static attribute that are data descriptors have precedence)
- `obj.__dict__`
- `obj.__class__.__dict__`
- for each base as `obj.__class__.__bases__` in MRO order return the first with "attr" in `base.__dict__`

Descriptors:

If "a" is a function defined in a class or metaclass and it does have the `__get__` and/or `__set__` method defined:

`obj.a = 1` calls `obj.__class__.__dict__['a'].__set__(obj, 1)`
`obj.a` calls `obj.__class__.__dict__['a'].__get__(a, a.__class__)` (bind operation, returns a method if it is not staticmethod or classmethod)
`C.a` class `C.__dict__['a'].__get__(None, C)` (does not bind because of the absence of an obj [using None], returns an unbound method)


